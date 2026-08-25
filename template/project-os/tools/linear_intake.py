#!/usr/bin/env python3
"""Deterministic Linear intake scanner and guarded write executor.

The scanner is read-only by default. Live writes require all three controls:
an apply command, an enabled config allowlist, and a runtime authorization
environment variable. Runtime state stores only sanitized receipts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable


API_URL = "https://api.linear.app/graphql"
FEATURE_ID_RE = re.compile(r"\b[A-Z][A-Z0-9-]+-\d+\b")
TARGET_VERSION_RE = re.compile(
    r"(?:Target Version|目标版本)\s*:\s*(v?\d+\.\d+(?:\.\d+)?)", re.IGNORECASE
)
ACCEPTANCE_RE = re.compile(r"Acceptance Criteria|验收标准", re.IGNORECASE)
DECISION_RE = re.compile(r"\[DEC-|Decision ID\s*:", re.IGNORECASE)
SUPPORTED_OPERATIONS = {"comment_create", "issue_update", "issue_create"}
SUPPORTED_UPDATE_FIELDS = {"stateId", "assigneeId"}
SUPPORTED_CREATE_FIELDS = {
    "teamId",
    "title",
    "description",
    "projectId",
    "stateId",
    "assigneeId",
    "labelIds",
    "priority",
}
FORBIDDEN_UPDATE_FIELDS = {
    "description",
    "projectId",
    "teamId",
    "title",
    "completedAt",
    "canceledAt",
}
QUEUE_ORDER = [
    "codex_queue",
    "codex_active",
    "human_queue",
    "human_active",
    "review_queue",
    "inconsistent",
    "closed_watch",
    "blocked_ambiguous",
    "done_closed",
]
QUEUE_LABELS = {
    "codex_queue": "Codex Queue / Codex 队列",
    "codex_active": "Codex Active / Codex 处理中",
    "human_queue": "Human Queue / 人类队列",
    "human_active": "Human Active / 人类处理中",
    "review_queue": "Review Queue / Review/UAT 队列",
    "inconsistent": "Inconsistent / 状态不一致",
    "closed_watch": "Closed Watch / 已完成事项观察",
    "blocked_ambiguous": "Blocked or Ambiguous / 阻塞或不明确",
    "done_closed": "Done or Closed / 已完成或关闭",
}


class IntakeError(RuntimeError):
    """A safe, user-facing intake failure."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Keep authorization headers from following an unexpected redirect."""

    def redirect_request(
        self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str
    ) -> None:
        raise urllib.error.HTTPError(req.full_url, code, msg, headers, fp)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stable_key(value: Any, prefix: str = "aipos") -> str:
    digest = hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()[:20]
    return f"{prefix}:{digest}"


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise IntakeError(f"File not found / 文件不存在: {path}") from exc
    except json.JSONDecodeError as exc:
        raise IntakeError(f"Invalid JSON / JSON 无效: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise IntakeError(f"Expected a JSON object / 需要 JSON object: {path}")
    return value


def validate_config(config: dict[str, Any]) -> None:
    if config.get("schema_version") != 1:
        raise IntakeError("config.schema_version must be 1")
    team = config.get("team")
    if not isinstance(team, dict) or not team.get("name"):
        raise IntakeError("config.team.name is required")
    max_issues = config.get("max_issues", 50)
    if type(max_issues) is not int or not 1 <= max_issues <= 250:
        raise IntakeError("config.max_issues must be between 1 and 250")
    lookback_days = config.get("lookback_days", 7)
    if type(lookback_days) is not int or not 1 <= lookback_days <= 365:
        raise IntakeError("config.lookback_days must be between 1 and 365")
    if config.get("language", "en+zh") != "en+zh":
        raise IntakeError("v0.6 supports language=en+zh")
    auth = config.get("auth", {})
    if not isinstance(auth, dict):
        raise IntakeError("config.auth must be an object")
    if auth.get("type", "personal_api_key") not in {"personal_api_key", "oauth"}:
        raise IntakeError("auth.type must be personal_api_key or oauth")
    if auth.get("endpoint", API_URL) != API_URL:
        raise IntakeError(f"auth.endpoint must be {API_URL}")
    token_env = auth.get("token_env", "LINEAR_API_KEY")
    if not isinstance(token_env, str) or not re.fullmatch(
        r"[A-Za-z_][A-Za-z0-9_]*", token_env
    ):
        raise IntakeError("auth.token_env must be a valid environment variable name")
    for field in [
        "projects",
        "project_name_prefixes",
        "active_statuses",
        "include_issues",
        "exclude_issues",
    ]:
        if not isinstance(config.get(field, []), list):
            raise IntakeError(f"config.{field} must be an array")
        if not all(isinstance(item, str) and item for item in config.get(field, [])):
            raise IntakeError(f"config.{field} entries must be non-empty strings")
    retry = config.get("retry", {})
    if not isinstance(retry, dict):
        raise IntakeError("config.retry must be an object")
    retries = retry.get("max_retries", 2)
    timeout = retry.get("timeout_seconds", 20)
    if type(retries) is not int or not 0 <= retries <= 5:
        raise IntakeError("retry.max_retries must be between 0 and 5")
    if type(timeout) is not int or not 1 <= timeout <= 120:
        raise IntakeError("retry.timeout_seconds must be between 1 and 120")
    state_file = str(
        config.get("state_file", "project-os/runtime/linear_intake_ledger.json")
    )
    if not state_file.startswith("project-os/runtime/"):
        raise IntakeError("config.state_file must stay under project-os/runtime/")
    policy = config.get("write_policy", {})
    if not isinstance(policy, dict):
        raise IntakeError("config.write_policy must be an object")
    if not isinstance(policy.get("enabled", False), bool):
        raise IntakeError("write_policy.enabled must be boolean")
    if not isinstance(policy.get("allowed_operations", []), list):
        raise IntakeError("write_policy.allowed_operations must be an array")
    if not isinstance(policy.get("allowed_update_fields", []), list):
        raise IntakeError("write_policy.allowed_update_fields must be an array")
    allowed = set(policy.get("allowed_operations", []))
    unknown = allowed - SUPPORTED_OPERATIONS
    if unknown:
        raise IntakeError(f"Unsupported allowed_operations: {sorted(unknown)}")
    update_fields = set(policy.get("allowed_update_fields", []))
    if not update_fields <= SUPPORTED_UPDATE_FIELDS:
        raise IntakeError(
            f"Unsupported allowed_update_fields: {sorted(update_fields - SUPPORTED_UPDATE_FIELDS)}"
        )
    max_age = policy.get("max_plan_age_minutes", 60)
    if type(max_age) is not int or not 1 <= max_age <= 1440:
        raise IntakeError("write_policy.max_plan_age_minutes must be between 1 and 1440")
    runtime_env = policy.get(
        "runtime_authorization_env", "AIPOS_LINEAR_WRITE_APPROVED"
    )
    if not isinstance(runtime_env, str) or not re.fullmatch(
        r"[A-Za-z_][A-Za-z0-9_]*", runtime_env
    ):
        raise IntakeError(
            "write_policy.runtime_authorization_env must be a valid environment variable name"
        )


@dataclass
class LinearClient:
    token: str
    auth_type: str = "personal_api_key"
    endpoint: str = API_URL
    retries: int = 2
    timeout: int = 20

    @property
    def authorization(self) -> str:
        if self.auth_type == "oauth":
            return f"Bearer {self.token}"
        return self.token

    def execute(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            request = urllib.request.Request(
                self.endpoint,
                data=payload,
                headers={
                    "Authorization": self.authorization,
                    "Content-Type": "application/json",
                    "User-Agent": "ai-project-os-linear-intake/0.6",
                },
                method="POST",
            )
            try:
                opener = urllib.request.build_opener(NoRedirect())
                with opener.open(request, timeout=self.timeout) as response:
                    result = json.loads(response.read().decode("utf-8"))
                errors = result.get("errors") or []
                if errors:
                    codes = {
                        error.get("extensions", {}).get("code")
                        for error in errors
                        if isinstance(error, dict)
                    }
                    if "RATELIMITED" in codes and attempt < self.retries:
                        time.sleep(2**attempt)
                        continue
                    messages = [str(error.get("message", "GraphQL error")) for error in errors]
                    raise IntakeError("Linear GraphQL error: " + "; ".join(messages))
                data = result.get("data")
                if not isinstance(data, dict):
                    raise IntakeError("Linear response did not contain a data object")
                return data
            except urllib.error.HTTPError as exc:
                last_error = exc
                if exc.code in {429, 500, 502, 503, 504} and attempt < self.retries:
                    time.sleep(2**attempt)
                    continue
                raise IntakeError(f"Linear HTTP error: {exc.code}") from exc
            except urllib.error.URLError as exc:
                last_error = exc
                if attempt < self.retries:
                    time.sleep(2**attempt)
                    continue
                raise IntakeError(f"Linear network error: {exc.reason}") from exc
        raise IntakeError(f"Linear request failed: {type(last_error).__name__}")

    def fetch_snapshot(self, team_id: str, max_issues: int) -> dict[str, Any]:
        query = """
        query IntakeIssues($teamId: String!, $first: Int!, $after: String) {
          team(id: $teamId) {
            id
            name
            key
            issues(first: $first, after: $after, orderBy: updatedAt) {
              nodes {
                id
                identifier
                title
                description
                updatedAt
                completedAt
                canceledAt
                state { id name type }
                assignee { id name }
                project { id name }
                labels(first: 20) {
                  nodes { name }
                  pageInfo { hasNextPage }
                }
                comments(first: 20, orderBy: updatedAt) {
                  nodes { id body createdAt updatedAt }
                  pageInfo { hasNextPage }
                }
                inverseRelations(first: 20) {
                  nodes {
                    type
                    issue { id identifier }
                  }
                  pageInfo { hasNextPage }
                }
              }
              pageInfo { hasNextPage endCursor }
            }
          }
        }
        """
        issues: list[dict[str, Any]] = []
        cursor: str | None = None
        team_value: dict[str, Any] = {}
        while len(issues) < max_issues:
            page_size = min(25, max_issues - len(issues))
            data = self.execute(
                query,
                {"teamId": team_id, "first": page_size, "after": cursor},
            )
            team_value = data.get("team") or {}
            connection = team_value.get("issues") or {}
            nodes = connection.get("nodes") or []
            issues.extend(normalize_live_issue(node) for node in nodes)
            page_info = connection.get("pageInfo") or {}
            if not page_info.get("hasNextPage"):
                break
            cursor = page_info.get("endCursor")
            if not cursor:
                raise IntakeError("Linear pagination reported another page without a cursor")
        issue_pagination = bool(page_info.get("hasNextPage")) if "page_info" in locals() else False
        nested_partial = nested_partial_connections(issues)
        reasons: list[str] = []
        if issue_pagination:
            reasons.append("max_issues reached before team scan completed")
        if nested_partial:
            reasons.append("nested connection limit reached: " + ", ".join(nested_partial))
        return {
            "schema_version": 1,
            "source": "linear-live",
            "team": {
                "id": team_value.get("id", team_id),
                "name": team_value.get("name", ""),
                "key": team_value.get("key", ""),
            },
            "issues": issues,
            "partial": bool(reasons),
            "partial_reason": "; ".join(reasons) if reasons else None,
        }

    def fetch_scoped_snapshot(
        self,
        team_id: str,
        max_issues: int,
        projects: list[str],
        project_prefixes: list[str],
        include_issues: list[str],
    ) -> dict[str, Any]:
        catalog_query = """
        query IntakeProjects($teamId: String!, $first: Int!, $after: String) {
          team(id: $teamId) {
            id
            name
            key
            projects(first: $first, after: $after, includeArchived: true, orderBy: updatedAt) {
              nodes { id name }
              pageInfo { hasNextPage endCursor }
            }
          }
        }
        """
        catalog: list[dict[str, Any]] = []
        cursor: str | None = None
        team_value: dict[str, Any] = {}
        catalog_partial = False
        while len(catalog) < 250:
            data = self.execute(
                catalog_query,
                {"teamId": team_id, "first": 50, "after": cursor},
            )
            team_value = data.get("team") or {}
            connection = team_value.get("projects") or {}
            catalog.extend(connection.get("nodes") or [])
            page_info = connection.get("pageInfo") or {}
            if not page_info.get("hasNextPage"):
                break
            cursor = page_info.get("endCursor")
            if not cursor:
                raise IntakeError("Linear project pagination has no cursor")
        else:
            catalog_partial = True

        exact = set(projects)
        prefixes = tuple(project_prefixes)
        matched = [
            project
            for project in catalog
            if project.get("name") in exact
            or bool(prefixes and str(project.get("name") or "").startswith(prefixes))
        ]
        ordered_projects = sorted(
            [project for project in matched if project.get("name") in exact],
            key=lambda item: str(item.get("name") or ""),
        ) + sorted(
            [project for project in matched if project.get("name") not in exact],
            key=lambda item: str(item.get("name") or ""),
            reverse=True,
        )
        missing_exact = sorted(exact - {str(project.get("name")) for project in matched})
        scope_errors: list[str] = []
        if missing_exact:
            scope_errors.append("Configured project(s) not found: " + ", ".join(missing_exact))
        if prefixes and not any(
            str(project.get("name") or "").startswith(prefixes) for project in matched
        ):
            scope_errors.append("No project matched project_name_prefixes")

        issues_by_id: dict[str, dict[str, Any]] = {}
        truncated = catalog_partial
        for identifier in include_issues:
            if len(issues_by_id) >= max_issues:
                truncated = True
                break
            issue = self._fetch_single_issue(identifier)
            if issue:
                issue_team = issue.get("team") or {}
                if issue_team.get("id") != team_id:
                    scope_errors.append(f"Explicit issue is outside configured team: {identifier}")
                else:
                    issues_by_id[str(issue.get("id"))] = issue
            else:
                scope_errors.append(f"Explicit issue not found: {identifier}")

        for project in ordered_projects:
            remaining = max_issues - len(issues_by_id)
            if remaining <= 0:
                truncated = True
                break
            project_issues, has_more = self._fetch_project_issues(
                str(project["id"]), remaining
            )
            for issue in project_issues:
                issues_by_id[str(issue.get("id"))] = issue
            if has_more:
                truncated = True
                break

        reasons = list(scope_errors)
        if catalog_partial:
            reasons.append("project catalog exceeded 250 entries")
        if truncated:
            reasons.append("max_issues reached before scoped scan completed")
        nested_partial = nested_partial_connections(list(issues_by_id.values()))
        if nested_partial:
            reasons.append("nested connection limit reached: " + ", ".join(nested_partial))
        return {
            "schema_version": 1,
            "source": "linear-live",
            "team": {
                "id": team_value.get("id", team_id),
                "name": team_value.get("name", ""),
                "key": team_value.get("key", ""),
            },
            "resolved_projects": [
                {"id": project.get("id"), "name": project.get("name")}
                for project in ordered_projects
            ],
            "issues": sorted(
                issues_by_id.values(), key=lambda item: str(item.get("identifier") or "")
            ),
            "partial": bool(reasons),
            "partial_reason": "; ".join(reasons) if reasons else None,
        }

    def _fetch_project_issues(
        self, project_id: str, limit: int
    ) -> tuple[list[dict[str, Any]], bool]:
        query = """
        query ProjectIntakeIssues($projectId: String!, $first: Int!, $after: String) {
          project(id: $projectId) {
            issues(first: $first, after: $after, includeArchived: true, orderBy: updatedAt) {
              nodes {
                id
                identifier
                title
                description
                updatedAt
                completedAt
                canceledAt
                state { id name type }
                assignee { id name }
                project { id name }
                labels(first: 20) {
                  nodes { name }
                  pageInfo { hasNextPage }
                }
                comments(first: 20, orderBy: updatedAt) {
                  nodes { id body createdAt updatedAt }
                  pageInfo { hasNextPage }
                }
                inverseRelations(first: 20) {
                  nodes { type issue { id identifier } }
                  pageInfo { hasNextPage }
                }
              }
              pageInfo { hasNextPage endCursor }
            }
          }
        }
        """
        issues: list[dict[str, Any]] = []
        cursor: str | None = None
        has_more = False
        while len(issues) < limit:
            data = self.execute(
                query,
                {
                    "projectId": project_id,
                    "first": min(25, limit - len(issues)),
                    "after": cursor,
                },
            )
            project = data.get("project") or {}
            connection = project.get("issues") or {}
            issues.extend(normalize_live_issue(node) for node in connection.get("nodes") or [])
            page_info = connection.get("pageInfo") or {}
            has_more = bool(page_info.get("hasNextPage"))
            if not has_more:
                break
            cursor = page_info.get("endCursor")
            if not cursor:
                raise IntakeError("Linear issue pagination has no cursor")
        return issues, has_more

    def _fetch_single_issue(self, identifier: str) -> dict[str, Any] | None:
        query = """
        query ExplicitIntakeIssue($id: String!) {
          issue(id: $id) {
            id
            identifier
            title
            description
            updatedAt
            completedAt
            canceledAt
            state { id name type }
            assignee { id name }
            team { id name key }
            project { id name }
            labels(first: 20) {
              nodes { name }
              pageInfo { hasNextPage }
            }
            comments(first: 20, orderBy: updatedAt) {
              nodes { id body createdAt updatedAt }
              pageInfo { hasNextPage }
            }
            inverseRelations(first: 20) {
              nodes { type issue { id identifier } }
              pageInfo { hasNextPage }
            }
          }
        }
        """
        data = self.execute(query, {"id": identifier})
        issue = data.get("issue")
        return normalize_live_issue(issue) if issue else None

    def apply_action(self, action: dict[str, Any]) -> str | None:
        operation = action["operation"]
        target_id = action.get("target_id")
        payload = action.get("payload") or {}
        if operation == "comment_create":
            data = self.execute(
                """
                mutation CommentCreate($input: CommentCreateInput!) {
                  commentCreate(input: $input) { success comment { id } }
                }
                """,
                {"input": {"issueId": target_id, "body": payload["body"]}},
            )
            result = data.get("commentCreate") or {}
            if not result.get("success"):
                raise IntakeError("Linear commentCreate returned success=false")
            return (result.get("comment") or {}).get("id")
        if operation == "issue_update":
            data = self.execute(
                """
                mutation IssueUpdate($id: String!, $input: IssueUpdateInput!) {
                  issueUpdate(id: $id, input: $input) { success issue { id } }
                }
                """,
                {"id": target_id, "input": payload},
            )
            result = data.get("issueUpdate") or {}
            if not result.get("success"):
                raise IntakeError("Linear issueUpdate returned success=false")
            return (result.get("issue") or {}).get("id")
        if operation == "issue_create":
            data = self.execute(
                """
                mutation IssueCreate($input: IssueCreateInput!) {
                  issueCreate(input: $input) { success issue { id } }
                }
                """,
                {"input": payload},
            )
            result = data.get("issueCreate") or {}
            if not result.get("success"):
                raise IntakeError("Linear issueCreate returned success=false")
            return (result.get("issue") or {}).get("id")
        raise IntakeError(f"Unsupported operation: {operation}")


def normalize_live_issue(node: dict[str, Any]) -> dict[str, Any]:
    label_connection = node.get("labels") or {}
    comment_connection = node.get("comments") or {}
    relation_connection = node.get("inverseRelations") or {}
    labels = label_connection.get("nodes") or []
    comments = comment_connection.get("nodes") or []
    inverse_relations = relation_connection.get("nodes") or []
    partial_connections = [
        name
        for name, connection in [
            ("labels", label_connection),
            ("comments", comment_connection),
            ("inverseRelations", relation_connection),
        ]
        if (connection.get("pageInfo") or {}).get("hasNextPage")
    ]
    return {
        "id": node.get("id"),
        "identifier": node.get("identifier"),
        "title": node.get("title", ""),
        "description": node.get("description") or "",
        "status": (node.get("state") or {}).get("name", ""),
        "status_type": (node.get("state") or {}).get("type", ""),
        "assignee": node.get("assignee"),
        "team": node.get("team"),
        "project": node.get("project"),
        "labels": [item.get("name") for item in labels if item.get("name")],
        "updated_at": node.get("updatedAt"),
        "completed_at": node.get("completedAt"),
        "canceled_at": node.get("canceledAt"),
        "blocked_by": [
            relation.get("issue")
            for relation in inverse_relations
            if relation.get("type") == "blocks" and relation.get("issue")
        ],
        "comments": [
            {
                "id": item.get("id"),
                "body": item.get("body") or "",
                "created_at": item.get("createdAt"),
                "updated_at": item.get("updatedAt"),
            }
            for item in comments
        ],
        "_partial_connections": partial_connections,
    }


def nested_partial_connections(issues: list[dict[str, Any]]) -> list[str]:
    return sorted(
        {
            f"{issue.get('identifier', 'unknown')}.{connection}"
            for issue in issues
            for connection in issue.get("_partial_connections", [])
        }
    )


def load_live_snapshot(config: dict[str, Any]) -> dict[str, Any]:
    env_name = config.get("auth", {}).get("token_env", "LINEAR_API_KEY")
    token = os.environ.get(env_name)
    if not token:
        raise IntakeError(
            f"Missing live credential / 缺少实时凭证: environment variable {env_name}"
        )
    team_id = config["team"].get("id")
    if not team_id or str(team_id).startswith("REPLACE_WITH_"):
        raise IntakeError("config.team.id is required for live Linear scans")
    client = LinearClient(
        token=token,
        auth_type=config.get("auth", {}).get("type", "personal_api_key"),
        endpoint=config.get("auth", {}).get("endpoint", API_URL),
        retries=config.get("retry", {}).get("max_retries", 2),
        timeout=config.get("retry", {}).get("timeout_seconds", 20),
    )
    projects = list(config.get("projects", []))
    prefixes = list(config.get("project_name_prefixes", []))
    include_issues = list(config.get("include_issues", []))
    if projects or prefixes or include_issues:
        return client.fetch_scoped_snapshot(
            team_id,
            config.get("max_issues", 50),
            projects,
            prefixes,
            include_issues,
        )
    return client.fetch_snapshot(team_id, config.get("max_issues", 50))


def project_name(issue: dict[str, Any]) -> str:
    project = issue.get("project")
    if isinstance(project, dict):
        return str(project.get("name") or "")
    return str(project or "")


def assignee_name(issue: dict[str, Any]) -> str | None:
    assignee = issue.get("assignee")
    if isinstance(assignee, dict):
        return assignee.get("name") or assignee.get("id")
    return str(assignee) if assignee else None


def is_recent(value: str | None, cutoff: datetime) -> bool:
    parsed = parse_time(value)
    return bool(parsed and parsed >= cutoff)


def latest_recent_comment(
    issue: dict[str, Any], cutoff: datetime
) -> dict[str, Any] | None:
    terminal_time = parse_time(issue.get("completed_at") or issue.get("canceled_at"))
    comments: list[dict[str, Any]] = []
    for comment in issue.get("comments", []):
        body = str(comment.get("body") or "")
        if "<!-- linear-intake:" in body:
            continue
        timestamp = parse_time(comment.get("updated_at") or comment.get("created_at"))
        if not timestamp or timestamp < cutoff:
            continue
        if terminal_time and timestamp <= terminal_time:
            continue
        comments.append(comment)
    if not comments:
        return None
    return max(
        comments,
        key=lambda value: value.get("updated_at") or value.get("created_at") or "",
    )


def in_scope(issue: dict[str, Any], config: dict[str, Any], cutoff: datetime) -> bool:
    identifier = issue.get("identifier")
    if identifier in set(config.get("include_issues", [])):
        return True
    if identifier in set(config.get("exclude_issues", [])):
        return False
    name = project_name(issue)
    exact = set(config.get("projects", []))
    prefixes = tuple(config.get("project_name_prefixes", []))
    project_match = not exact and not prefixes
    project_match = project_match or name in exact or bool(prefixes and name.startswith(prefixes))
    if not project_match:
        return False
    status = str(issue.get("status") or "").lower()
    active = {value.lower() for value in config.get("active_statuses", [])}
    if status in active:
        return True
    if status == "backlog" and is_recent(issue.get("updated_at"), cutoff):
        return True
    if status in {"done", "completed", "canceled", "cancelled"}:
        return latest_recent_comment(issue, cutoff) is not None
    return is_recent(issue.get("updated_at"), cutoff)


def readiness_gaps(issue: dict[str, Any]) -> list[str]:
    description = str(issue.get("description") or "")
    title = str(issue.get("title") or "")
    if DECISION_RE.search(title + "\n" + description):
        return ["Decision requires human resolution / Decision 需要人类确认"]
    gaps: list[str] = []
    if not FEATURE_ID_RE.search(title + "\n" + description):
        gaps.append("Feature ID missing / 缺少 Feature ID")
    if not TARGET_VERSION_RE.search(description):
        gaps.append("Target Version missing / 缺少目标版本")
    if not ACCEPTANCE_RE.search(description):
        gaps.append("Acceptance Criteria missing / 缺少验收标准")
    blocked_by = issue.get("blocked_by") or []
    if blocked_by:
        rendered = ", ".join(
            value.get("identifier", value.get("id", "unknown"))
            if isinstance(value, dict)
            else str(value)
            for value in blocked_by
        )
        gaps.append(f"Blocked by {rendered} / 被 {rendered} 阻塞")
    return gaps


def issue_target_version(issue: dict[str, Any]) -> str | None:
    match = TARGET_VERSION_RE.search(str(issue.get("description") or ""))
    return match.group(1) if match else None


def classify_feedback(issue: dict[str, Any], comment: dict[str, Any] | None) -> str:
    if not comment:
        return "none"
    body = str(comment.get("body") or "").lower()
    target = (issue_target_version(issue) or "").lower()
    version_mentions = {value.lower() for value in re.findall(r"v\d+\.\d+(?:\.\d+)?", body)}
    if (
        any(term in body for term in ["next version", "next-version", "下个版本", "下一版本", "carry-over", "revalidation", "重新验证"])
        or (version_mentions and target and target not in version_mentions)
    ):
        return "carry_over_revalidation"
    if any(term in body for term in ["backlog", "以后再做", "暂不排期"]):
        return "backlog"
    if any(term in body for term in ["duplicate", "重复"]):
        return "duplicate_candidate"
    if any(term in body for term in ["need decision", "please confirm", "需要决定", "请确认", "是否应该", "?"]):
        return "decision_needed"
    status = str(issue.get("status") or "").lower()
    if any(term in body for term in ["uat fail", "failed", "review rework", "需要修改", "验收失败", "改一波"]):
        return "review_rework"
    if any(term in body for term in ["bug", "fix", "broken", "修复", "有问题", "错误"]):
        return "current_fix" if status not in {"done", "completed"} else "decision_needed"
    return "context_only" if status not in {"done", "completed"} else "decision_needed"


def route_issue(
    issue: dict[str, Any], cutoff: datetime
) -> tuple[str, list[str], str]:
    status = str(issue.get("status") or "").lower()
    assigned = bool(assignee_name(issue))
    comment = latest_recent_comment(issue, cutoff)
    feedback = classify_feedback(issue, comment)
    if status == "todo":
        if assigned:
            return "human_queue", [], feedback
        gaps = readiness_gaps(issue)
        if gaps:
            return "blocked_ambiguous", gaps, feedback
        return "codex_queue", [], feedback
    if status in {"in progress", "started"}:
        return ("human_active" if assigned else "codex_active"), [], feedback
    if status in {"in review", "review"}:
        return ("review_queue" if assigned else "inconsistent"), [], feedback
    if status in {"done", "completed", "canceled", "cancelled"}:
        if comment:
            return "closed_watch", [], feedback
        return "done_closed", [], feedback
    if status == "backlog":
        return "blocked_ambiguous", ["Backlog is not scheduled / Backlog 尚未排期"], feedback
    return "blocked_ambiguous", [f"Unknown status: {issue.get('status')}"], feedback


def make_comment_action(
    issue: dict[str, Any], reason: str, body: str, facts: dict[str, Any]
) -> dict[str, Any]:
    basis = {
        "operation": "comment_create",
        "target_id": issue.get("id") or issue.get("identifier"),
        "reason": reason,
        "routing": {
            "identifier": issue.get("identifier"),
            "status": issue.get("status"),
            "assignee": assignee_name(issue),
        },
        "facts": facts,
    }
    key = stable_key(basis, "linear-intake")
    return {
        "idempotency_key": key,
        "operation": "comment_create",
        "target_id": basis["target_id"],
        "risk": "low",
        "reason": reason,
        "payload": {"body": f"{body}\n\n<!-- {key} -->"},
    }


def planned_actions_for(
    issue: dict[str, Any], queue: str, feedback: str, gaps: list[str], cutoff: datetime
) -> list[dict[str, Any]]:
    identifier = issue.get("identifier", "Issue")
    action: dict[str, Any] | None = None
    if queue == "inconsistent":
        action = make_comment_action(
            issue,
            "in-review-unassigned",
            f"Automation advisory / 自动化建议\n\n{identifier} is In Review but has no assignee. Assign it to the human reviewer or Owner before treating review as active.\n\n{identifier} 处于 In Review 但没有 assignee。请先 assign 给人类 reviewer 或 Owner，再把它视为正在 review。",
            {"condition": "In Review + unassigned"},
        )
    if queue == "closed_watch":
        comment = latest_recent_comment(issue, cutoff) or {}
        action = make_comment_action(
            issue,
            f"closed-watch:{feedback}",
            f"Closed-watch advisory / 已完成事项观察建议\n\nRecent feedback was classified as **{feedback}**. Keep the original completed scope closed; create or confirm a carry-over, backlog, patch, or Decision before development.\n\n近期反馈被分类为 **{feedback}**。请保持原完成范围关闭，并在开发前创建或确认 carry-over、Backlog、patch 或 Decision。",
            {
                "feedback": feedback,
                "source_comment_id": comment.get("id"),
                "source_comment_updated_at": comment.get("updated_at")
                or comment.get("created_at"),
            },
        )
    if queue == "blocked_ambiguous" and gaps and str(issue.get("status")).lower() == "todo":
        rendered = "\n".join(f"- {gap}" for gap in gaps)
        action = make_comment_action(
            issue,
            "readiness-gaps",
            f"Ready-check advisory / Ready 检查建议\n\nThis issue is not Codex-ready:\n{rendered}\n\n补齐这些信息后，再保持 Todo + unassigned 交给 Codex。",
            {
                "gaps": gaps,
                "title": issue.get("title"),
                "description_hash": hashlib.sha256(
                    str(issue.get("description") or "").encode("utf-8")
                ).hexdigest()[:16],
            },
        )
    if action is None:
        return []
    marker = f"<!-- {action['idempotency_key']} -->"
    if any(marker in str(comment.get("body") or "") for comment in issue.get("comments", [])):
        return []
    return [action]


def scan_snapshot(
    snapshot: dict[str, Any], config: dict[str, Any], as_of: datetime
) -> dict[str, Any]:
    validate_config(config)
    lookback_days = config.get("lookback_days", 7)
    cutoff = as_of - timedelta(days=lookback_days)
    queues: dict[str, list[dict[str, Any]]] = {name: [] for name in QUEUE_ORDER}
    skipped: list[dict[str, str]] = []
    blockers: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []
    comment_count = 0
    candidates = list(snapshot.get("issues") or [])
    for issue in candidates:
        if not in_scope(issue, config, cutoff):
            skipped.append(
                {
                    "identifier": str(issue.get("identifier") or issue.get("id") or "unknown"),
                    "reason": "Outside configured scan scope / 不在配置的扫描范围内",
                }
            )
            continue
        comment_count += len(issue.get("comments") or [])
        queue, gaps, feedback = route_issue(issue, cutoff)
        entry = {
            "id": issue.get("id"),
            "identifier": issue.get("identifier"),
            "title": issue.get("title", ""),
            "status": issue.get("status", ""),
            "assignee": assignee_name(issue),
            "project": project_name(issue),
            "feedback": feedback,
            "readiness_gaps": gaps,
        }
        queues[queue].append(entry)
        if gaps:
            blockers.append({"identifier": entry["identifier"], "reasons": gaps})
        actions.extend(planned_actions_for(issue, queue, feedback, gaps, cutoff))
    for values in queues.values():
        values.sort(key=lambda value: str(value.get("identifier") or ""))
    actions.sort(key=lambda value: value["idempotency_key"])
    scan_complete = not bool(snapshot.get("partial"))
    if not scan_complete:
        reason = str(snapshot.get("partial_reason") or "partial source data")
        blockers.insert(
            0,
            {
                "identifier": "SCAN",
                "reasons": [
                    f"Incomplete scan: {reason} / 扫描不完整：{reason}"
                ],
            },
        )
        actions = []
        next_action = "Narrow scope or raise the safe limit, then rerun dry scan. / 缩小范围或提高安全上限，然后重新 dry scan。"
    else:
        next_action = choose_next_action(queues)
    result = {
        "schema_version": 1,
        "run_id": stable_key(
            {
                "team": config["team"].get("id") or config["team"].get("name"),
                "projects": config.get("projects", []),
                "prefixes": config.get("project_name_prefixes", []),
                "as_of": as_of.isoformat(),
                "mode": "dry-run",
            },
            "linear-run",
        ),
        "generated_at": as_of.isoformat().replace("+00:00", "Z"),
        "mode": "dry-run",
        "scan_complete": scan_complete,
        "write_actions": "None. Dry run only. / 无写入，仅 dry-run。",
        "scan_scope": {
            "team": config["team"].get("name"),
            "projects": config.get("projects", []),
            "project_name_prefixes": config.get("project_name_prefixes", []),
            "active_statuses": config.get("active_statuses", []),
            "lookback_days": lookback_days,
            "include_issues": config.get("include_issues", []),
        },
        "scanned": {
            "issues": sum(len(values) for values in queues.values()),
            "comments": comment_count,
        },
        "queues": queues,
        "created": [],
        "updated": [],
        "skipped": skipped,
        "blockers": blockers,
        "planned_actions": actions,
        "next_action": next_action,
    }
    return result


def choose_next_action(queues: dict[str, list[dict[str, Any]]]) -> str:
    if queues["blocked_ambiguous"]:
        return "Resolve blockers or missing decisions before development. / 开发前先解决阻塞项或缺失 Decision。"
    if queues["inconsistent"]:
        return "Repair status/assignee inconsistencies. / 修复 status/assignee 不一致。"
    if queues["closed_watch"]:
        return "Triage closed-watch feedback without reopening old scope. / 分类旧完成事项反馈，不要重开原范围。"
    if queues["codex_active"]:
        return "Continue the existing Codex Active item. / 继续现有 Codex Active 事项。"
    if queues["codex_queue"]:
        item = queues["codex_queue"][0]["identifier"]
        return f"Interactive Codex may start {item} after confirming local context. / 交互式 Codex 确认本地上下文后可开始 {item}。"
    if queues["review_queue"] or queues["human_queue"]:
        return "Wait for the assigned human action. / 等待已指派的人类动作。"
    return "No actionable item in scope. / 当前范围没有可执行事项。"


def render_markdown(report: dict[str, Any]) -> str:
    scope = report["scan_scope"]
    lines = [
        "# Linear Intake Run / Linear 扫描结果",
        "",
        f"Run ID: `{report['run_id']}`",
        f"Generated At: `{report['generated_at']}`",
        f"Mode: `{report['mode']}`",
        f"Scan Complete: `{'Yes' if report.get('scan_complete') else 'No'}`",
        "",
        "## Scan Scope / 扫描范围",
        "",
        f"- Team: {scope.get('team') or '-'}",
        f"- Projects: {', '.join(scope.get('projects') or []) or '-'}",
        f"- Project Prefixes: {', '.join(scope.get('project_name_prefixes') or []) or '-'}",
        f"- Statuses: {', '.join(scope.get('active_statuses') or []) or '-'}",
        f"- Lookback: {scope.get('lookback_days')} days",
        f"- Explicit Issues: {', '.join(scope.get('include_issues') or []) or '-'}",
        "",
        "## Scanned / 已扫描",
        "",
        f"- Issues: {report['scanned']['issues']}",
        f"- Comments: {report['scanned']['comments']}",
        "",
    ]
    for queue in QUEUE_ORDER:
        lines.extend([f"## {QUEUE_LABELS[queue]}", ""])
        items = report["queues"][queue]
        if not items:
            lines.append("- None / 无")
        for item in items:
            assignee = item.get("assignee") or "unassigned"
            detail = f"status={item.get('status')}; assignee={assignee}; feedback={item.get('feedback')}"
            lines.append(f"- {item.get('identifier')}: {item.get('title')} ({detail})")
            for gap in item.get("readiness_gaps") or []:
                lines.append(f"  - Blocker: {gap}")
        lines.append("")
    for heading, field in [
        ("Created / 已创建", "created"),
        ("Updated / 已更新", "updated"),
        ("Skipped / 已跳过", "skipped"),
        ("Blockers / 阻塞项", "blockers"),
    ]:
        lines.extend([f"## {heading}", ""])
        values = report[field]
        if not values:
            lines.append("- None / 无")
        else:
            for value in values:
                lines.append(f"- {canonical_json(value)}")
        lines.append("")
    lines.extend(
        [
            "## Planned Linear Actions / 计划中的 Linear 动作",
            "",
            f"- Count: {len(report['planned_actions'])}",
            "- These actions were not executed. / 这些动作尚未执行。",
            "",
            "## Write Actions / 写入动作",
            "",
            f"- {report['write_actions']}",
            "",
            "## Next Action / 下一步",
            "",
            f"- {report['next_action']}",
            "",
        ]
    )
    return "\n".join(lines)


def load_ledger(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "receipts": {}}
    value = read_json(path)
    if value.get("schema_version") != 1 or not isinstance(value.get("receipts"), dict):
        raise IntakeError("Invalid run ledger schema")
    return value


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def validate_action(action: dict[str, Any], policy: dict[str, Any]) -> None:
    operation = action.get("operation")
    if operation not in SUPPORTED_OPERATIONS:
        raise IntakeError(f"Unsupported operation: {operation}")
    if operation not in set(policy.get("allowed_operations", [])):
        raise IntakeError(f"Operation is not allowlisted: {operation}")
    if not action.get("idempotency_key"):
        raise IntakeError("Every action requires idempotency_key")
    if operation != "issue_create" and not action.get("target_id"):
        raise IntakeError(f"{operation} requires target_id")
    payload = action.get("payload")
    if not isinstance(payload, dict):
        raise IntakeError("Every action requires an object payload")
    if operation == "comment_create":
        if set(payload) != {"body"} or not isinstance(payload.get("body"), str):
            raise IntakeError("comment_create payload must contain only body")
    if operation == "issue_update":
        fields = set(payload)
        if fields & FORBIDDEN_UPDATE_FIELDS:
            raise IntakeError(f"Forbidden issue_update fields: {sorted(fields & FORBIDDEN_UPDATE_FIELDS)}")
        allowed_fields = set(policy.get("allowed_update_fields", []))
        if not fields or not fields <= allowed_fields:
            raise IntakeError(f"issue_update fields are not allowlisted: {sorted(fields)}")
    if operation == "issue_create":
        unknown_fields = set(payload) - SUPPORTED_CREATE_FIELDS
        if unknown_fields:
            raise IntakeError(f"Unsupported issue_create fields: {sorted(unknown_fields)}")
        required = {"teamId", "title", "description"}
        if not required <= set(payload):
            raise IntakeError("issue_create requires teamId, title, and description")
        description = str(payload.get("description") or "")
        for phrase in ["Action Steps", "Expected Result", "执行动作", "期待结果"]:
            if phrase not in description:
                raise IntakeError(f"issue_create description missing: {phrase}")


def apply_plan(
    plan: dict[str, Any],
    config: dict[str, Any],
    client: LinearClient,
    ledger_path: Path,
    authorized: bool,
    now: Callable[[], datetime] = utc_now,
) -> dict[str, Any]:
    validate_config(config)
    policy = config.get("write_policy", {})
    runtime_env = policy.get("runtime_authorization_env", "AIPOS_LINEAR_WRITE_APPROVED")
    if not policy.get("enabled"):
        raise IntakeError("Writes are disabled in config / 配置未启用写入")
    if not authorized:
        raise IntakeError("Apply requires --authorize-writes")
    if os.environ.get(runtime_env) != "1":
        raise IntakeError(f"Runtime write authorization missing: {runtime_env}=1")
    if plan.get("scan_complete") is not True:
        raise IntakeError("Apply requires a complete dry-run scan")
    generated_at = parse_time(plan.get("generated_at"))
    if generated_at is None:
        raise IntakeError("Apply plan is missing generated_at")
    current_time = now()
    max_age = int(policy.get("max_plan_age_minutes", 60))
    age = current_time - generated_at
    if age < timedelta(minutes=-5) or age > timedelta(minutes=max_age):
        raise IntakeError(f"Apply plan is stale or future-dated; max age is {max_age} minutes")
    actions = plan.get("planned_actions") or plan.get("actions") or []
    if not isinstance(actions, list):
        raise IntakeError("Plan actions must be a list")
    keys: list[str] = []
    for action in actions:
        validate_action(action, policy)
        keys.append(action["idempotency_key"])
    if len(keys) != len(set(keys)):
        raise IntakeError("Plan contains duplicate idempotency keys")
    ledger = load_ledger(ledger_path)
    receipts = ledger["receipts"]
    outcome = {"applied": [], "skipped": [], "failed": []}
    for action in actions:
        key = action["idempotency_key"]
        existing = receipts.get(key)
        if existing and existing.get("status") == "succeeded":
            outcome["skipped"].append({"idempotency_key": key, "reason": "already-succeeded"})
            continue
        attempts = int((existing or {}).get("attempts", 0)) + 1
        receipt = {
            "operation": action["operation"],
            "target_id": action.get("target_id"),
            "status": "failed",
            "attempts": attempts,
            "updated_at": now().isoformat().replace("+00:00", "Z"),
        }
        try:
            result_id = client.apply_action(action)
            receipt["status"] = "succeeded"
            receipt["result_id"] = result_id
            outcome["applied"].append({"idempotency_key": key, "result_id": result_id})
        except IntakeError as exc:
            receipt["error_type"] = type(exc).__name__
            outcome["failed"].append({"idempotency_key": key, "error_type": type(exc).__name__})
        receipts[key] = receipt
        write_json_atomic(ledger_path, ledger)
    return outcome


def resolve_under_root(root: Path, value: str) -> Path:
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise IntakeError(f"Path escapes repository root: {value}") from exc
    return candidate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Run a dry-run intake scan")
    scan.add_argument("--config", required=True)
    scan.add_argument("--snapshot", help="Offline snapshot JSON; omit for live Linear")
    scan.add_argument("--as-of", help="ISO-8601 time for deterministic runs")
    scan.add_argument("--json-out")
    scan.add_argument("--markdown-out")

    apply = subparsers.add_parser("apply", help="Apply an explicitly authorized plan")
    apply.add_argument("--config", required=True)
    apply.add_argument("--plan", required=True)
    apply.add_argument("--authorize-writes", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    try:
        config_path = resolve_under_root(root, args.config)
        config = read_json(config_path)
        validate_config(config)
        if args.command == "scan":
            snapshot = (
                read_json(resolve_under_root(root, args.snapshot))
                if args.snapshot
                else load_live_snapshot(config)
            )
            as_of = parse_time(args.as_of) if args.as_of else utc_now()
            if as_of is None:
                raise IntakeError("Invalid --as-of time")
            report = scan_snapshot(snapshot, config, as_of)
            markdown = render_markdown(report)
            if args.json_out:
                write_json_atomic(resolve_under_root(root, args.json_out), report)
            if args.markdown_out:
                path = resolve_under_root(root, args.markdown_out)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(markdown, encoding="utf-8")
            print(markdown)
            return 0

        env_name = config.get("auth", {}).get("token_env", "LINEAR_API_KEY")
        token = os.environ.get(env_name)
        if not token:
            raise IntakeError(f"Missing live credential: {env_name}")
        client = LinearClient(
            token=token,
            auth_type=config.get("auth", {}).get("type", "personal_api_key"),
            endpoint=config.get("auth", {}).get("endpoint", API_URL),
            retries=config.get("retry", {}).get("max_retries", 2),
            timeout=config.get("retry", {}).get("timeout_seconds", 20),
        )
        plan = read_json(resolve_under_root(root, args.plan))
        ledger_path = resolve_under_root(
            root, config.get("state_file", "project-os/runtime/linear_intake_ledger.json")
        )
        outcome = apply_plan(
            plan, config, client, ledger_path, authorized=args.authorize_writes
        )
        print(json.dumps(outcome, indent=2, ensure_ascii=False))
        return 0 if not outcome["failed"] else 2
    except IntakeError as exc:
        print(f"[BLOCK] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
