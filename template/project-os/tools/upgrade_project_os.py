#!/usr/bin/env python3
"""Inspect, plan, apply, and verify guarded AI Project OS upgrades."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any


VERSION_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
ENV_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
DEFAULT_PROTECTED = [
    "LOCAL_OVERRIDES.md",
    "audit/",
    "runtime/",
    "safety/PROJECT_MEMORY_AUDIT.md",
    "safety/DOC_GAP_REGISTER.md",
    "safety/SECRET_SCAN_REPORT.md",
    "safety/PUBLICATION_MANIFEST.md",
    "discovery/PROJECT_MAP.md",
    "discovery/DEPENDENCY_MAP.md",
    "discovery/DOCUMENT_INVENTORY.md",
    "discovery/SETTINGS_AND_DATA_REGISTER.md",
    "discovery/LOGIC_BOUNDARY_AUDIT.md",
    "discovery/WHITEBOX_IMPORT_REPORT.md",
    "discovery/SCAN_EVIDENCE.json",
    "safety/SAFETY_EVIDENCE.json",
]
SKIPPED_NAMES = {".DS_Store"}
SKIPPED_PARTS = {"__pycache__"}


class UpgradeError(RuntimeError):
    """A safe user-facing upgrade failure."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str
    ) -> None:
        raise urllib.error.HTTPError(req.full_url, code, msg, headers, fp)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def tree_digest(tree: dict[str, bytes]) -> str:
    index = [{"path": path, "sha256": sha256_bytes(tree[path])} for path in sorted(tree)]
    return sha256_bytes(canonical_json(index).encode("utf-8"))


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise UpgradeError(f"File not found / 文件不存在: {path}") from exc
    except json.JSONDecodeError as exc:
        raise UpgradeError(f"Invalid JSON / JSON 无效: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise UpgradeError(f"Expected JSON object / 需要 JSON object: {path}")
    return value


def resolve_under_root(root: Path, value: str) -> Path:
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise UpgradeError(f"Path escapes repository root: {value}") from exc
    return candidate


def normalized_relative(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise UpgradeError(f"Unsafe relative path: {value}")
    return path.as_posix()


def parse_version(value: str) -> tuple[int, int, int]:
    match = VERSION_RE.match(value)
    if not match:
        raise UpgradeError(f"Invalid semantic version: {value}")
    return tuple(int(item) for item in match.groups())


def parse_time(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise UpgradeError(f"Invalid ISO-8601 time: {value}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def os_version_from_bytes(value: bytes) -> str:
    text = value.decode("utf-8", errors="strict")
    match = re.search(r"^Installed OS Version:\s*(v\d+\.\d+\.\d+)\s*$", text, re.MULTILINE)
    if not match:
        raise UpgradeError("OS_VERSION.md does not contain a valid Installed OS Version")
    parse_version(match.group(1))
    return match.group(1)


def load_directory_tree(path: Path) -> dict[str, bytes]:
    if not path.is_dir():
        raise UpgradeError(f"OS directory not found: {path}")
    tree: dict[str, bytes] = {}
    for candidate in sorted(path.rglob("*")):
        relative = candidate.relative_to(path)
        if candidate.name in SKIPPED_NAMES or any(part in SKIPPED_PARTS for part in relative.parts):
            continue
        if candidate.is_symlink():
            raise UpgradeError(f"Symlinks are not supported in OS sources: {relative.as_posix()}")
        if candidate.is_dir():
            continue
        if not candidate.is_file():
            raise UpgradeError(f"Unsupported OS source entry: {relative.as_posix()}")
        tree[normalized_relative(relative.as_posix())] = candidate.read_bytes()
    if "OS_VERSION.md" not in tree:
        raise UpgradeError("OS source is missing OS_VERSION.md")
    return tree


def load_zip_tree(path: Path) -> dict[str, bytes]:
    if not path.is_file():
        raise UpgradeError(f"OS zip not found: {path}")
    tree: dict[str, bytes] = {}
    try:
        with zipfile.ZipFile(path) as archive:
            for info in sorted(archive.infolist(), key=lambda item: item.filename):
                if info.is_dir():
                    continue
                pure = PurePosixPath(info.filename)
                if pure.is_absolute() or ".." in pure.parts:
                    raise UpgradeError(f"Unsafe zip entry: {info.filename}")
                if not pure.parts or pure.parts[0] != "project-os" or len(pure.parts) < 2:
                    raise UpgradeError(f"Zip entry must stay under project-os/: {info.filename}")
                mode = (info.external_attr >> 16) & 0o170000
                if mode == 0o120000:
                    raise UpgradeError(f"Zip symlink is not supported: {info.filename}")
                relative = normalized_relative(PurePosixPath(*pure.parts[1:]).as_posix())
                if PurePosixPath(relative).name in SKIPPED_NAMES or any(
                    part in SKIPPED_PARTS for part in PurePosixPath(relative).parts
                ):
                    continue
                if relative in tree:
                    raise UpgradeError(f"Duplicate zip path: {relative}")
                tree[relative] = archive.read(info)
    except zipfile.BadZipFile as exc:
        raise UpgradeError(f"Invalid OS zip: {path}") from exc
    if "OS_VERSION.md" not in tree:
        raise UpgradeError("OS zip is missing project-os/OS_VERSION.md")
    return tree


def load_tree(root: Path, descriptor: dict[str, Any]) -> dict[str, bytes]:
    source_type = descriptor.get("type")
    source_path = descriptor.get("path")
    if source_type not in {"directory", "zip"}:
        raise UpgradeError("A file upgrade plan requires source.type=directory or zip")
    if not isinstance(source_path, str) or not source_path:
        raise UpgradeError("source.path is required")
    path = resolve_under_root(root, source_path)
    return load_directory_tree(path) if source_type == "directory" else load_zip_tree(path)


def github_release_metadata(source: dict[str, Any]) -> dict[str, Any]:
    repository = source.get("repository")
    if not isinstance(repository, str) or not REPOSITORY_RE.match(repository):
        raise UpgradeError("source.repository must use owner/name")
    url = f"https://api.github.com/repos/{repository}/releases/latest"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ai-project-os-upgrade"}
    token_env = source.get("token_env", "GITHUB_TOKEN")
    if not isinstance(token_env, str) or not ENV_RE.match(token_env):
        raise UpgradeError("source.token_env must be a valid environment variable name")
    token = os.environ.get(token_env)
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers, method="GET")
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise UpgradeError(f"Cannot read GitHub Release metadata: {exc}") from exc
    if not isinstance(payload, dict):
        raise UpgradeError("GitHub Release metadata must be an object")
    tag = payload.get("tag_name")
    if not isinstance(tag, str):
        raise UpgradeError("GitHub Release metadata is missing tag_name")
    assets = []
    for asset in payload.get("assets") or []:
        if not isinstance(asset, dict):
            continue
        assets.append(
            {
                "name": asset.get("name"),
                "size": asset.get("size"),
                "digest": asset.get("digest"),
                "url": asset.get("browser_download_url"),
            }
        )
    return {
        "version": tag,
        "source": f"github:{repository}",
        "release_url": payload.get("html_url"),
        "assets": assets,
    }


def source_metadata(root: Path, source: dict[str, Any]) -> dict[str, Any]:
    source_type = source.get("type")
    if source_type in {"directory", "zip"}:
        tree = load_tree(root, source)
        return {
            "version": os_version_from_bytes(tree["OS_VERSION.md"]),
            "source": f"{source_type}:{source.get('path')}",
            "tree_digest": tree_digest(tree),
            "files": len(tree),
        }
    if source_type == "metadata_json":
        path = source.get("path")
        if not isinstance(path, str):
            raise UpgradeError("source.path is required")
        metadata = read_json(resolve_under_root(root, path))
        version = metadata.get("version") or metadata.get("tag_name")
        if not isinstance(version, str):
            raise UpgradeError("metadata source is missing version/tag_name")
        return {"version": version, "source": f"metadata:{path}"}
    if source_type == "github_release":
        return github_release_metadata(source)
    raise UpgradeError("source.type must be directory, zip, metadata_json, or github_release")


def validate_config(config: dict[str, Any]) -> None:
    if config.get("schema_version") != 1:
        raise UpgradeError("config.schema_version must be 1")
    installed_path = config.get("installed_path", "project-os")
    if not isinstance(installed_path, str) or not installed_path:
        raise UpgradeError("config.installed_path must be a non-empty path")
    if not isinstance(config.get("source"), dict):
        raise UpgradeError("config.source must be an object")
    if not isinstance(config.get("allow_downgrade", False), bool):
        raise UpgradeError("config.allow_downgrade must be boolean")
    policy = config.get("apply_policy", {})
    if not isinstance(policy, dict):
        raise UpgradeError("config.apply_policy must be an object")
    max_age = policy.get("max_plan_age_minutes", 60)
    if type(max_age) is not int or not 1 <= max_age <= 1440:
        raise UpgradeError("apply_policy.max_plan_age_minutes must be between 1 and 1440")
    env = policy.get("authorization_env", "AIPOS_OS_UPGRADE_APPROVED")
    if not isinstance(env, str) or not ENV_RE.match(env):
        raise UpgradeError("apply_policy.authorization_env must be a valid environment variable")
    branch_prefix = policy.get("branch_prefix", "codex/upgrade-")
    if not isinstance(branch_prefix, str) or not branch_prefix:
        raise UpgradeError("apply_policy.branch_prefix must be non-empty")


def inspect_upgrade(config: dict[str, Any], root: Path) -> dict[str, Any]:
    validate_config(config)
    installed = load_directory_tree(resolve_under_root(root, config.get("installed_path", "project-os")))
    installed_version = os_version_from_bytes(installed["OS_VERSION.md"])
    available = source_metadata(root, config["source"])
    available_version = available.get("version")
    if not isinstance(available_version, str):
        raise UpgradeError("Available version is missing")
    installed_tuple = parse_version(installed_version)
    available_tuple = parse_version(available_version)
    blockers: list[str] = []
    if available_tuple < installed_tuple and not config.get("allow_downgrade", False):
        blockers.append("Downgrade requires explicit allow_downgrade=true / 降级需要明确授权")
    relation = (
        "upgrade"
        if available_tuple > installed_tuple
        else "same"
        if available_tuple == installed_tuple
        else "downgrade"
    )
    return {
        "schema_version": 1,
        "installed_version": installed_version,
        "available_version": available_version,
        "relation": relation,
        "compatible": not blockers,
        "source": available.get("source"),
        "source_evidence": {
            key: value
            for key, value in available.items()
            if key not in {"version", "source"}
        },
        "blockers": blockers,
        "next_action": (
            "Generate a three-way upgrade plan. / 生成三方升级计划。"
            if not blockers and relation == "upgrade"
            else "No upgrade is required. / 不需要升级。"
            if not blockers and relation == "same"
            else "Review blockers and policy before planning. / 规划前先处理阻塞与策略。"
        ),
    }


def is_protected(path: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if pattern.endswith("/") and path.startswith(pattern):
            return True
        if path == pattern:
            return True
    return False


def version_migration(installed: bytes, target: bytes, target_version: str) -> bytes:
    installed_text = installed.decode("utf-8")
    target_text = target.decode("utf-8")
    preserved: dict[str, str] = {}
    for field in ["Installed Date", "Local Customizations"]:
        match = re.search(rf"^{re.escape(field)}:\s*(.*)$", installed_text, re.MULTILINE)
        if match:
            preserved[field] = match.group(1)
    target_text = re.sub(
        r"^Installed OS Version:\s*.*$",
        f"Installed OS Version: {target_version}",
        target_text,
        flags=re.MULTILINE,
    )
    for field, value in preserved.items():
        target_text = re.sub(
            rf"^{re.escape(field)}:\s*.*$",
            f"{field}: {value}",
            target_text,
            flags=re.MULTILINE,
        )
    target_text = re.sub(
        r"^Last Upgrade:\s*.*$",
        f"Last Upgrade: Upgraded to {target_version} via guarded migration",
        target_text,
        flags=re.MULTILINE,
    )
    return target_text.encode("utf-8")


def planned_bytes(path: str, installed: bytes | None, target: bytes, target_version: str) -> bytes:
    if path == "OS_VERSION.md" and installed is not None:
        return version_migration(installed, target, target_version)
    return target


def build_plan(config: dict[str, Any], root: Path) -> dict[str, Any]:
    inspection = inspect_upgrade(config, root)
    if inspection["blockers"]:
        raise UpgradeError("; ".join(inspection["blockers"]))
    source = config["source"]
    if source.get("type") not in {"directory", "zip"}:
        raise UpgradeError("Planning requires a directory or zip source after metadata inspection")
    installed_path = config.get("installed_path", "project-os")
    installed = load_directory_tree(resolve_under_root(root, installed_path))
    target = load_tree(root, source)
    base_descriptor = config.get("base")
    base = load_tree(root, base_descriptor) if isinstance(base_descriptor, dict) else {}
    target_version = inspection["available_version"]
    patterns = list(DEFAULT_PROTECTED)
    extra = config.get("protected_paths", [])
    if not isinstance(extra, list) or not all(isinstance(item, str) and item for item in extra):
        raise UpgradeError("protected_paths must be an array of non-empty strings")
    patterns.extend(extra)
    actions: list[dict[str, Any]] = []
    blockers: list[str] = []
    for path in sorted(set(installed) | set(target) | set(base)):
        current = installed.get(path)
        desired_source = target.get(path)
        old = base.get(path)
        protected = is_protected(path, patterns)
        action = "identical"
        reason = "Installed and target files are identical."
        desired: bytes | None = desired_source
        if desired_source is None:
            action = "preserve" if protected else "remove_candidate"
            reason = (
                "Protected/project-specific file is absent upstream and remains untouched."
                if protected
                else "Installed-only file requires human removal review."
            )
            desired = current
        elif current is None:
            action = "add"
            reason = "File exists only in the target source."
        elif path == "OS_VERSION.md" and current != desired_source:
            action = "migrate"
            reason = "Update OS metadata while preserving installed date and local customization fields."
            desired = planned_bytes(path, current, desired_source, target_version)
        elif current == desired_source:
            action = "identical"
            reason = "Installed and target files are identical."
        elif protected:
            action = "preserve"
            reason = "Protected project memory or human disposition is never overwritten automatically."
            desired = current
        elif old is None:
            action = "conflict"
            reason = "No trusted base exists for two different file versions."
        elif current == old and desired_source != old:
            action = "safe_update"
            reason = "Only the upstream target changed from the trusted base."
        elif desired_source == old and current != old:
            action = "preserve"
            reason = "Only the installed project changed from the trusted base."
            desired = current
        elif current != old and desired_source != old:
            action = "conflict"
            reason = "Installed project and upstream target both changed from the trusted base."
        else:
            action = "conflict"
            reason = "File state is ambiguous and requires human review."
        if action == "conflict":
            blockers.append(f"Conflict requires human decision: {path}")
        actions.append(
            {
                "path": path,
                "action": action,
                "protected": protected,
                "installed_sha256": sha256_bytes(current) if current is not None else None,
                "base_sha256": sha256_bytes(old) if old is not None else None,
                "target_sha256": sha256_bytes(desired_source) if desired_source is not None else None,
                "planned_sha256": sha256_bytes(desired) if desired is not None else None,
                "reason": reason,
            }
        )
    apply_policy = config.get("apply_policy", {})
    created_at = config.get("as_of")
    if not isinstance(created_at, str):
        raise UpgradeError("config.as_of is required for a deterministic, freshness-checkable plan")
    parse_time(created_at)
    plan: dict[str, Any] = {
        "schema_version": 1,
        "status": "READY" if not blockers else "BLOCKED",
        "created_at": created_at,
        "installed_path": installed_path,
        "installed_version": inspection["installed_version"],
        "target_version": target_version,
        "source": source,
        "base": base_descriptor,
        "source_digest": tree_digest(target),
        "installed_digest": tree_digest(installed),
        "protected_paths": patterns,
        "apply_policy": {
            "max_plan_age_minutes": apply_policy.get("max_plan_age_minutes", 60),
            "authorization_env": apply_policy.get(
                "authorization_env", "AIPOS_OS_UPGRADE_APPROVED"
            ),
            "branch_prefix": apply_policy.get("branch_prefix", "codex/upgrade-"),
        },
        "actions": actions,
        "blockers": blockers,
        "validation": [
            "Run strict AI Project OS validator.",
            "Run the complete project-os tool test suite.",
            "Run the target publication-profile safety gate.",
            "Run project-specific human UAT before accepting the upgrade."
        ],
        "rollback": {
            "strategy": "Abandon or revert the upgrade branch after human review; never rewrite shared history automatically.",
            "preserve": patterns,
            "automatic": False,
        },
    }
    plan["plan_id"] = "aipos-upgrade:" + sha256_bytes(
        canonical_json(plan).encode("utf-8")
    )[:24]
    return plan


def render_inspection(value: dict[str, Any]) -> str:
    lines = [
        "# OS Upgrade Inspection / OS 升级检查",
        "",
        f"Installed Version: `{value.get('installed_version', '-')}`",
        f"Available Version: `{value.get('available_version', '-')}`",
        f"Relation: `{value.get('relation', '-')}`",
        f"Compatible: `{'yes' if value.get('compatible') else 'no'}`",
        f"Source: `{value.get('source', '-')}`",
        "",
        "## Blockers / 阻塞",
        "",
    ]
    lines.extend(f"- {item}" for item in value.get("blockers") or ["None / 无"])
    lines.extend(
        [
            "",
            "## Next Action / 下一步",
            "",
            f"- {value.get('next_action', '-')}",
            "",
            "Inspection is read-only and never stores credential values. / 检查只读，绝不保存凭证值。",
            "",
        ]
    )
    return "\n".join(lines)


def render_plan(plan: dict[str, Any]) -> str:
    counts: dict[str, int] = {}
    for action in plan.get("actions") or []:
        name = action.get("action", "unknown")
        counts[name] = counts.get(name, 0) + 1
    lines = [
        "# OS Upgrade Plan / OS 升级计划",
        "",
        f"Plan ID: `{plan.get('plan_id', '-')}`",
        f"Status: `{plan.get('status', '-')}`",
        f"Current Version: `{plan.get('installed_version', '-')}`",
        f"Target Version: `{plan.get('target_version', '-')}`",
        f"Created At: `{plan.get('created_at', '-')}`",
        "",
        "## Summary / 摘要",
        "",
    ]
    for name in sorted(counts):
        lines.append(f"- {name}: {counts[name]}")
    lines.extend(["", "## Blockers / 阻塞", ""])
    lines.extend(f"- {item}" for item in plan.get("blockers") or ["None / 无"])
    lines.extend(
        [
            "",
            "## Ordered Actions / 有序动作",
            "",
            "| Path | Action | Protected | Installed | Target | Planned | Reason |",
            "|---|---|---:|---|---|---|---|",
        ]
    )
    for action in plan.get("actions") or []:
        lines.append(
            "| {path} | {action} | {protected} | {installed} | {target} | {planned} | {reason} |".format(
                path=action.get("path", "-"),
                action=action.get("action", "-"),
                protected="Yes" if action.get("protected") else "No",
                installed=action.get("installed_sha256") or "-",
                target=action.get("target_sha256") or "-",
                planned=action.get("planned_sha256") or "-",
                reason=str(action.get("reason", "-")).replace("|", "\\|"),
            )
        )
    lines.extend(
        [
            "",
            "## Apply Boundary / 执行边界",
            "",
            f"- Branch prefix: `{(plan.get('apply_policy') or {}).get('branch_prefix', '-')}`",
            f"- Authorization env name: `{(plan.get('apply_policy') or {}).get('authorization_env', '-')}`",
            "- Apply also requires the CLI authorization flag and a fresh unchanged plan. / Apply 还需要 CLI 授权参数以及新鲜且未变化的计划。",
            "- Protected files are preserved; remove-candidates are never deleted automatically. / 保护文件保持不变；remove-candidate 永远不会自动删除。",
            "",
            "Reports contain hashes and classifications, not file content or secret values. / 报告只包含 hash 与分类，不包含文件正文或 secret 值。",
            "",
        ]
    )
    return "\n".join(lines)


def run_git(root: Path, args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, text=True, capture_output=True, check=False
        )
    except OSError as exc:
        raise UpgradeError(f"Cannot run Git: {exc}") from exc
    if result.returncode != 0:
        raise UpgradeError(result.stderr.strip() or "Git command failed")
    return result.stdout.strip()


def validate_apply_gate(
    plan: dict[str, Any], root: Path, authorize: bool, as_of: str
) -> None:
    if plan.get("schema_version") != 1 or plan.get("status") != "READY":
        raise UpgradeError("Only a complete READY plan can be applied")
    if not authorize:
        raise UpgradeError("Apply requires --authorize-upgrade")
    policy = plan.get("apply_policy") or {}
    env = policy.get("authorization_env", "AIPOS_OS_UPGRADE_APPROVED")
    if os.environ.get(env) != "APPROVED":
        raise UpgradeError(f"Runtime authorization requires {env}=APPROVED")
    branch = run_git(root, ["branch", "--show-current"])
    prefix = policy.get("branch_prefix", "codex/upgrade-")
    if not branch.startswith(prefix):
        raise UpgradeError(f"Upgrade apply requires a branch starting with {prefix}")
    dirty = run_git(root, ["status", "--porcelain", "--untracked-files=no"])
    allowed_dirty = {
        f"{str(plan.get('installed_path', 'project-os')).rstrip('/')}/{action.get('path')}"
        for action in plan.get("actions") or []
        if isinstance(action, dict) and action.get("action") in {"add", "safe_update", "migrate"}
    }
    for line in dirty.splitlines():
        path = line[2:].strip() if len(line) >= 3 else ""
        if " -> " in path or path not in allowed_dirty:
            raise UpgradeError(f"Unrelated tracked worktree change blocks upgrade apply: {path}")
    created = parse_time(plan.get("created_at"))
    current = parse_time(as_of)
    age = (current - created).total_seconds() / 60
    max_age = policy.get("max_plan_age_minutes", 60)
    if age < 0 or age > max_age:
        raise UpgradeError("Upgrade plan is stale or from the future")


def apply_plan(
    plan: dict[str, Any], root: Path, authorize: bool, as_of: str
) -> dict[str, Any]:
    validate_apply_gate(plan, root, authorize, as_of)
    source = plan.get("source")
    if not isinstance(source, dict):
        raise UpgradeError("Plan source is missing")
    target = load_tree(root, source)
    if tree_digest(target) != plan.get("source_digest"):
        raise UpgradeError("Upgrade source changed after plan generation")
    installed_root = resolve_under_root(root, plan.get("installed_path", "project-os"))
    results: list[dict[str, Any]] = []
    target_version = plan.get("target_version")
    if not isinstance(target_version, str):
        raise UpgradeError("Plan target_version is missing")
    for action in plan.get("actions") or []:
        if not isinstance(action, dict):
            raise UpgradeError("Plan action must be an object")
        relative = normalized_relative(str(action.get("path", "")))
        destination = (installed_root / relative).resolve()
        try:
            destination.relative_to(installed_root.resolve())
        except ValueError as exc:
            raise UpgradeError(f"Action escapes installed project-os: {relative}") from exc
        operation = action.get("action")
        current = destination.read_bytes() if destination.is_file() else None
        current_sha = sha256_bytes(current) if current is not None else None
        if operation not in {"add", "safe_update", "migrate"}:
            results.append({"path": relative, "action": operation, "status": "unchanged"})
            continue
        desired_source = target.get(relative)
        if desired_source is None:
            raise UpgradeError(f"Target source is missing planned path: {relative}")
        desired = planned_bytes(relative, current, desired_source, target_version)
        desired_sha = sha256_bytes(desired)
        if desired_sha != action.get("planned_sha256"):
            raise UpgradeError(f"Planned output changed for: {relative}")
        if current_sha == desired_sha:
            results.append({"path": relative, "action": operation, "status": "already_applied"})
            continue
        if current_sha != action.get("installed_sha256"):
            raise UpgradeError(f"Installed file changed after planning: {relative}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=destination.parent, prefix=".aipos-upgrade-", delete=False
            ) as handle:
                temporary = Path(handle.name)
                handle.write(desired)
            os.replace(temporary, destination)
            temporary = None
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        results.append({"path": relative, "action": operation, "status": "applied"})
    return {
        "schema_version": 1,
        "plan_id": plan.get("plan_id"),
        "installed_version": plan.get("installed_version"),
        "target_version": target_version,
        "status": "applied_pending_verification",
        "actions": results,
        "rollback": "Abandon or revert this upgrade branch after human review; no automatic history rewrite is performed.",
    }


def verify_plan(plan: dict[str, Any], root: Path) -> tuple[dict[str, Any], int]:
    installed_root = resolve_under_root(root, plan.get("installed_path", "project-os"))
    findings: list[str] = []
    for action in plan.get("actions") or []:
        if not isinstance(action, dict):
            continue
        if action.get("action") not in {"add", "safe_update", "migrate", "identical", "preserve"}:
            continue
        relative = normalized_relative(str(action.get("path", "")))
        path = (installed_root / relative).resolve()
        actual = sha256_bytes(path.read_bytes()) if path.is_file() else None
        expected = action.get("planned_sha256")
        if actual != expected:
            findings.append(f"Hash mismatch: {relative}")
    result = {
        "schema_version": 1,
        "plan_id": plan.get("plan_id"),
        "target_version": plan.get("target_version"),
        "status": "pass" if not findings else "fail",
        "findings": findings,
        "next_action": (
            "Run strict validator, full tests, safety gate, and human UAT."
            if not findings
            else "Stop and review the upgrade branch; follow rollback guidance."
        ),
    }
    return result, 0 if not findings else 2


def write_json(root: Path, value: str | None, content: dict[str, Any], runtime_only: bool = False) -> None:
    if not value:
        return
    path = resolve_under_root(root, value)
    if runtime_only:
        runtime = resolve_under_root(root, "project-os/runtime")
        try:
            path.relative_to(runtime)
        except ValueError as exc:
            raise UpgradeError("Apply/verify receipts must stay under project-os/runtime/") from exc
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def write_text(root: Path, value: str | None, content: str) -> None:
    if not value:
        return
    path = resolve_under_root(root, value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    subparsers = parser.add_subparsers(dest="command", required=True)
    inspect = subparsers.add_parser("inspect")
    inspect.add_argument("--config", required=True)
    inspect.add_argument("--json-output")
    inspect.add_argument("--report")
    plan = subparsers.add_parser("plan")
    plan.add_argument("--config", required=True)
    plan.add_argument("--json-output")
    plan.add_argument("--report")
    apply = subparsers.add_parser("apply")
    apply.add_argument("--plan", required=True)
    apply.add_argument("--as-of", required=True)
    apply.add_argument("--authorize-upgrade", action="store_true")
    apply.add_argument("--receipt")
    verify = subparsers.add_parser("verify")
    verify.add_argument("--plan", required=True)
    verify.add_argument("--receipt")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    try:
        if args.command in {"inspect", "plan"}:
            config = read_json(resolve_under_root(root, args.config))
            if args.command == "inspect":
                result = inspect_upgrade(config, root)
                rendered = render_inspection(result)
                code = 0 if not result["blockers"] else 2
            else:
                result = build_plan(config, root)
                rendered = render_plan(result)
                code = 0 if result["status"] == "READY" else 2
            write_json(root, args.json_output, result)
            write_text(root, args.report, rendered)
            print(rendered)
            return code
        plan = read_json(resolve_under_root(root, args.plan))
        if args.command == "apply":
            result = apply_plan(plan, root, args.authorize_upgrade, args.as_of)
            write_json(root, args.receipt, result, runtime_only=True)
            print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
            return 0
        result, code = verify_plan(plan, root)
        write_json(root, args.receipt, result, runtime_only=True)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return code
    except UpgradeError as exc:
        print(f"[BLOCK] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
