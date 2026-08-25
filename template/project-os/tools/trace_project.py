#!/usr/bin/env python3
"""Validate traceability and change-impact evidence for AI Project OS."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


FEATURE_ID_RE = re.compile(r"^[A-Z][A-Z0-9-]+-\d+$")
LINEAR_ID_RE = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")
VERSION_RE = re.compile(r"^v\d+\.\d+\.\d+$")
TRACE_STATES = [
    "planned",
    "implemented",
    "verified",
    "uat_pending",
    "accepted",
    "released",
]
CONFIDENCE_LEVELS = {"high", "medium", "low", "unknown"}
IMPACT_LEVELS = {"low", "medium", "high"}
REQUIRED_IMPACT_AREAS = {
    "modules",
    "dependencies",
    "data_security",
    "documentation",
    "tests",
    "uat",
    "rollout_rollback",
}


class TraceError(RuntimeError):
    """A user-facing traceability failure."""


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise TraceError(f"File not found / 文件不存在: {path}") from exc
    except json.JSONDecodeError as exc:
        raise TraceError(f"Invalid JSON / JSON 无效: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise TraceError(f"Expected JSON object / 需要 JSON object: {path}")
    return value


def resolve_under_root(root: Path, value: str) -> Path:
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise TraceError(f"Path escapes repository root: {value}") from exc
    return candidate


def existing_path(root: Path, value: str) -> bool:
    try:
        return resolve_under_root(root, value).exists()
    except TraceError:
        return False


def path_findings(
    root: Path, feature_id: str, field: str, values: list[Any]
) -> list[str]:
    findings: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value:
            findings.append(f"{feature_id}.{field}: path must be a non-empty string")
        elif not existing_path(root, value):
            findings.append(f"{feature_id}.{field}: missing path: {value}")
    return findings


def validate_manifest(manifest: dict[str, Any], root: Path) -> list[str]:
    findings: list[str] = []
    if manifest.get("schema_version") != 1:
        findings.append("schema_version must be 1")
    release = manifest.get("release")
    if not isinstance(release, dict):
        return findings + ["release must be an object"]
    version = release.get("version")
    if not isinstance(version, str) or not VERSION_RE.match(version):
        findings.append("release.version must use vMAJOR.MINOR.PATCH")
    if release.get("status") not in {"planning", "candidate", "released"}:
        findings.append("release.status must be planning, candidate, or released")
    if release.get("uat_status") not in {"pending", "pass", "fail"}:
        findings.append("release.uat_status must be pending, pass, or fail")
    features = manifest.get("features")
    if not isinstance(features, list) or not features:
        return findings + ["features must be a non-empty array"]
    seen: set[str] = set()
    for index, feature in enumerate(features):
        prefix = f"features[{index}]"
        if not isinstance(feature, dict):
            findings.append(f"{prefix} must be an object")
            continue
        feature_id = feature.get("feature_id")
        if not isinstance(feature_id, str) or not FEATURE_ID_RE.match(feature_id):
            findings.append(f"{prefix}.feature_id is invalid")
            feature_id = prefix
        elif feature_id in seen:
            findings.append(f"duplicate feature_id: {feature_id}")
        else:
            seen.add(feature_id)
        state = feature.get("state")
        if state not in TRACE_STATES:
            findings.append(f"{feature_id}.state must be one of {TRACE_STATES}")
            continue
        if feature.get("target_version") != version:
            findings.append(f"{feature_id}.target_version must equal release.version")
        linear_issue = feature.get("linear_issue")
        if not isinstance(linear_issue, str) or not LINEAR_ID_RE.match(linear_issue):
            findings.append(f"{feature_id}.linear_issue is invalid")
        requirements = feature.get("requirement_sources") or []
        if not isinstance(requirements, list) or not requirements:
            findings.append(f"{feature_id}.requirement_sources must not be empty")
        else:
            findings.extend(path_findings(root, feature_id, "requirement_sources", requirements))
        impact_report = feature.get("change_impact")
        if not isinstance(impact_report, str) or not impact_report:
            findings.append(f"{feature_id}.change_impact is required")
        elif not existing_path(root, impact_report):
            findings.append(f"{feature_id}.change_impact missing path: {impact_report}")

        code_paths = feature.get("code_paths") or []
        evidence_paths = feature.get("evidence_paths") or []
        tests = feature.get("tests") or []
        uat = feature.get("uat") or {}
        decisions = feature.get("decisions") or []
        risks = feature.get("risks") or []
        for field, value in [
            ("code_paths", code_paths),
            ("evidence_paths", evidence_paths),
            ("tests", tests),
        ]:
            if not isinstance(value, list):
                findings.append(f"{feature_id}.{field} must be an array")
        code_paths = code_paths if isinstance(code_paths, list) else []
        evidence_paths = evidence_paths if isinstance(evidence_paths, list) else []
        tests = tests if isinstance(tests, list) else []
        if not isinstance(uat, dict):
            findings.append(f"{feature_id}.uat must be an object")
            uat = {}
        if not isinstance(decisions, list) or not isinstance(risks, list):
            findings.append(f"{feature_id}.decisions and risks must be arrays")

        state_index = TRACE_STATES.index(state)
        if state_index >= TRACE_STATES.index("implemented"):
            if not code_paths and not evidence_paths:
                findings.append(f"{feature_id}: implemented state needs code_paths or evidence_paths")
            findings.extend(path_findings(root, feature_id, "code_paths", code_paths))
            findings.extend(path_findings(root, feature_id, "evidence_paths", evidence_paths))
        if state_index >= TRACE_STATES.index("verified"):
            if not tests:
                findings.append(f"{feature_id}: verified state needs tests")
            for test in tests:
                if not isinstance(test, dict):
                    findings.append(f"{feature_id}.tests entry must be an object")
                    continue
                if test.get("status") != "pass":
                    findings.append(f"{feature_id}.{test.get('id', 'test')}: test status must be pass")
                test_path = test.get("path")
                if not isinstance(test_path, str) or not existing_path(root, test_path):
                    findings.append(f"{feature_id}.{test.get('id', 'test')}: missing test path")
        if state_index >= TRACE_STATES.index("uat_pending"):
            if uat.get("status") not in {"pending", "pass"}:
                findings.append(f"{feature_id}.uat.status must be pending or pass")
        if state_index >= TRACE_STATES.index("accepted"):
            if uat.get("status") != "pass":
                findings.append(f"{feature_id}: accepted state requires human UAT pass")
            evidence = uat.get("evidence")
            if not isinstance(evidence, str) or not existing_path(root, evidence):
                findings.append(f"{feature_id}: accepted state requires UAT evidence path")
        if state == "released":
            if release.get("uat_status") != "pass":
                findings.append("released state requires release.uat_status=pass")
            if not release.get("tag") or not release.get("release_url"):
                findings.append("released state requires release tag and release_url")
    if release.get("status") == "released":
        if release.get("uat_status") != "pass":
            findings.append("released release.status requires release.uat_status=pass")
        if any(feature.get("state") != "released" for feature in features if isinstance(feature, dict)):
            findings.append("released release.status requires every feature state=released")
    return findings


def render_traceability(manifest: dict[str, Any], findings: list[str]) -> str:
    release = manifest.get("release") or {}
    lines = [
        "# Traceability Report / 追踪报告",
        "",
        f"Release: `{release.get('version', '-')}`",
        f"Release State: `{release.get('status', '-')}`",
        f"Human UAT: `{release.get('uat_status', '-')}`",
        "",
        "## Validation / 验证",
        "",
        f"Result: `{'PASS' if not findings else 'BLOCK'}`",
        f"Findings: {len(findings)}",
        "",
    ]
    if findings:
        lines.extend(f"- {finding}" for finding in findings)
    else:
        lines.append("- Evidence chain is structurally complete for the declared states. / 当前声明状态的证据链结构完整。")
    lines.extend(
        [
            "",
            "## Requirement-to-Release Matrix / 需求到发布矩阵",
            "",
            "| Feature | State | Linear | Requirement | Impact | Code/Evidence | Tests | Human UAT | Decisions | Risks |",
            "|---|---|---|---:|---|---:|---:|---|---:|---:|",
        ]
    )
    for feature in manifest.get("features") or []:
        uat = feature.get("uat") or {}
        lines.append(
            "| {feature_id} | {state} | {linear_issue} | {requirements} | `{impact}` | {evidence} | {tests} | {uat} | {decisions} | {risks} |".format(
                feature_id=feature.get("feature_id", "-"),
                state=feature.get("state", "-"),
                linear_issue=feature.get("linear_issue", "-"),
                requirements=len(feature.get("requirement_sources") or []),
                impact=feature.get("change_impact", "-"),
                evidence=len(feature.get("code_paths") or []) + len(feature.get("evidence_paths") or []),
                tests=len(feature.get("tests") or []),
                uat=uat.get("status", "missing"),
                decisions=len(feature.get("decisions") or []),
                risks=len(feature.get("risks") or []),
            )
        )
    lines.extend(
        [
            "",
            "## Release Evidence / 发布证据",
            "",
            f"- Branch: `{release.get('branch') or '-'}`",
            f"- Pull Request: {release.get('pr_url') or '-'}",
            f"- Tag: `{release.get('tag') or '-'}`",
            f"- Release: {release.get('release_url') or '-'}",
            "",
            "Automated tests never count as human UAT. / 自动测试永远不能替代人工 UAT。",
            "",
        ]
    )
    return "\n".join(lines)


def validate_impact(value: dict[str, Any], root: Path) -> tuple[list[str], list[str]]:
    findings: list[str] = []
    blockers: list[str] = []
    if value.get("schema_version") != 1:
        findings.append("schema_version must be 1")
    feature_id = value.get("feature_id")
    if not isinstance(feature_id, str) or not FEATURE_ID_RE.match(feature_id):
        findings.append("feature_id is invalid")
    target_version = value.get("target_version")
    if not isinstance(target_version, str) or not VERSION_RE.match(target_version):
        findings.append("target_version must use vMAJOR.MINOR.PATCH")
    scope_change = value.get("scope_change")
    if not isinstance(scope_change, bool):
        findings.append("scope_change must be boolean")
    elif scope_change:
        blockers.append("Scope expansion requires Owner approval / 扩大范围需要 Owner 批准")
    decisions = value.get("unresolved_decisions")
    if not isinstance(decisions, list):
        findings.append("unresolved_decisions must be an array")
        decisions = []
    if decisions:
        blockers.append("Unresolved Decision(s): " + ", ".join(str(item) for item in decisions))
    impacts = value.get("impacts")
    if not isinstance(impacts, list) or not impacts:
        return findings + ["impacts must be a non-empty array"], blockers
    seen_areas: set[str] = set()
    for index, impact in enumerate(impacts):
        prefix = f"impacts[{index}]"
        if not isinstance(impact, dict):
            findings.append(f"{prefix} must be an object")
            continue
        area = impact.get("area")
        if area not in REQUIRED_IMPACT_AREAS:
            findings.append(f"{prefix}.area is invalid: {area}")
        else:
            seen_areas.add(area)
        level = impact.get("level")
        confidence = impact.get("confidence")
        if level not in IMPACT_LEVELS:
            findings.append(f"{prefix}.level is invalid")
        if confidence not in CONFIDENCE_LEVELS:
            findings.append(f"{prefix}.confidence is invalid")
        for field in ["claim", "evidence", "next_verification"]:
            if not isinstance(impact.get(field), str) or not impact.get(field).strip():
                findings.append(f"{prefix}.{field} is required")
        evidence_path = impact.get("evidence_path")
        if evidence_path:
            if not isinstance(evidence_path, str):
                findings.append(f"{prefix}.evidence_path must be a string")
            elif not existing_path(root, evidence_path):
                findings.append(f"{prefix}.evidence_path missing: {evidence_path}")
        if level == "high" and confidence in {"low", "unknown"}:
            blockers.append(
                f"High-impact {area} claim has {confidence} confidence / 高影响 {area} 结论置信度为 {confidence}"
            )
    missing = REQUIRED_IMPACT_AREAS - seen_areas
    if missing:
        findings.append(f"missing impact areas: {sorted(missing)}")
    tests = value.get("test_plan")
    uat = value.get("uat_plan")
    if not isinstance(tests, list) or not tests:
        findings.append("test_plan must be a non-empty array")
    if not isinstance(uat, list) or not uat:
        findings.append("uat_plan must be a non-empty array")
    for field in ["rollout", "rollback"]:
        if not isinstance(value.get(field), str) or not value.get(field).strip():
            findings.append(f"{field} is required")
    return findings, blockers


def render_impact(value: dict[str, Any], findings: list[str], blockers: list[str]) -> str:
    ready = not findings and not blockers
    lines = [
        "# Change Impact Report / 变更影响报告",
        "",
        f"Feature ID: `{value.get('feature_id', '-')}`",
        f"Target Version: `{value.get('target_version', '-')}`",
        f"Development Gate: `{'READY' if ready else 'BLOCKED'}`",
        "",
        "## Gate Findings / 门禁发现",
        "",
    ]
    if not findings and not blockers:
        lines.append("- No structural blocker found. / 未发现结构性阻塞。")
    lines.extend(f"- Validation: {item}" for item in findings)
    lines.extend(f"- Blocker: {item}" for item in blockers)
    lines.extend(
        [
            "",
            "## Impact Matrix / 影响矩阵",
            "",
            "| Area | Level | Confidence | Claim | Evidence | Next Verification |",
            "|---|---|---|---|---|---|",
        ]
    )
    for impact in value.get("impacts") or []:
        if not isinstance(impact, dict):
            continue
        lines.append(
            "| {area} | {level} | {confidence} | {claim} | {evidence} | {next_verification} |".format(
                area=impact.get("area", "-"),
                level=impact.get("level", "-"),
                confidence=impact.get("confidence", "-"),
                claim=str(impact.get("claim", "-")).replace("|", "\\|"),
                evidence=str(impact.get("evidence", "-")).replace("|", "\\|"),
                next_verification=str(impact.get("next_verification", "-")).replace("|", "\\|"),
            )
        )
    lines.extend(["", "## Test Impact / 测试影响", ""])
    lines.extend(f"- {item}" for item in value.get("test_plan") or ["Missing / 缺失"])
    lines.extend(["", "## Human UAT Impact / 人工 UAT 影响", ""])
    lines.extend(f"- {item}" for item in value.get("uat_plan") or ["Missing / 缺失"])
    lines.extend(
        [
            "",
            "## Delivery / 交付",
            "",
            f"- Rollout: {value.get('rollout') or 'Missing / 缺失'}",
            f"- Rollback: {value.get('rollback') or 'Missing / 缺失'}",
            "",
            "Tests and UAT are intentionally separate. / 测试与人工 UAT 明确分开。",
            "",
        ]
    )
    return "\n".join(lines)


def write_output(path: Path | None, content: str) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    subparsers = parser.add_subparsers(dest="command", required=True)
    trace = subparsers.add_parser("trace")
    trace.add_argument("--manifest", required=True)
    trace.add_argument("--output")
    impact = subparsers.add_parser("impact")
    impact.add_argument("--input", required=True)
    impact.add_argument("--output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    try:
        if args.command == "trace":
            value = read_json(resolve_under_root(root, args.manifest))
            findings = validate_manifest(value, root)
            rendered = render_traceability(value, findings)
        else:
            value = read_json(resolve_under_root(root, args.input))
            findings, blockers = validate_impact(value, root)
            rendered = render_impact(value, findings, blockers)
            findings = findings + blockers
        output = resolve_under_root(root, args.output) if args.output else None
        write_output(output, rendered)
        print(rendered)
        return 0 if not findings else 2
    except TraceError as exc:
        print(f"[BLOCK] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
