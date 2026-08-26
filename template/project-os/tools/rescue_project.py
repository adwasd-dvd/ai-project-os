#!/usr/bin/env python3
"""Build deterministic, sanitized mature-project rescue evidence.

The tool inspects product files without modifying them, excludes the installed
project-os package from product evidence, and writes only to an explicitly
selected repository-internal evidence directory when --write is provided.
It never writes Linear, runs product commands, accesses production, or approves
human gates.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable


SCHEMA_VERSION = 1
OUTPUT_FILES = (
    "RESCUE_EVIDENCE.json",
    "RESCUE_DIAGNOSIS.md",
    "RECOVERY_ROADMAP.md",
    "LINEAR_RESCUE_IMPORT.json",
    "PM_NEXT_ACTION.md",
    "RESCUE_RECEIPT.json",
)
VERSION_RE = re.compile(r"^v\d+\.\d+\.\d+$")
FEATURE_PREFIX_RE = re.compile(r"^[A-Z][A-Z0-9]{1,9}$")
FINDING_ID_RE = re.compile(r"^[A-Z][A-Z0-9_-]{2,63}$")
STATES = {"observed", "derived", "claimed", "inferred", "contradicted", "unknown"}
IMPACTS = {"critical", "high", "medium", "low", "unknown"}
CONFIDENCES = {"high", "medium", "low", "unknown"}
DISPOSITIONS = {"confirm", "decision", "bug", "feature", "chore", "backlog", "accept_risk"}
BLOCK_GATES = {"baseline", "development", "linear", "release"}
HUMAN_DISPOSITIONS = {"confirm", "decision", "accept_risk"}
CODEX_DISPOSITIONS = {"bug", "feature", "chore"}
IMPACT_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "unknown": 4}
FORBIDDEN_KEYS = {
    "credential",
    "environment_value",
    "file_content",
    "matched_value",
    "password",
    "payload",
    "private_key",
    "raw",
    "secret",
    "source_line",
    "token",
    "value",
}


class RescueError(RuntimeError):
    """Raised when rescue evidence cannot be generated safely."""


def load_sibling(name: str) -> ModuleType:
    path = Path(__file__).with_name(f"{name}.py")
    spec = importlib.util.spec_from_file_location(f"aipos_{name}", path)
    if spec is None or spec.loader is None:
        raise RescueError(f"Cannot load required tool: {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


whitebox_scan = load_sibling("whitebox_scan")
safety_scan = load_sibling("safety_scan")


def resolve_under_root(root: Path, value: str, *, must_exist: bool = False) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise RescueError("Paths must stay inside the repository root.") from exc
    if must_exist and not resolved.exists():
        raise RescueError(f"Required path does not exist: {value}")
    return resolved


def default_feature_prefix(name: str) -> str:
    letters = re.sub(r"[^A-Za-z0-9]", "", name).upper()
    if not letters or not letters[0].isalpha():
        letters = "PROJ" + letters
    return (letters[:10] or "PROJ")


def default_input(root: Path) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "project": {
            "name": root.name,
            "target_version": None,
            "feature_prefix": default_feature_prefix(root.name),
            "language": "en+zh",
            "exclude_prefixes": ["project-os"],
        },
        "linear": {
            "project": root.name,
            "milestone": None,
            "write_approved": False,
        },
        "human_gates": {
            "baseline_confirmed": False,
            "decisions_resolved": False,
            "uat_passed": False,
        },
        "findings": [],
        "resolutions": [],
    }


def read_input(root: Path, value: str | None) -> dict[str, Any]:
    if not value:
        return default_input(root)
    path = resolve_under_root(root, value, must_exist=True)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RescueError(f"Cannot read rescue input: {exc}") from exc
    if not isinstance(data, dict):
        raise RescueError("Rescue input must be a JSON object.")
    return data


def find_forbidden_key(value: Any, prefix: str = "") -> str | None:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = str(key).lower()
            path = f"{prefix}.{key}" if prefix else str(key)
            if normalized in FORBIDDEN_KEYS:
                return path
            found = find_forbidden_key(item, path)
            if found:
                return found
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found = find_forbidden_key(item, f"{prefix}[{index}]")
            if found:
                return found
    return None


def text_is_sensitive(value: str) -> bool:
    return bool(safety_scan.text_rule_ids(value))


def required_text(item: dict[str, Any], field: str, context: str) -> str:
    value = item.get(field)
    if not isinstance(value, str) or not value.strip():
        raise RescueError(f"{context}.{field} is required.")
    value = value.strip()
    if len(value) > 1000:
        raise RescueError(f"{context}.{field} is too long.")
    if text_is_sensitive(value):
        raise RescueError(f"{context}.{field} appears to contain sensitive raw data.")
    return value


def validate_evidence_paths(root: Path, values: Any, context: str) -> list[str]:
    if not isinstance(values, list) or not values:
        raise RescueError(f"{context}.evidence must be a non-empty array.")
    paths: list[str] = []
    for raw in values:
        if not isinstance(raw, str) or not raw.strip():
            raise RescueError(f"{context}.evidence contains an invalid path.")
        absolute = resolve_under_root(root, raw.strip(), must_exist=True)
        paths.append(absolute.relative_to(root).as_posix())
    return sorted(set(paths))


def normalize_input(root: Path, raw: dict[str, Any]) -> dict[str, Any]:
    forbidden = find_forbidden_key(raw)
    if forbidden:
        raise RescueError(f"Forbidden sensitive/raw field: {forbidden}")
    if raw.get("schema_version") != SCHEMA_VERSION:
        raise RescueError(f"schema_version must be {SCHEMA_VERSION}.")

    project = raw.get("project")
    linear = raw.get("linear")
    gates = raw.get("human_gates")
    findings = raw.get("findings")
    resolutions = raw.get("resolutions", [])
    if not isinstance(project, dict) or not isinstance(linear, dict):
        raise RescueError("project and linear objects are required.")
    if not isinstance(gates, dict) or not isinstance(findings, list) or not isinstance(resolutions, list):
        raise RescueError("human_gates object plus findings and resolutions arrays are required.")

    name = required_text(project, "name", "project")
    target_version = project.get("target_version")
    if target_version is not None and (
        not isinstance(target_version, str) or not VERSION_RE.fullmatch(target_version)
    ):
        raise RescueError("project.target_version must be null or vMAJOR.MINOR.PATCH.")
    feature_prefix = project.get("feature_prefix") or default_feature_prefix(name)
    if not isinstance(feature_prefix, str) or not FEATURE_PREFIX_RE.fullmatch(feature_prefix):
        raise RescueError("project.feature_prefix must be 2-10 uppercase letters/digits and start with a letter.")
    if project.get("language", "en+zh") != "en+zh":
        raise RescueError("project.language must be en+zh for v1.0 rescue outputs.")
    exclusions = project.get("exclude_prefixes", ["project-os"])
    if not isinstance(exclusions, list) or not all(isinstance(item, str) for item in exclusions):
        raise RescueError("project.exclude_prefixes must be an array of paths.")
    exclusions = list(whitebox_scan.normalize_exclude_prefixes(["project-os", *exclusions]))

    linear_project = linear.get("project")
    milestone = linear.get("milestone")
    if linear_project is not None and not isinstance(linear_project, str):
        raise RescueError("linear.project must be a string or null.")
    if milestone is not None and not isinstance(milestone, str):
        raise RescueError("linear.milestone must be a string or null.")
    if type(linear.get("write_approved")) is not bool:
        raise RescueError("linear.write_approved must be boolean.")

    normalized_gates: dict[str, bool] = {}
    for field in ("baseline_confirmed", "decisions_resolved", "uat_passed"):
        if type(gates.get(field)) is not bool:
            raise RescueError(f"human_gates.{field} must be boolean.")
        normalized_gates[field] = gates[field]

    normalized_findings: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    if len(findings) > 500:
        raise RescueError("findings exceeds the 500-item safety limit.")
    for index, item in enumerate(findings):
        context = f"findings[{index}]"
        if not isinstance(item, dict):
            raise RescueError(f"{context} must be an object.")
        finding_id = item.get("finding_id")
        if not isinstance(finding_id, str) or not FINDING_ID_RE.fullmatch(finding_id):
            raise RescueError(f"{context}.finding_id is invalid.")
        if finding_id in seen_ids:
            raise RescueError(f"Duplicate finding_id: {finding_id}")
        seen_ids.add(finding_id)
        state = item.get("state")
        impact = item.get("impact")
        confidence = item.get("confidence")
        disposition = item.get("recommended_disposition")
        if state not in STATES or impact not in IMPACTS or confidence not in CONFIDENCES:
            raise RescueError(f"{context} has an invalid state, impact, or confidence.")
        if disposition not in DISPOSITIONS:
            raise RescueError(f"{context}.recommended_disposition is invalid.")
        blocks = item.get("blocks", [])
        if not isinstance(blocks, list) or not set(blocks).issubset(BLOCK_GATES):
            raise RescueError(f"{context}.blocks contains an invalid gate.")
        resolved = item.get("resolved", False)
        if type(resolved) is not bool:
            raise RescueError(f"{context}.resolved must be boolean.")
        resolution_evidence = item.get("resolution_evidence", [])
        if resolved:
            resolution_evidence = validate_evidence_paths(root, resolution_evidence, context)
        elif resolution_evidence:
            raise RescueError(f"{context}.resolution_evidence requires resolved=true.")
        normalized_findings.append(
            {
                "finding_id": finding_id,
                "title_en": required_text(item, "title_en", context),
                "title_zh": required_text(item, "title_zh", context),
                "state": state,
                "impact": impact,
                "confidence": confidence,
                "evidence": validate_evidence_paths(root, item.get("evidence"), context),
                "action_steps_en": required_text(item, "action_steps_en", context),
                "action_steps_zh": required_text(item, "action_steps_zh", context),
                "expected_result_en": required_text(item, "expected_result_en", context),
                "expected_result_zh": required_text(item, "expected_result_zh", context),
                "next_verification_en": required_text(item, "next_verification_en", context),
                "next_verification_zh": required_text(item, "next_verification_zh", context),
                "recommended_disposition": disposition,
                "owner": required_text(item, "owner", context),
                "blocks": sorted(set(blocks)),
                "resolved": resolved,
                "resolution_evidence": resolution_evidence,
                "source": "declared",
            }
        )

    normalized_resolutions: list[dict[str, Any]] = []
    resolved_ids: set[str] = set()
    for index, item in enumerate(resolutions):
        context = f"resolutions[{index}]"
        if not isinstance(item, dict):
            raise RescueError(f"{context} must be an object.")
        finding_id = item.get("finding_id")
        if not isinstance(finding_id, str) or not FINDING_ID_RE.fullmatch(finding_id):
            raise RescueError(f"{context}.finding_id is invalid.")
        if finding_id in resolved_ids:
            raise RescueError(f"Duplicate resolution finding_id: {finding_id}")
        resolved_ids.add(finding_id)
        normalized_resolutions.append(
            {
                "finding_id": finding_id,
                "resolution_en": required_text(item, "resolution_en", context),
                "resolution_zh": required_text(item, "resolution_zh", context),
                "resolved_by": required_text(item, "resolved_by", context),
                "resolution_evidence": validate_evidence_paths(
                    root, item.get("resolution_evidence"), context
                ),
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "project": {
            "name": name,
            "target_version": target_version,
            "feature_prefix": feature_prefix,
            "language": "en+zh",
            "exclude_prefixes": exclusions,
        },
        "linear": {
            "project": linear_project.strip() if isinstance(linear_project, str) else None,
            "milestone": milestone.strip() if isinstance(milestone, str) else None,
            "write_approved": linear["write_approved"],
        },
        "human_gates": normalized_gates,
        "findings": normalized_findings,
        "resolutions": normalized_resolutions,
    }


def run_git_paths(root: Path, *args: str) -> set[str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        return set()
    return {item for item in result.stdout.split("\0") if item}


def product_git_state(root: Path, exclusions: Iterable[str]) -> dict[str, Any]:
    prefixes = tuple(exclusions)

    def kept(values: set[str]) -> set[str]:
        return {
            value
            for value in values
            if not whitebox_scan.excluded_by_prefix(Path(value), prefixes)
        }

    is_repo = whitebox_scan.git_value(root, "rev-parse", "--is-inside-work-tree") == "true"
    if not is_repo:
        return {"is_repository": False, "clean": None, "staged": 0, "unstaged": 0, "untracked": 0}
    staged = kept(run_git_paths(root, "diff", "--cached", "--name-only", "-z"))
    unstaged = kept(run_git_paths(root, "diff", "--name-only", "-z"))
    untracked = kept(run_git_paths(root, "ls-files", "--others", "--exclude-standard", "-z"))
    return {
        "is_repository": True,
        "clean": not (staged or unstaged or untracked),
        "staged": len(staged),
        "unstaged": len(unstaged),
        "untracked": len(untracked),
    }


def make_finding(
    finding_id: str,
    title_en: str,
    title_zh: str,
    *,
    state: str,
    impact: str,
    confidence: str,
    evidence: list[str],
    action_steps_en: str,
    action_steps_zh: str,
    expected_result_en: str,
    expected_result_zh: str,
    next_verification_en: str,
    next_verification_zh: str,
    disposition: str,
    owner: str,
    blocks: Iterable[str] = (),
    source: str = "automatic",
) -> dict[str, Any]:
    return {
        "finding_id": finding_id,
        "title_en": title_en,
        "title_zh": title_zh,
        "state": state,
        "impact": impact,
        "confidence": confidence,
        "evidence": sorted(set(evidence)),
        "action_steps_en": action_steps_en,
        "action_steps_zh": action_steps_zh,
        "expected_result_en": expected_result_en,
        "expected_result_zh": expected_result_zh,
        "next_verification_en": next_verification_en,
        "next_verification_zh": next_verification_zh,
        "recommended_disposition": disposition,
        "owner": owner,
        "blocks": sorted(set(blocks)),
        "resolved": False,
        "resolution_evidence": [],
        "source": source,
    }


def items(evidence: dict[str, Any], key: str) -> list[Any]:
    value = evidence.get(key, {})
    return list(value.get("items", [])) if isinstance(value, dict) else []


def automatic_findings(
    config: dict[str, Any],
    whitebox: dict[str, Any],
    safety: dict[str, Any],
    git_state: dict[str, Any],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    project = config["project"]
    if not project["target_version"]:
        result.append(
            make_finding(
                "CFG-TARGET-001",
                "Target version is not configured",
                "尚未配置目标版本",
                state="unknown", impact="high", confidence="high", evidence=[],
                action_steps_en="Choose the first controlled target version for rescued work and record it in the rescue input.",
                action_steps_zh="选择救援工作的第一个受控目标版本，并写入救援输入。",
                expected_result_en="Every proposed work record has one explicit target version and Milestone.",
                expected_result_zh="每个建议工作事项都有一个明确的目标版本和 Milestone。",
                next_verification_en="Confirm the version with the Owner and regenerate the rescue plan.",
                next_verification_zh="与 Owner 确认版本并重新生成救援计划。",
                disposition="decision", owner="Owner", blocks=("baseline", "linear", "development"),
            )
        )

    file_count = whitebox["coverage"]["file_count"]
    if file_count == 0:
        result.append(
            make_finding(
                "SCOPE-001", "No product files remain in rescue scope", "救援范围内没有产品文件",
                state="unknown", impact="high", confidence="high", evidence=[],
                action_steps_en="Review repository root and exclusion prefixes before drawing project conclusions.",
                action_steps_zh="在得出项目结论前，检查仓库根目录和排除前缀。",
                expected_result_en="The rescue scope contains the intended product files while OS-owned files remain excluded.",
                expected_result_zh="救援范围包含目标产品文件，同时继续排除 OS 自有文件。",
                next_verification_en="Correct scope configuration and rerun inspect.",
                next_verification_zh="修正范围配置并重新运行 inspect。",
                disposition="confirm", owner="Owner", blocks=("baseline", "development"),
            )
        )

    manifests = items(whitebox, "manifests")
    lockfiles = items(whitebox, "lockfiles")
    if not manifests and file_count:
        result.append(
            make_finding(
                "DEP-001", "Dependency system is not evidenced", "依赖系统缺少证据",
                state="unknown", impact="high", confidence="medium", evidence=[],
                action_steps_en="Identify the canonical build/dependency manifest or explicitly classify the project as dependency-free.",
                action_steps_zh="识别权威构建/依赖清单，或明确把项目分类为无依赖项目。",
                expected_result_en="The runtime dependency source and reproducible setup path are explicit.",
                expected_result_zh="运行依赖来源和可复现安装路径清楚明确。",
                next_verification_en="Confirm the build system with a maintainer and record direct evidence.",
                next_verification_zh="与维护者确认构建系统并记录直接证据。",
                disposition="decision", owner="Owner", blocks=("baseline", "development"),
            )
        )
    elif manifests and not lockfiles:
        evidence = [row["path"] for row in manifests]
        result.append(
            make_finding(
                "DEP-LOCK-001", "Dependency lock evidence is missing", "缺少依赖锁定证据",
                state="derived", impact="medium", confidence="high", evidence=evidence,
                action_steps_en="Decide whether this ecosystem requires a committed lockfile and document the reproducible install policy.",
                action_steps_zh="决定该生态是否需要提交 lockfile，并记录可复现安装策略。",
                expected_result_en="Dependency resolution is reproducible or an explicit exception is accepted.",
                expected_result_zh="依赖解析可复现，或已明确接受例外。",
                next_verification_en="Generate or verify the canonical lock evidence in an isolated branch.",
                next_verification_zh="在隔离分支生成或验证权威锁定证据。",
                disposition="chore", owner="Codex", blocks=("release",),
            )
        )

    if not items(whitebox, "tests") and file_count:
        result.append(
            make_finding(
                "TEST-001", "No automated test path was discovered", "未发现自动化测试路径",
                state="derived", impact="high", confidence="medium", evidence=[],
                action_steps_en="Identify existing verification commands or add the smallest tests around critical behavior before broad changes.",
                action_steps_zh="识别现有验证命令，或在大范围修改前为关键行为增加最小测试。",
                expected_result_en="Critical rescue changes have reproducible automated verification.",
                expected_result_zh="关键救援改动具有可复现的自动验证。",
                next_verification_en="Run the maintainer-confirmed test command and record its result.",
                next_verification_zh="运行维护者确认的测试命令并记录结果。",
                disposition="feature", owner="Codex", blocks=("release",),
            )
        )

    if not items(whitebox, "documents") and file_count:
        result.append(
            make_finding(
                "DOC-001", "No maintained project documentation was discovered", "未发现受维护的项目文档",
                state="derived", impact="medium", confidence="medium", evidence=[],
                action_steps_en="Create a minimal evidence-backed project overview with setup, architecture, boundaries, and known unknowns.",
                action_steps_zh="创建最小的证据化项目概览，包含安装、架构、边界和已知未知项。",
                expected_result_en="A new maintainer can locate the system entry points and current risks.",
                expected_result_zh="新维护者可以找到系统入口和当前风险。",
                next_verification_en="Have the Owner review the overview against current behavior.",
                next_verification_zh="由 Owner 对照当前行为审查概览。",
                disposition="chore", owner="Codex", blocks=("release",),
            )
        )

    if not items(whitebox, "likely_entrypoints") and file_count:
        result.append(
            make_finding(
                "ENTRY-001", "Runtime entry point is not mechanically evident", "运行入口在机械证据中不明确",
                state="unknown", impact="medium", confidence="low", evidence=[row["path"] for row in manifests],
                action_steps_en="Identify and verify the canonical start, build, or library-consumer entry point.",
                action_steps_zh="识别并验证权威启动、构建或库调用入口。",
                expected_result_en="One reproducible command or integration path demonstrates how the system runs.",
                expected_result_zh="一个可复现命令或集成路径证明系统如何运行。",
                next_verification_en="Run the candidate entry point in an isolated environment.",
                next_verification_zh="在隔离环境运行候选入口。",
                disposition="confirm", owner="Owner", blocks=(),
            )
        )

    if not items(whitebox, "ci_candidates") and file_count:
        result.append(
            make_finding(
                "CI-001", "No continuous-integration configuration was discovered", "未发现持续集成配置",
                state="derived", impact="low", confidence="high", evidence=[],
                action_steps_en="Decide whether critical validation should run automatically on pull requests.",
                action_steps_zh="决定关键验证是否应在 Pull Request 中自动运行。",
                expected_result_en="The project has an explicit CI decision and repeatable release checks.",
                expected_result_zh="项目具有明确的 CI 决定和可重复发布检查。",
                next_verification_en="Confirm repository hosting and required branch checks.",
                next_verification_zh="确认仓库托管方式和必需分支检查。",
                disposition="backlog", owner="Owner", blocks=(),
            )
        )

    for safety_item in safety["findings"]:
        disposition = safety_item["disposition"]
        if disposition == "info":
            continue
        is_block = disposition == "block"
        result.append(
            make_finding(
                safety_item["finding_id"],
                f"Repository safety {disposition} at {safety_item['path']}",
                f"仓库安全项需要{('阻塞处理' if is_block else '人工复核')}：{safety_item['path']}",
                state="observed", impact=safety_item["severity"], confidence="high",
                evidence=[safety_item["path"]],
                action_steps_en=safety_item["remediation"],
                action_steps_zh="按对应 SAF 规则处理该路径；不要把命中值复制进报告。",
                expected_result_en="The selected publication profile has no unresolved safety block at this path.",
                expected_result_zh="所选发布 profile 在该路径不再有未解决的安全阻塞。",
                next_verification_en="Rerun the sanitized safety scan for the same profile and scope.",
                next_verification_zh="对相同 profile 和 scope 重新运行脱敏安全扫描。",
                disposition="bug" if is_block else "confirm", owner="Owner" if not is_block else "Codex",
                blocks=("baseline", "development", "linear", "release") if is_block else ("release",),
                source="safety",
            )
        )

    if git_state["is_repository"] and not git_state["clean"]:
        result.append(
            make_finding(
                "GIT-001", "Product worktree contains uncommitted changes", "产品工作区存在未提交改动",
                state="observed", impact="medium", confidence="high", evidence=[],
                action_steps_en="Identify the owner and intent of existing changes before rescue implementation modifies overlapping product files.",
                action_steps_zh="在救援实现修改重叠产品文件前，确认现有改动的负责人和意图。",
                expected_result_en="Existing work is preserved and rescue changes are isolated on a clear branch.",
                expected_result_zh="现有工作得到保留，救援改动隔离在清晰分支中。",
                next_verification_en="Review Git status with the maintainer; do not discard unrelated changes.",
                next_verification_zh="与维护者审查 Git 状态，不丢弃无关改动。",
                disposition="confirm", owner="Owner", blocks=(),
            )
        )
    return result


def finding_sort_key(item: dict[str, Any]) -> tuple[int, str]:
    return IMPACT_ORDER[item["impact"]], item["finding_id"]


def apply_resolutions(
    findings: list[dict[str, Any]], resolutions: list[dict[str, Any]]
) -> None:
    by_id = {item["finding_id"]: item for item in findings}
    for resolution in resolutions:
        finding_id = resolution["finding_id"]
        finding = by_id.get(finding_id)
        if finding is None:
            raise RescueError(f"Resolution references an unknown finding: {finding_id}")
        if finding["source"] == "safety":
            raise RescueError(
                f"Safety finding {finding_id} cannot be resolved while the current scan still emits it."
            )
        finding["resolved"] = True
        finding["resolution_evidence"] = resolution["resolution_evidence"]
        finding["resolution_en"] = resolution["resolution_en"]
        finding["resolution_zh"] = resolution["resolution_zh"]
        finding["resolved_by"] = resolution["resolved_by"]


def derive_gate(config: dict[str, Any], findings: list[dict[str, Any]]) -> str:
    open_items = [item for item in findings if not item["resolved"]]
    if any(item["source"] == "safety" and "baseline" in item["blocks"] for item in open_items):
        return "SAFETY_BLOCKED"
    if any(
        "baseline" in item["blocks"]
        or item["recommended_disposition"] == "decision"
        or (item["state"] in {"contradicted", "unknown"} and item["impact"] in {"critical", "high"})
        for item in open_items
    ):
        return "NEEDS_HUMAN_DECISION"
    if not config["human_gates"]["baseline_confirmed"]:
        return "READY_FOR_BASELINE_REVIEW"
    if not config["linear"]["project"] or not config["linear"]["milestone"]:
        return "NEEDS_LINEAR_CONFIGURATION"
    if not config["linear"]["write_approved"]:
        return "READY_FOR_LINEAR_APPROVAL"
    return "READY_FOR_DEVELOPMENT"


def derive_queues(config: dict[str, Any], findings: list[dict[str, Any]], gate: str) -> dict[str, Any]:
    open_items = [item for item in findings if not item["resolved"]]
    human = [
        item["finding_id"]
        for item in open_items
        if item["recommended_disposition"] in HUMAN_DISPOSITIONS or "baseline" in item["blocks"]
    ]
    codex = [
        item["finding_id"]
        for item in open_items
        if item["recommended_disposition"] in CODEX_DISPOSITIONS and "baseline" not in item["blocks"]
    ]
    review = [
        item["finding_id"]
        for item in open_items
        if item["source"] == "safety" or item["state"] in {"contradicted", "unknown"}
    ]
    backlog = [item["finding_id"] for item in open_items if item["recommended_disposition"] == "backlog"]
    blockers = [item["finding_id"] for item in open_items if item["blocks"]]

    if gate == "SAFETY_BLOCKED":
        next_action = "Resolve the first safety Block and rerun rescue inspection. / 先解决第一个安全 Block，再重新运行救援检查。"
    elif gate == "NEEDS_HUMAN_DECISION":
        next_action = "Owner reviews the first blocking contradiction, unknown, or Decision. / Owner 审查第一个阻塞矛盾、未知项或 Decision。"
    elif gate == "READY_FOR_BASELINE_REVIEW":
        next_action = "Owner reviews and confirms the evidence-backed baseline. / Owner 审查并确认基于证据的 Baseline。"
    elif gate == "NEEDS_LINEAR_CONFIGURATION":
        next_action = "Set one Linear Project and one target Milestone in the rescue input. / 在救援输入中设置一个 Linear Project 和一个目标 Milestone。"
    elif gate == "READY_FOR_LINEAR_APPROVAL":
        next_action = "Review the dry-run Linear package and explicitly approve writes separately. / 审查 Linear dry-run 包，并另行明确批准写入。"
    elif codex:
        next_action = f"Codex may start the highest-priority ready item: {codex[0]}. / Codex 可开始最高优先级 Ready 项：{codex[0]}。"
    elif human:
        next_action = f"Owner reviews the highest-priority Human Queue item: {human[0]}. / Owner 审查最高优先级人类队列事项：{human[0]}。"
    elif backlog:
        next_action = f"Triage the highest-priority Backlog item: {backlog[0]}. / 分类最高优先级 Backlog 事项：{backlog[0]}。"
    else:
        next_action = "No safe implementation item is ready; rescan or refine scope. / 当前没有可安全实施的事项；请重新扫描或细化范围。"
    return {
        "gate": gate,
        "human_queue": sorted(set(human)),
        "codex_queue": sorted(set(codex)),
        "review_queue": sorted(set(review)),
        "backlog": sorted(set(backlog)),
        "blockers": sorted(set(blockers)),
        "next_action": next_action,
        "linear_write_approved": config["linear"]["write_approved"],
        "local_product_writes_performed": 0,
        "external_writes_performed": 0,
    }


def linear_type(disposition: str) -> str:
    return {
        "decision": "Decision",
        "accept_risk": "Decision",
        "bug": "Bug",
        "feature": "Feature",
        "chore": "Chore",
        "confirm": "Chore",
        "backlog": "Backlog",
    }[disposition]


def build_linear_import(
    config: dict[str, Any], findings: list[dict[str, Any]], evidence: dict[str, Any], gate: str
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    target = config["project"]["target_version"] or "<target-version-required>"
    milestone = config["linear"]["milestone"] or "<milestone-required>"
    prefix = config["project"]["feature_prefix"]
    for index, finding in enumerate(
        [item for item in findings if not item["resolved"]], start=1
    ):
        record_type = linear_type(finding["recommended_disposition"])
        feature_id = f"{prefix}-R{index:03d}"
        key_source = "|".join(
            [config["linear"]["project"] or "", milestone, finding["finding_id"], record_type]
        )
        records.append(
            {
                "record_key": hashlib.sha256(key_source.encode("utf-8")).hexdigest()[:24],
                "feature_id": feature_id,
                "type": record_type,
                "title": f"{finding['title_en']} / {finding['title_zh']}",
                "target_version": target,
                "project": config["linear"]["project"] or "<project-required>",
                "milestone": milestone,
                "source_finding": finding["finding_id"],
                "action_steps": {
                    "en": finding["action_steps_en"],
                    "zh": finding["action_steps_zh"],
                },
                "expected_result": {
                    "en": finding["expected_result_en"],
                    "zh": finding["expected_result_zh"],
                },
                "evidence": finding["evidence"],
                "impact": finding["impact"],
                "confidence": finding["confidence"],
                "queue": "human" if finding["recommended_disposition"] in HUMAN_DISPOSITIONS else "codex",
                "assignee": None,
                "status": "Backlog" if record_type == "Backlog" else "Todo",
                "blocks": finding["blocks"],
            }
        )

    repository = evidence["whitebox"]["repository"]
    product = evidence["whitebox"]
    description = (
        f"## Project Rescue / 项目救援\n\n"
        f"Project / 项目: {config['project']['name']}\n\n"
        f"Rescue gate / 救援门禁: `{gate}`\n\n"
        f"Product files / 产品文件: {product['coverage']['file_count']}\n\n"
        f"Git commit / Git 提交: `{repository['git'].get('commit') or '-'}`\n\n"
        f"Open findings / 未解决发现: {sum(1 for item in findings if not item['resolved'])}\n\n"
        "Detailed evidence / 详细证据: `project-os/rescue/RESCUE_DIAGNOSIS.md`, "
        "`RECOVERY_ROADMAP.md`, and `PM_NEXT_ACTION.md`."
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "mode": "dry-run",
        "language": "en+zh",
        "one_project_rule": True,
        "target_project": config["linear"]["project"],
        "target_milestone": config["linear"]["milestone"],
        "write_approved_in_input": config["linear"]["write_approved"],
        "writes_performed": 0,
        "project_description_markdown": description,
        "proposed_records": records,
        "boundary": "This file is a proposal only. It never performs Linear writes or human approval. / 本文件只是一份建议，绝不执行 Linear 写入或人工批准。",
    }


def render_diagnosis(evidence: dict[str, Any]) -> str:
    findings = evidence["findings"]
    counts = evidence["summary"]
    lines = [
        "# Rescue Diagnosis / 救援诊断",
        "",
        f"Project / 项目: **{evidence['project']['name']}**",
        f"Gate / 门禁: `{evidence['pm']['gate']}`",
        f"Product files / 产品文件: {evidence['whitebox']['coverage']['file_count']}",
        f"Open findings / 未解决发现: {counts['open_findings']}",
        f"Safety / 安全: Block {counts['safety_block']}, Review {counts['safety_review']}",
        "",
        "Generated evidence contains paths and metadata, not matched values, source lines, environment values, file contents, raw conversations, or private payloads. / 生成证据只含路径和元数据，不含命中值、源代码行、环境变量值、文件正文、原始对话或私密 payload。",
        "",
        "## Coverage / 覆盖范围",
        "",
        f"- Excluded prefixes / 排除前缀: {', '.join(evidence['project']['exclude_prefixes'])}",
        f"- Manifests / 依赖清单: {len(items(evidence['whitebox'], 'manifests'))}",
        f"- Lockfiles / 锁定文件: {len(items(evidence['whitebox'], 'lockfiles'))}",
        f"- Documents / 文档: {len(items(evidence['whitebox'], 'documents'))}",
        f"- Tests / 测试: {len(items(evidence['whitebox'], 'tests'))}",
        f"- Entrypoints / 入口: {len(items(evidence['whitebox'], 'likely_entrypoints'))}",
        f"- Git product worktree clean / 产品工作区干净: {evidence['git_state']['clean']}",
        "",
        "## Findings / 发现",
        "",
        "| ID | Finding / 发现 | State | Impact | Confidence | Disposition | Resolved | Blocks | Evidence |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for item in findings:
        evidence_paths = ", ".join(f"`{path}`" for path in item["evidence"]) or "-"
        title = f"{item['title_en']} / {item['title_zh']}"
        lines.append(
            f"| {item['finding_id']} | {title} | {item['state']} | {item['impact']} | "
            f"{item['confidence']} | {item['recommended_disposition']} | {item['resolved']} | "
            f"{', '.join(item['blocks']) or '-'} | {evidence_paths} |"
        )
    lines.extend(["", "## Next Verification / 下一步验证", ""])
    for item in findings:
        if not item["resolved"]:
            lines.append(
                f"- **{item['finding_id']}**: {item['next_verification_en']} / {item['next_verification_zh']}"
            )
    lines.extend(
        [
            "",
            "## Boundary / 边界",
            "",
            "This diagnosis does not run product code, install dependencies, access production, change Git/Linear/GitHub, resolve business Decisions, approve UAT, or release software. / 本诊断不运行产品代码、不安装依赖、不访问生产、不修改 Git/Linear/GitHub、不替人解决业务 Decision、不批准 UAT，也不发布软件。",
            "",
        ]
    )
    return "\n".join(lines)


def render_roadmap(evidence: dict[str, Any]) -> str:
    findings = [item for item in evidence["findings"] if not item["resolved"]]
    safety_ids = [item["finding_id"] for item in findings if item["source"] == "safety"]
    baseline_ids = [
        item["finding_id"]
        for item in findings
        if "baseline" in item["blocks"] or item["state"] in {"contradicted", "unknown"}
    ]
    stabilize_ids = [
        item["finding_id"]
        for item in findings
        if item["recommended_disposition"] in CODEX_DISPOSITIONS and item["finding_id"] not in safety_ids
    ]
    phases = [
        ("0", "Contain safety and scope risk / 控制安全与范围风险", safety_ids, "No publication Block remains; scope is accepted. / 无发布 Block，范围已确认。"),
        ("1", "Close contradictions and unknowns / 关闭矛盾与未知项", baseline_ids, "Blocking Decisions are resolved or explicitly routed. / 阻塞 Decision 已解决或明确路由。"),
        ("2", "Stabilize the project / 稳定项目", stabilize_ids, "Dependencies, tests, docs, and critical behavior have reproducible evidence. / 依赖、测试、文档和关键行为有可复现证据。"),
        ("3", "Confirm baseline / 确认 Baseline", [], "Owner confirms coverage, limitations, and remaining risk. / Owner 确认覆盖范围、限制和剩余风险。"),
        ("4", "Import one Linear roadmap / 导入单一 Linear 路线图", [], "Explicit approval precedes idempotent writes to one Project and Milestone. / 明确批准后才向一个 Project 和 Milestone 幂等写入。"),
        ("5", "Develop and release through gates / 通过门禁开发与发布", [], "Tests, review, human UAT, release, and post-release checks remain distinct. / 测试、Review、人工 UAT、发布和发布后检查保持分离。"),
    ]
    lines = [
        "# Recovery Roadmap / 恢复路线图",
        "",
        f"Current Gate / 当前门禁: `{evidence['pm']['gate']}`",
        "",
        "The order below is dependency-aware. Later phases do not bypass unresolved earlier gates. / 以下顺序考虑依赖关系，后续阶段不能绕过前序未解决门禁。",
        "",
    ]
    for number, title, ids, completion in phases:
        lines.extend(
            [
                f"## Phase {number} - {title}",
                "",
                f"Findings / 发现: {', '.join(ids) or 'No automatically assigned finding / 无自动分配发现'}",
                "",
                f"Completion Evidence / 完成证据: {completion}",
                "",
            ]
        )
    lines.extend(
        [
            "## Rollback / 回滚",
            "",
            "Before product changes, abandon the rescue branch or remove generated `project-os/rescue/` evidence. After controlled changes begin, use project-specific rollback evidence and preserve project memory. The rescue tool never rewrites Git history or rolls production back. / 产品改动前可放弃救援分支或删除生成的 `project-os/rescue/` 证据。受控改动开始后，使用项目自己的回滚证据并保留项目记忆。救援工具绝不改写 Git 历史或自动回滚生产。",
            "",
        ]
    )
    return "\n".join(lines)


def render_pm(evidence: dict[str, Any]) -> str:
    pm = evidence["pm"]
    lines = [
        "# PM Next Action / PM 下一步",
        "",
        f"Gate / 门禁: `{pm['gate']}`",
        f"Next Action / 下一步: {pm['next_action']}",
        "",
        "## Queues / 队列",
        "",
        f"- Human Queue / 人类队列: {', '.join(pm['human_queue']) or 'None / 无'}",
        f"- Codex Queue / Codex 队列: {', '.join(pm['codex_queue']) or 'None / 无'}",
        f"- Review Queue / Review 队列: {', '.join(pm['review_queue']) or 'None / 无'}",
        f"- Blockers / 阻塞: {', '.join(pm['blockers']) or 'None / 无'}",
        f"- Backlog / 待办池: {', '.join(pm['backlog']) or 'None / 无'}",
        "",
        "## Control Facts / 控制事实",
        "",
        f"- Linear write approved in input / 输入中已批准 Linear 写入: {pm['linear_write_approved']}",
        "- Linear writes performed / 已执行 Linear 写入: 0",
        "- Product writes performed / 已执行产品写入: 0",
        "- External writes performed / 已执行外部写入: 0",
        "- Human UAT approval performed / 已执行人工 UAT 批准: 0",
        "",
    ]
    return "\n".join(lines)


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_bundle(
    root: Path,
    config: dict[str, Any],
    output_dir: Path,
    profile: str,
    scope: str,
    max_files: int,
    max_bytes: int,
) -> dict[str, str]:
    exclusions = config["project"]["exclude_prefixes"]
    whitebox = whitebox_scan.build_evidence(
        root,
        output_dir,
        max_files=max_files,
        exclude_prefixes=exclusions,
    )
    # The number of excluded OS files grows when this tool writes its own
    # evidence. Prefixes are the stable coverage fact; omit the volatile count.
    whitebox["coverage"].pop("excluded_requested_count", None)
    output_relative = (output_dir / safety_scan.OUTPUT_NAME).relative_to(root)
    safety = safety_scan.scan_repository(
        root,
        profile,
        scope,
        output_relative,
        max_files,
        max_bytes,
        exclusions,
    )
    safety["skipped"].pop("requested_prefixes", None)
    git_state = product_git_state(root, exclusions)
    findings = automatic_findings(config, whitebox, safety, git_state) + config["findings"]
    ids: set[str] = set()
    for item in findings:
        if item["finding_id"] in ids:
            raise RescueError(f"Automatic and declared finding IDs collide: {item['finding_id']}")
        ids.add(item["finding_id"])
    apply_resolutions(findings, config["resolutions"])
    findings.sort(key=finding_sort_key)
    gate = derive_gate(config, findings)
    pm = derive_queues(config, findings, gate)
    summary = {
        "total_findings": len(findings),
        "open_findings": sum(1 for item in findings if not item["resolved"]),
        "contradictions": sum(1 for item in findings if item["state"] == "contradicted" and not item["resolved"]),
        "unknowns": sum(1 for item in findings if item["state"] == "unknown" and not item["resolved"]),
        "safety_block": safety["summary"]["block_findings"],
        "safety_review": safety["summary"]["review_findings"],
    }
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "tool": "AI Project OS rescue_project.py",
        "mode": "local evidence plan",
        "project": config["project"],
        "linear": config["linear"],
        "human_gates": config["human_gates"],
        "safety_boundary": {
            "product_code_writes": False,
            "external_writes": False,
            "production_access": False,
            "secret_values_emitted": False,
            "source_lines_emitted": False,
            "file_contents_emitted": False,
            "raw_conversations_emitted": False,
        },
        "git_state": git_state,
        "whitebox": whitebox,
        "publication_safety": safety,
        "findings": findings,
        "summary": summary,
        "pm": pm,
    }
    linear_import = build_linear_import(config, findings, evidence, gate)
    artifacts = {
        "RESCUE_EVIDENCE.json": json_text(evidence),
        "RESCUE_DIAGNOSIS.md": render_diagnosis(evidence),
        "RECOVERY_ROADMAP.md": render_roadmap(evidence),
        "LINEAR_RESCUE_IMPORT.json": json_text(linear_import),
        "PM_NEXT_ACTION.md": render_pm(evidence),
    }
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "result": "PASS",
        "gate": gate,
        "artifacts": [
            {"path": name, "sha256": sha256_text(content)}
            for name, content in sorted(artifacts.items())
        ],
        "product_writes_performed": 0,
        "external_writes_performed": 0,
        "sanitized": True,
    }
    artifacts["RESCUE_RECEIPT.json"] = json_text(receipt)
    return artifacts


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def write_bundle(output_dir: Path, artifacts: dict[str, str]) -> None:
    for name in OUTPUT_FILES:
        write_atomic(output_dir / name, artifacts[name])


def verify_bundle(output_dir: Path, artifacts: dict[str, str]) -> list[str]:
    findings: list[str] = []
    for name in OUTPUT_FILES:
        path = output_dir / name
        if not path.exists():
            findings.append(f"Missing: {name}")
            continue
        try:
            current = path.read_text(encoding="utf-8")
        except OSError as exc:
            findings.append(f"Unreadable {name}: {exc}")
            continue
        if current != artifacts[name]:
            findings.append(f"Stale: {name}")
    return findings


def print_summary(artifacts: dict[str, str], *, written: bool = False) -> None:
    evidence = json.loads(artifacts["RESCUE_EVIDENCE.json"])
    summary = evidence["summary"]
    print("AI Project OS Rescue / AI Project OS 项目救援")
    print(f"Project / 项目: {evidence['project']['name']}")
    print(f"Gate / 门禁: {evidence['pm']['gate']}")
    print(f"Product files / 产品文件: {evidence['whitebox']['coverage']['file_count']}")
    print(f"Findings / 发现: {summary['open_findings']}")
    print(f"Safety Block / 安全阻塞: {summary['safety_block']}")
    print(f"Next Action / 下一步: {evidence['pm']['next_action']}")
    print(f"Evidence written / 已写证据: {'Yes / 是' if written else 'No / 否'}")
    print("Product or external writes / 产品或外部写入: No / 否")


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--input", help="Optional rescue input JSON inside the repository.")
    parser.add_argument("--profile", choices=safety_scan.PROFILES, default="private")
    parser.add_argument("--scope", choices=safety_scan.SCOPES, default="worktree")
    parser.add_argument("--output-dir", default="project-os/rescue")
    parser.add_argument("--max-files", type=int, default=50_000)
    parser.add_argument("--max-bytes", type=int, default=safety_scan.MAX_FILE_BYTES)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    inspect_parser = subparsers.add_parser("inspect", help="Read-only rescue inspection.")
    add_common_arguments(inspect_parser)
    inspect_parser.add_argument("--summary", action="store_true")
    plan_parser = subparsers.add_parser("plan", help="Generate the rescue evidence plan.")
    add_common_arguments(plan_parser)
    plan_parser.add_argument("--write", action="store_true", help="Write only rescue evidence files.")
    plan_parser.add_argument("--summary", action="store_true")
    verify_parser = subparsers.add_parser("verify", help="Check that written rescue evidence is current.")
    add_common_arguments(verify_parser)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        print("[BLOCK] Repository root does not exist.", file=sys.stderr)
        return 2
    if args.max_files < 1 or args.max_bytes < 1:
        print("[BLOCK] Limits must be positive.", file=sys.stderr)
        return 2
    try:
        output_dir = resolve_under_root(root, args.output_dir)
        config = normalize_input(root, read_input(root, args.input))
        artifacts = build_bundle(
            root, config, output_dir, args.profile, args.scope, args.max_files, args.max_bytes
        )
        if args.command == "verify":
            findings = verify_bundle(output_dir, artifacts)
            if findings:
                for finding in findings:
                    print(f"[FAIL] {finding}")
                return 1
            print("[PASS] Rescue evidence is current / 救援证据为最新")
            return 0
        if args.command == "plan" and args.write:
            write_bundle(output_dir, artifacts)
            print_summary(artifacts, written=True)
            return 0
        if args.summary:
            print_summary(artifacts)
        else:
            print(artifacts["RESCUE_DIAGNOSIS.md"], end="")
        return 0
    except (RescueError, whitebox_scan.ScanError, safety_scan.ScanError) as exc:
        print(f"[BLOCK] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
