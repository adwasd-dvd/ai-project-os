#!/usr/bin/env python3
"""Generate deterministic release, recovery, and post-release evidence.

This tool is intentionally no-write with respect to GitHub, Git, Linear, and
production systems. It only validates committed-style inputs and writes the
explicit report paths requested by the operator.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


VERSION_RE = re.compile(r"^v\d+\.\d+\.\d+$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
URL_RE = re.compile(r"^https://")
FORBIDDEN_KEYS = {
    "api_key",
    "token",
    "authorization",
    "raw_payload",
    "comment_body",
    "file_content",
    "source_line",
}


class ReleaseError(RuntimeError):
    """A safe user-facing release-control error."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReleaseError(f"File not found / 文件不存在: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ReleaseError(f"Invalid JSON / JSON 无效: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReleaseError(f"Expected JSON object / 需要 JSON object: {path}")
    return value


def resolve_under_root(root: Path, value: str) -> Path:
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ReleaseError(f"Path escapes repository root: {value}") from exc
    return candidate


def existing_path(root: Path, value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        return resolve_under_root(root, value).exists()
    except ReleaseError:
        return False


def load_trace_project() -> Any:
    script = Path(__file__).with_name("trace_project.py")
    spec = importlib.util.spec_from_file_location("aipos_trace_project", script)
    if spec is None or spec.loader is None:
        raise ReleaseError("Cannot load trace_project.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contains_forbidden_key(value: Any) -> str | None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_KEYS:
                return str(key)
            found = contains_forbidden_key(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = contains_forbidden_key(child)
            if found:
                return found
    return None


def validate_release_input(
    value: dict[str, Any], root: Path
) -> tuple[list[str], list[str], dict[str, Any]]:
    findings: list[str] = []
    blockers: list[str] = []
    if value.get("schema_version") != 1:
        findings.append("schema_version must be 1")
    version = value.get("version")
    if not isinstance(version, str) or not VERSION_RE.match(version):
        findings.append("version must use vMAJOR.MINOR.PATCH")

    scope = value.get("scope")
    if not isinstance(scope, dict):
        findings.append("scope must be an object")
        scope = {}
    for field in ["included", "excluded", "deferred"]:
        entries = scope.get(field)
        if not isinstance(entries, list):
            findings.append(f"scope.{field} must be an array")
        elif field == "included" and not entries:
            findings.append("scope.included must not be empty")

    manifest_path = value.get("traceability_manifest")
    trace: dict[str, Any] = {}
    if not existing_path(root, manifest_path):
        findings.append("traceability_manifest must reference an existing path")
    else:
        trace = read_json(resolve_under_root(root, manifest_path))
        trace_findings = load_trace_project().validate_manifest(trace, root)
        findings.extend(f"traceability: {item}" for item in trace_findings)
        trace_release = trace.get("release") or {}
        if trace_release.get("version") != version:
            findings.append("traceability release version must match input version")
        if trace_release.get("status") not in {"candidate", "released"}:
            blockers.append("Traceability release state must be candidate or released")
        if trace_release.get("uat_status") != "pass":
            blockers.append("Human version UAT Pass is required")
        feature_states = {
            feature.get("state")
            for feature in trace.get("features") or []
            if isinstance(feature, dict)
        }
        if not feature_states or not feature_states <= {"accepted", "released"}:
            blockers.append("Every included feature must be accepted or released")
        included = set(scope.get("included") or [])
        traced = {
            feature.get("feature_id")
            for feature in trace.get("features") or []
            if isinstance(feature, dict)
        }
        if included != traced:
            blockers.append("scope.included must exactly match traceability features")

    impact_path = value.get("change_impact_report")
    if not existing_path(root, impact_path):
        findings.append("change_impact_report must reference an existing path")
    elif "Development Gate: `READY`" not in resolve_under_root(root, impact_path).read_text(
        encoding="utf-8"
    ):
        blockers.append("Change-impact gate must be READY")

    safety = value.get("safety")
    if not isinstance(safety, dict):
        findings.append("safety must be an object")
        safety = {}
    if safety.get("decision") != "Go":
        blockers.append("Safety publication decision must be Go")
    if safety.get("block_findings") != 0:
        blockers.append("Safety Block findings must be zero")
    review_count = safety.get("review_findings")
    if type(review_count) is not int or review_count < 0:
        findings.append("safety.review_findings must be a non-negative integer")
    elif review_count and not str(safety.get("review_disposition", "")).strip():
        blockers.append("Safety Review findings require a disposition")
    if not existing_path(root, safety.get("evidence")):
        findings.append("safety.evidence must reference an existing path")
    if not str(safety.get("profile", "")).strip() or not str(
        safety.get("destination", "")
    ).strip():
        findings.append("safety.profile and safety.destination are required")

    tests = value.get("tests")
    if not isinstance(tests, list) or not tests:
        findings.append("tests must be a non-empty array")
        tests = []
    for index, test in enumerate(tests):
        if not isinstance(test, dict):
            findings.append(f"tests[{index}] must be an object")
            continue
        if test.get("status") != "pass":
            blockers.append(f"Test {test.get('id', index)} must pass")
        if not existing_path(root, test.get("evidence")):
            findings.append(f"tests[{index}].evidence must reference an existing path")

    package = value.get("package")
    if not isinstance(package, dict):
        findings.append("package must be an object")
        package = {}
    if not str(package.get("asset", "")).endswith(".zip"):
        findings.append("package.asset must name a zip file")
    if not isinstance(package.get("sha256"), str) or not SHA256_RE.match(
        package.get("sha256", "")
    ):
        blockers.append("Package SHA-256 is missing or invalid")
    if package.get("deterministic") is not True:
        blockers.append("Package must be proven deterministic")
    if package.get("extracted_validation") != "pass":
        blockers.append("Extracted package validation must pass")
    if not existing_path(root, package.get("evidence")):
        findings.append("package.evidence must reference an existing path")

    rollback = value.get("rollback")
    if not isinstance(rollback, dict):
        findings.append("rollback must be an object")
        rollback = {}
    for field in ["target", "plan", "authority", "verification"]:
        if not isinstance(rollback.get(field), str) or not rollback.get(field).strip():
            blockers.append(f"rollback.{field} is required")

    limitations = value.get("known_limitations")
    if not isinstance(limitations, list):
        findings.append("known_limitations must be an array")

    github = value.get("github")
    if not isinstance(github, dict):
        findings.append("github must be an object")
        github = {}
    if not str(github.get("branch", "")).strip():
        blockers.append("GitHub branch is required")
    if not isinstance(github.get("pr_url"), str) or not URL_RE.match(
        github.get("pr_url", "")
    ):
        blockers.append("GitHub PR URL is required before release readiness")

    forbidden = contains_forbidden_key(value)
    if forbidden:
        findings.append(f"Forbidden sensitive/raw field: {forbidden}")
    return findings, blockers, trace


def render_readiness(
    value: dict[str, Any], findings: list[str], blockers: list[str], trace: dict[str, Any]
) -> str:
    ready = not findings and not blockers
    scope = value.get("scope") or {}
    safety = value.get("safety") or {}
    package = value.get("package") or {}
    rollback = value.get("rollback") or {}
    trace_release = trace.get("release") or {}
    lines = [
        "# Release Readiness Report / 发布就绪报告",
        "",
        f"Version: `{value.get('version', '-')}`",
        f"Gate: `{'READY' if ready else 'BLOCKED'}`",
        f"Human UAT: `{trace_release.get('uat_status', 'missing')}`",
        f"Release State: `{trace_release.get('status', 'missing')}`",
        "",
        "## Findings / 发现",
        "",
    ]
    if ready:
        lines.append("- No release blocker found. / 未发现发布阻塞。")
    lines.extend(f"- Validation: {item}" for item in findings)
    lines.extend(f"- Blocker: {item}" for item in blockers)
    lines.extend(
        [
            "",
            "## Scope / 范围",
            "",
            f"- Included: {', '.join(scope.get('included') or []) or '-'}",
            f"- Excluded: {len(scope.get('excluded') or [])}",
            f"- Deferred: {len(scope.get('deferred') or [])}",
            "",
            "## Publication / 发布",
            "",
            f"- Safety: {safety.get('decision', '-')} ({safety.get('profile', '-')})",
            f"- Destination: {safety.get('destination', '-')}",
            f"- Package: {package.get('asset', '-')} / {package.get('sha256', '-')}",
            f"- Rollback target: {rollback.get('target', '-')}",
            "",
            "## Next Action / 下一步",
            "",
            "- Publish only after this gate is READY and the human release transaction is explicitly authorized. / 只有本门禁为 READY 且人工明确批准发布事务后才能发布。"
            if ready
            else "- Resolve every finding and blocker, regenerate evidence, and rerun this command. / 处理所有发现和阻塞，重新生成证据后再运行本命令。",
            "",
            "This report never creates a tag, Release, Linear update, rollback, or human approval. / 本报告绝不会自动创建 tag、Release、Linear 更新、回滚或人工批准。",
            "",
        ]
    )
    return "\n".join(lines)


def render_release_notes(value: dict[str, Any], trace: dict[str, Any]) -> str:
    scope = value.get("scope") or {}
    safety = value.get("safety") or {}
    package = value.get("package") or {}
    rollback = value.get("rollback") or {}
    github = value.get("github") or {}
    trace_release = trace.get("release") or {}
    lines = [
        f"# Release {value.get('version', '-')}",
        "",
        "## Summary / 摘要",
        "",
        str(value.get("summary") or "AI Project OS release candidate / AI Project OS 发布候选"),
        "",
        "## Included Features / 包含功能",
        "",
    ]
    lines.extend(f"- {item}" for item in scope.get("included") or ["Missing / 缺失"])
    lines.extend(["", "## Excluded / 不包含", ""])
    lines.extend(f"- {item}" for item in scope.get("excluded") or ["None / 无"])
    lines.extend(["", "## Deferred / 延后", ""])
    lines.extend(f"- {item}" for item in scope.get("deferred") or ["None / 无"])
    lines.extend(["", "## Verification / 验证", ""])
    for test in value.get("tests") or []:
        if isinstance(test, dict):
            lines.append(f"- {test.get('id', '-')}: {test.get('status', '-')}")
    lines.extend(
        [
            f"- Human UAT: {trace_release.get('uat_status', 'missing')}",
            f"- Safety: {safety.get('decision', '-')} / Block {safety.get('block_findings', '-')}",
            f"- Package SHA-256: {package.get('sha256', '-')}",
            "",
            "## Known Limitations / 已知限制",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in value.get("known_limitations") or ["None recorded / 未记录"])
    lines.extend(
        [
            "",
            "## Rollback / 回滚",
            "",
            f"- Target: {rollback.get('target', '-')}",
            f"- Plan: {rollback.get('plan', '-')}",
            f"- Authority: {rollback.get('authority', '-')}",
            f"- Verification: {rollback.get('verification', '-')}",
            "",
            "## GitHub",
            "",
            f"- Branch: {github.get('branch', '-')}",
            f"- PR: {github.get('pr_url', '-')}",
            f"- Tag: {github.get('tag', '-')}",
            f"- Release: {github.get('release_url', '-')}",
            f"- Asset: {package.get('asset', '-')}",
            "",
        ]
    )
    return "\n".join(lines)


def classify_feedback(value: dict[str, Any]) -> dict[str, str]:
    if value.get("schema_version") != 1:
        raise ReleaseError("schema_version must be 1")
    required_bools = [
        "original_scope_complete",
        "blocks_current_uat",
        "affects_released_version",
        "requires_business_decision",
    ]
    if any(type(value.get(field)) is not bool for field in required_bools):
        raise ReleaseError("feedback classification boolean fields are required")
    kind = value.get("kind")
    if kind not in {"bug", "feature", "question"}:
        raise ReleaseError("kind must be bug, feature, or question")
    if value["requires_business_decision"]:
        classification = "decision"
        action = "Create or update a Decision and stop implementation. / 创建或更新 Decision 并停止实现。"
    elif value["original_scope_complete"] and value.get("later_version_feedback") is True:
        classification = "carry_over"
        action = "Keep the old issue Done and create a next-version revalidation record. / 保持旧 Issue Done，并创建下版本复验记录。"
    elif value["blocks_current_uat"]:
        classification = "current_fix"
        action = "Fix inside the frozen current version and rerun affected UAT. / 在冻结的当前版本内修复并重跑受影响 UAT。"
    elif kind == "bug" and value["affects_released_version"] and value.get("severity") in {
        "critical",
        "high",
    }:
        classification = "hotfix"
        action = "Plan a narrow hotfix/patch with explicit rollback and UAT. / 规划窄范围 hotfix/patch，并明确回滚与 UAT。"
    elif kind == "bug":
        classification = "patch"
        action = "Triage into a patch version; do not add a new feature. / 归入 patch 版本，不加入新 Feature。"
    elif kind == "feature":
        classification = "next_version"
        action = "Place in the next version or Backlog after scope review. / 范围审查后放入下一版本或 Backlog。"
    else:
        classification = "backlog"
        action = "Record for later triage without changing current scope. / 记录待后续分类，不改变当前范围。"
    return {"classification": classification, "next_action": action}


def validate_post_release(value: dict[str, Any], root: Path) -> tuple[list[str], list[str]]:
    findings: list[str] = []
    blockers: list[str] = []
    if value.get("schema_version") != 1:
        findings.append("schema_version must be 1")
    if not isinstance(value.get("version"), str) or not VERSION_RE.match(value.get("version", "")):
        findings.append("version must use vMAJOR.MINOR.PATCH")
    if value.get("tag") != value.get("version"):
        blockers.append("tag must exactly match version")
    if not isinstance(value.get("release_url"), str) or not URL_RE.match(
        value.get("release_url", "")
    ):
        blockers.append("release_url must be an HTTPS URL")
    local_digest = value.get("local_sha256")
    remote_digest = value.get("remote_sha256")
    if not isinstance(local_digest, str) or not SHA256_RE.match(local_digest):
        blockers.append("local_sha256 is invalid")
    if local_digest != remote_digest:
        blockers.append("remote asset digest does not match local digest")
    checks = value.get("checks")
    if not isinstance(checks, list) or not checks:
        findings.append("checks must be a non-empty array")
        checks = []
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            findings.append(f"checks[{index}] must be an object")
            continue
        if check.get("status") != "pass":
            blockers.append(f"Post-release check {check.get('id', index)} must pass")
        evidence = check.get("evidence")
        if not isinstance(evidence, str) or not evidence.strip():
            findings.append(f"checks[{index}].evidence is required")
    if not str(value.get("rollback_target", "")).strip():
        findings.append("rollback_target is required")
    forbidden = contains_forbidden_key(value)
    if forbidden:
        findings.append(f"Forbidden sensitive/raw field: {forbidden}")
    return findings, blockers


def render_post_release(
    value: dict[str, Any], findings: list[str], blockers: list[str]
) -> str:
    passed = not findings and not blockers
    lines = [
        "# Post-Release Verification Receipt / 发布后验证回执",
        "",
        f"Version: `{value.get('version', '-')}`",
        f"Result: `{'PASS' if passed else 'BLOCK'}`",
        f"Tag: `{value.get('tag', '-')}`",
        f"Release: {value.get('release_url', '-')}",
        f"Asset SHA-256: `{value.get('local_sha256', '-')}`",
        f"Rollback Target: `{value.get('rollback_target', '-')}`",
        "",
        "## Findings / 发现",
        "",
    ]
    if passed:
        lines.append("- Remote and local release evidence match. / 远端与本地发布证据一致。")
    lines.extend(f"- Validation: {item}" for item in findings)
    lines.extend(f"- Blocker: {item}" for item in blockers)
    lines.extend(["", "## Checks / 检查", ""])
    for check in value.get("checks") or []:
        if isinstance(check, dict):
            lines.append(
                f"- {check.get('id', '-')}: {check.get('status', '-')} / {check.get('evidence', '-')}"
            )
    lines.extend(
        [
            "",
            "Receipt content is sanitized metadata only; no token, raw payload, comment body, source line, or file content is stored. / 回执只含脱敏元数据，不保存 token、raw payload、评论正文、源代码行或文件内容。",
            "",
        ]
    )
    return "\n".join(lines)


def write_output(root: Path, value: str | None, content: str) -> None:
    if not value:
        return
    path = resolve_under_root(root, value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    subparsers = parser.add_subparsers(dest="command", required=True)
    plan = subparsers.add_parser("plan")
    plan.add_argument("--input", required=True)
    plan.add_argument("--report")
    plan.add_argument("--notes")
    classify = subparsers.add_parser("classify")
    classify.add_argument("--input", required=True)
    classify.add_argument("--output")
    post = subparsers.add_parser("post-release")
    post.add_argument("--input", required=True)
    post.add_argument("--output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    try:
        value = read_json(resolve_under_root(root, args.input))
        if args.command == "classify":
            result = classify_feedback(value)
            rendered = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
            write_output(root, args.output, rendered)
            print(rendered, end="")
            return 0
        if args.command == "post-release":
            findings, blockers = validate_post_release(value, root)
            rendered = render_post_release(value, findings, blockers)
            write_output(root, args.output, rendered)
            print(rendered)
            return 0 if not findings and not blockers else 2
        findings, blockers, trace = validate_release_input(value, root)
        readiness = render_readiness(value, findings, blockers, trace)
        notes = render_release_notes(value, trace)
        write_output(root, args.report, readiness)
        write_output(root, args.notes, notes)
        print(readiness)
        return 0 if not findings and not blockers else 2
    except ReleaseError as exc:
        print(f"[BLOCK] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
