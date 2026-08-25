#!/usr/bin/env python3
"""Lightweight AI Project OS validator.

Checks required files and policy guardrails in both source-repository and
installed-package layouts. Source repositories also check template drift and
release zip shape. It is intentionally small because AI Project OS is a
Markdown-first package, not a build system.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


CORE_FILES = [
    "AGENT_DOC_POLICY.md",
    "AGENTS.md",
    "AUTOMATION_POLICY.md",
    "AUTOMATION_RUNBOOK.md",
    "BOOTSTRAP.md",
    "CHANGELOG.md",
    "CHANGE_IMPACT.md",
    "DAILY_MEETING.md",
    "FEATURE_TEMPLATE.md",
    "GITHUB_POLICY.md",
    "LINEAR_INTAKE.md",
    "LINEAR_POLICY.md",
    "LOCAL_OVERRIDES.md",
    "OS_VERSION.md",
    "PROJECT.md",
    "QUICKSTART.md",
    "QUALITY_GATE.md",
    "REPO_PUBLICATION_POLICY.md",
    "RELEASE_CONTROL.md",
    "ROADMAP.md",
    "RELEASE_POLICY.md",
    "REQUIREMENT_MANAGEMENT.md",
    "SELF_CHECK.md",
    "SECURITY_BOUNDARY.md",
    "START_HERE.md",
    "TRACEABILITY.md",
    "UAT_TEMPLATE.md",
    "UPGRADE_POLICY.md",
    "VERSION_PLANNING.md",
    "WHITEBOX_PROTOCOL.md",
    "WORKFLOW.md",
    "discovery/README.md",
    "discovery/PROJECT_MAP.md",
    "discovery/DEPENDENCY_MAP.md",
    "discovery/DOCUMENT_INVENTORY.md",
    "discovery/SETTINGS_AND_DATA_REGISTER.md",
    "discovery/LOGIC_BOUNDARY_AUDIT.md",
    "discovery/WHITEBOX_IMPORT_REPORT.md",
    "automation/README.md",
    "automation/linear_intake.example.json",
    "automation/fixtures/train_a_snapshot.json",
    "runtime/.gitignore",
    "examples/FIRST_PROJECT.md",
    "examples/CHANGE_IMPACT_REPORT.md",
    "examples/SAFETY_EXAMPLE.md",
    "examples/TRACEABILITY_REPORT.md",
    "examples/TRAIN_A_EXAMPLE.md",
    "examples/TRAIN_A_INTAKE_REPORT.md",
    "examples/WHITEBOX_EXAMPLE.md",
    "safety/README.md",
    "safety/DOC_GAP_REGISTER.md",
    "safety/PROJECT_MEMORY_AUDIT.md",
    "safety/PUBLICATION_MANIFEST.md",
    "safety/SECRET_SCAN_REPORT.md",
    "traceability/README.md",
    "traceability/TRACEABILITY_MANIFEST.example.json",
    "traceability/CHANGE_IMPACT_INPUT.example.json",
    "release/README.md",
    "release/RELEASE_INPUT.example.json",
    "release/FEEDBACK_TRIAGE.example.json",
    "release/POST_RELEASE_INPUT.example.json",
    "upgrade/README.md",
    "upgrade/UPGRADE_CONFIG.example.json",
    "upgrade/UPSTREAM_GITHUB.example.json",
    "upgrade/fixtures/upstream_release.json",
    "tools/linear_intake.py",
    "tools/build_release.py",
    "tools/safety_scan.py",
    "tools/test_build_release.py",
    "tools/test_linear_intake.py",
    "tools/test_safety_scan.py",
    "tools/test_trace_project.py",
    "tools/release_project.py",
    "tools/test_release_project.py",
    "tools/upgrade_project_os.py",
    "tools/test_upgrade_project_os.py",
    "tools/test_validate_project_os.py",
    "tools/test_whitebox_scan.py",
    "tools/validate_project_os.py",
    "tools/trace_project.py",
    "tools/whitebox_scan.py",
]

AUDIT_FILES = [
    "audit/FEATURE_INVENTORY.md",
    "audit/GAPS_AND_DUPLICATES.md",
    "audit/LINEAR_IMPORT_PLAN.md",
    "audit/PRODUCT_MAP.md",
    "audit/PROJECT_BASELINE_DRAFT.md",
    "audit/RISKS_AND_DECISIONS.md",
    "audit/SELF_CHECK_REPORT.md",
]

MIRRORED_FILES = [
    file
    for file in CORE_FILES
    if file not in {
        "LOCAL_OVERRIDES.md",
    }
]

POLICY_PHRASES = {
    "AGENTS.md": [
        "无 Feature ID，不正式开发",
        "无目标版本，不顺手做",
        "一个 Codex 不能自我验收",
        "版本未人工 UAT，不得进入下一正式版本",
        "首次批量写入 Linear 必须人工确认",
        "WHITEBOX_PROTOCOL.md",
        "Evidence",
        "Confidence",
        "secret 值",
        "SECURITY_BOUNDARY.md",
        "Private repository is not a secret store",
        "matched value",
    ],
    "LINEAR_POLICY.md": [
        "English + Chinese",
        "Action Steps",
        "Expected Result",
        "Codex-authored Linear",
        "首次批量写入 Linear",
        "Assigned = human queue",
        "Unassigned = Codex queue",
        "`next:*` label 可以在多人团队或高级自动化中作为辅助信号",
        "Publication profile",
    ],
    "RELEASE_POLICY.md": [
        "UAT 通过，允许发布",
        "Patch 版本不得塞入新 Feature",
        "carry-over",
        "不要直接移动旧 issue",
        "Publication Safety Gate",
        "Release Asset SHA-256",
        "Deterministic Release Package",
    ],
    "VERSION_PLANNING.md": [
        "一个可交付 Issue 只属于一个目标版本",
        "Carry-over Revalidation",
        "不要直接把旧 Issue",
    ],
    "LINEAR_INTAKE.md": [
        "Mandatory Scan Scope",
        "Assignee-driven Routing",
        "Codex Queue",
        "Human Queue",
        "Review Queue",
        "Run Summary Template",
        "scanned",
        "skipped",
        "blockers",
    ],
    "AUTOMATION_POLICY.md": [
        "dry-run",
        "不自动批准 UAT",
        "不自动扩大 scope",
        "不自动修改本地代码",
        "Idempotency",
        "Status + Assignee Routing",
        "Implemented Runner Interface",
        "Write Authorization",
        "AIPOS_LINEAR_WRITE_APPROVED=1",
    ],
    "ROADMAP.md": [
        "Project Whitebox",
        "Repo Safety & Project Memory Boundary",
        "OS Self-Upgrade",
        "v1.0",
        "Development Train A",
        "Development Train B",
    ],
    "WHITEBOX_PROTOCOL.md": [
        "Observed",
        "Derived",
        "Claimed",
        "Inferred",
        "Contradicted",
        "Unknown",
        "Evidence",
        "Confidence",
        "Next Verification",
        "secret values",
        "Phase 0.5",
    ],
    "BOOTSTRAP.md": [
        "Phase 0.5 Whitebox Discovery",
        "Phase 0.75 Safety Classification",
        "whitebox_scan.py",
        "safety_scan.py",
        "SCAN_EVIDENCE.json",
        "LOGIC_BOUNDARY_AUDIT.md",
    ],
    "QUALITY_GATE.md": [
        "Ready for Whitebox Discovery",
        "Whitebox Complete",
        "Ready for Safety Classification",
        "Safety Classification Complete",
        "Evidence",
        "Confidence",
        "Next Verification",
        "Ready for Automated Linear Write",
        "Ready for Change Impact",
        "Traceability Complete for Declared State",
    ],
    "OS_VERSION.md": [
        "v0.6.0",
    ],
    "CHANGELOG.md": [
        "v0.6.0",
    ],
    "QUICKSTART.md": [
        "60-Second Start",
        "project-os/START_HERE.md",
        "English + Chinese",
    ],
    "SECURITY_BOUNDARY.md": [
        "Local Only",
        "Team Shared",
        "Private Repo",
        "Public Safe",
        "private repository is not a secret store",
    ],
    "REPO_PUBLICATION_POLICY.md": [
        "Publication Profiles",
        "--scope staged",
        "--scope tracked",
        "Go",
        "Review",
        "Block",
    ],
    "AGENT_DOC_POLICY.md": [
        "Single-User Pattern",
        "Team Pattern",
        "Public Pattern",
        "Canonical Source",
    ],
    "AUTOMATION_RUNBOOK.md": [
        "Dry run",
        "AIPOS_LINEAR_WRITE_APPROVED=1",
        "Idempotency and Partial Failure",
        "Scheduled scans never modify local product code",
        "Linear GraphQL getting started",
    ],
    "CHANGE_IMPACT.md": [
        "modules",
        "dependencies",
        "data_security",
        "documentation",
        "tests",
        "uat",
        "rollout_rollback",
        "high-impact claim has low or unknown confidence",
    ],
    "TRACEABILITY.md": [
        "Requirement",
        "Linear Issue",
        "Automated Tests",
        "Human UAT",
        "GitHub Release",
        "Automated test Pass never means human UAT Pass",
        "equivalent record",
        "post-release verification state",
    ],
    "RELEASE_CONTROL.md": [
        "Lifecycle Separation",
        "human UAT Pass",
        "release_project.py",
        "Rollback Boundary",
        "Post-Release Verification",
        "does not mutate Git, GitHub, Linear, tags, Releases",
    ],
    "UPGRADE_POLICY.md": [
        "inspect -> plan",
        "three-way plan",
        "Never Overwrite Automatically",
        "Guarded Apply",
        "--authorize-upgrade",
        "AIPOS_OS_UPGRADE_APPROVED=APPROVED",
        "Verify After Upgrade",
    ],
}

DISCOVERY_REPORT_FIELDS = {
    "discovery/PROJECT_MAP.md": ["Evidence", "Confidence", "Next Verification"],
    "discovery/DEPENDENCY_MAP.md": ["Evidence", "Confidence", "Next Verification"],
    "discovery/DOCUMENT_INVENTORY.md": ["Evidence", "Confidence", "Contradiction"],
    "discovery/SETTINGS_AND_DATA_REGISTER.md": [
        "Evidence",
        "Confidence",
        "Secret Values Present: Must be No",
        "Do not paste values",
    ],
    "discovery/LOGIC_BOUNDARY_AUDIT.md": [
        "Evidence",
        "Confidence",
        "Next Verification",
        "Contradiction Register",
    ],
    "discovery/WHITEBOX_IMPORT_REPORT.md": [
        "Evidence freshness",
        "Confidence",
        "Contradictions",
        "Unknowns",
        "Action Steps",
        "Expected Result",
        "No approval means no first bulk write",
    ],
}

SAFETY_REPORT_FIELDS = {
    "safety/PUBLICATION_MANIFEST.md": [
        "Destination Profile",
        "Artifact Classification",
        "Decision: Go / Review / Block",
    ],
    "safety/PROJECT_MEMORY_AUDIT.md": [
        "Sources Reviewed",
        "Confidence",
        "Next Verification",
        "Chat-only",
    ],
    "safety/DOC_GAP_REGISTER.md": [
        "Gap ID",
        "Evidence",
        "Decision Needed",
        "Next Verification",
    ],
    "safety/SECRET_SCAN_REPORT.md": [
        "Finding ID",
        "Rule ID",
        "Classification",
        "Disposition",
        "Remediation",
        "Matched Values Emitted: Must be No",
        "Source Lines Emitted: Must be No",
    ],
}


@dataclass
class Finding:
    level: str
    path: str
    message: str
    hint: str = ""

    def render(self) -> str:
        suffix = f" Hint / 提示: {self.hint}" if self.hint else ""
        return f"[{self.level}] {self.path}: {self.message}{suffix}"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def project_os_bases(root: Path) -> list[Path]:
    """Return installed OS plus the distributable copy when this is a source repo."""
    bases = [root / "project-os"]
    template_root = root / "template"
    if template_root.exists():
        bases.append(template_root / "project-os")
    return bases


def check_required_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for base in project_os_bases(root):
        label = base.relative_to(root).as_posix()
        if not base.exists():
            findings.append(
                Finding("FAIL", label, "Required directory missing / 必需目录不存在")
            )
            continue
        for rel in CORE_FILES + AUDIT_FILES:
            path = base / rel
            if not path.exists():
                findings.append(
                    Finding(
                        "FAIL",
                        path.relative_to(root).as_posix(),
                        "Required file missing / 必需文件不存在",
                    )
                )
    return findings


def check_policy_phrases(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for base in project_os_bases(root):
        for rel, phrases in POLICY_PHRASES.items():
            path = base / rel
            if not path.exists():
                continue
            text = read_text(path)
            for phrase in phrases:
                if phrase not in text:
                    findings.append(
                        Finding(
                            "FAIL",
                            path.relative_to(root).as_posix(),
                            f"Missing policy phrase / 缺少关键规则: {phrase}",
                        )
                    )
    return findings


def check_template_drift(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    project_os = root / "project-os"
    template_os = root / "template" / "project-os"
    if not template_os.exists():
        return findings
    for rel in MIRRORED_FILES:
        left = project_os / rel
        right = template_os / rel
        if not left.exists() or not right.exists():
            continue
        if read_text(left) != read_text(right):
            findings.append(
                Finding(
                    "WARN",
                    rel,
                    "Installed and template copy differ / 安装实例和模板副本不一致",
                    "If this is not a local override, sync the file.",
                )
            )
    return findings


def check_discovery_contract(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for base in project_os_bases(root):
        for rel, phrases in DISCOVERY_REPORT_FIELDS.items():
            path = base / rel
            if not path.exists():
                continue
            text = read_text(path)
            for phrase in phrases:
                if phrase not in text:
                    findings.append(
                        Finding(
                            "FAIL",
                            path.relative_to(root).as_posix(),
                            f"Missing whitebox field / 缺少白盒字段: {phrase}",
                        )
                    )

        scanner = base / "tools" / "whitebox_scan.py"
        if scanner.exists():
            scanner_text = read_text(scanner)
            for phrase in [
                '"--write"',
                '"--check"',
                '"secret_values_emitted": False',
                '"environment_values_emitted": False',
                '"file_contents_emitted": False',
                "Output directory must be inside the repository root.",
            ]:
                if phrase not in scanner_text:
                    findings.append(
                        Finding(
                            "FAIL",
                            scanner.relative_to(root).as_posix(),
                            f"Missing scanner guardrail / 缺少 scanner 保护: {phrase}",
                        )
                    )
    return findings


def check_safety_contract(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for base in project_os_bases(root):
        for rel, phrases in SAFETY_REPORT_FIELDS.items():
            path = base / rel
            if not path.exists():
                continue
            text = read_text(path)
            for phrase in phrases:
                if phrase not in text:
                    findings.append(
                        Finding(
                            "FAIL",
                            path.relative_to(root).as_posix(),
                            f"Missing safety field / 缺少安全字段: {phrase}",
                        )
                    )

        scanner = base / "tools" / "safety_scan.py"
        if scanner.exists():
            scanner_text = read_text(scanner)
            for phrase in [
                '"--write"',
                '"--check"',
                '"--fail-on-block"',
                '"matched_values_emitted": False',
                '"source_lines_emitted": False',
                '"environment_values_emitted": False',
                '"file_contents_emitted": False',
                "Output directory must be inside the repository root.",
            ]:
                if phrase not in scanner_text:
                    findings.append(
                        Finding(
                            "FAIL",
                            scanner.relative_to(root).as_posix(),
                            f"Missing safety scanner guardrail / 缺少安全 scanner 保护: {phrase}",
                        )
                    )
    return findings


def check_train_a_contract(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    required_impact_areas = {
        "modules",
        "dependencies",
        "data_security",
        "documentation",
        "tests",
        "uat",
        "rollout_rollback",
    }
    for base in project_os_bases(root):
        builder = base / "tools" / "build_release.py"
        if builder.exists():
            builder_text = read_text(builder)
            for phrase in [
                "FIXED_ZIP_TIME",
                "committed_source_tar",
                "Distributable template has uncommitted changes",
                "Output must stay under the repository releases/ directory",
            ]:
                if phrase not in builder_text:
                    findings.append(
                        Finding(
                            "FAIL",
                            builder.relative_to(root).as_posix(),
                            f"Missing deterministic package guardrail / 缺少确定性打包保护: {phrase}",
                        )
                    )

        runner = base / "tools" / "linear_intake.py"
        if runner.exists():
            runner_text = read_text(runner)
            for phrase in [
                "SUPPORTED_OPERATIONS",
                "FORBIDDEN_UPDATE_FIELDS",
                "AIPOS_LINEAR_WRITE_APPROVED",
                "--authorize-writes",
                "idempotency_key",
                "write_json_atomic",
                "None. Dry run only.",
                "NoRedirect",
                "auth.endpoint must be",
                "scan_complete",
                "max_plan_age_minutes",
                "nested connection limit reached",
            ]:
                if phrase not in runner_text:
                    findings.append(
                        Finding(
                            "FAIL",
                            runner.relative_to(root).as_posix(),
                            f"Missing automation guardrail / 缺少自动化保护: {phrase}",
                        )
                    )

        trace_tool = base / "tools" / "trace_project.py"
        if trace_tool.exists():
            trace_text = read_text(trace_tool)
            for phrase in [
                '"uat_pending"',
                '"accepted"',
                '"released"',
                "human UAT pass",
                "High-impact",
                "REQUIRED_IMPACT_AREAS",
            ]:
                if phrase not in trace_text:
                    findings.append(
                        Finding(
                            "FAIL",
                            trace_tool.relative_to(root).as_posix(),
                            f"Missing traceability guardrail / 缺少追踪保护: {phrase}",
                        )
                    )

        config_path = base / "automation" / "linear_intake.example.json"
        if config_path.exists():
            try:
                config = json.loads(read_text(config_path))
                policy = config.get("write_policy") or {}
                if config.get("language") != "en+zh":
                    findings.append(
                        Finding("FAIL", config_path.relative_to(root).as_posix(), "Default language must be en+zh")
                    )
                if policy.get("enabled") is not False:
                    findings.append(
                        Finding("FAIL", config_path.relative_to(root).as_posix(), "Example writes must be disabled")
                    )
                if config.get("state_file") != "project-os/runtime/linear_intake_ledger.json":
                    findings.append(
                        Finding("FAIL", config_path.relative_to(root).as_posix(), "Runtime ledger must stay under project-os/runtime/")
                    )
            except json.JSONDecodeError as exc:
                findings.append(
                    Finding("FAIL", config_path.relative_to(root).as_posix(), f"Invalid automation JSON: {exc}")
                )

        impact_path = base / "traceability" / "CHANGE_IMPACT_INPUT.example.json"
        if impact_path.exists():
            try:
                impact = json.loads(read_text(impact_path))
                areas = {
                    item.get("area")
                    for item in impact.get("impacts", [])
                    if isinstance(item, dict)
                }
                missing = required_impact_areas - areas
                if missing:
                    findings.append(
                        Finding(
                            "FAIL",
                            impact_path.relative_to(root).as_posix(),
                            f"Missing change-impact areas: {sorted(missing)}",
                        )
                    )
            except json.JSONDecodeError as exc:
                findings.append(
                    Finding("FAIL", impact_path.relative_to(root).as_posix(), f"Invalid impact JSON: {exc}")
                )
    return findings


def check_release_zips(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not (root / "template" / "project-os").exists():
        return findings
    releases = root / "releases"
    if not releases.exists():
        findings.append(
            Finding(
                "WARN",
                "releases/",
                "No releases directory found / 未找到 releases 目录",
            )
        )
        return findings

    zips = sorted(releases.glob("ai-project-os-v*.zip"))
    if not zips:
        findings.append(
            Finding(
                "WARN",
                "releases/",
                "No release zip found / 未找到 release zip",
            )
        )
        return findings

    for zip_path in zips:
        rel_label = zip_path.relative_to(root).as_posix()
        try:
            with zipfile.ZipFile(zip_path) as archive:
                names = archive.namelist()
                if not names:
                    findings.append(Finding("FAIL", rel_label, "Zip is empty / zip 为空"))
                    continue
                bad_names = [
                    name
                    for name in names
                    if name.startswith("/")
                    or ".." in Path(name).parts
                    or name.startswith("template/")
                    or name.startswith("project-os/project-os/")
                    or name.endswith(".DS_Store")
                ]
                if bad_names:
                    findings.append(
                        Finding(
                            "FAIL",
                            rel_label,
                            "Zip contains invalid paths / zip 包含非法路径",
                            ", ".join(bad_names[:3]),
                        )
                    )
                if "project-os/START_HERE.md" not in names:
                    findings.append(
                        Finding(
                            "FAIL",
                            rel_label,
                            "Zip must contain project-os/START_HERE.md / zip 必须包含启动文件",
                        )
                    )
                version_match = re.search(
                    r"-v(\d+)\.(\d+)\.(\d+)\.zip$", zip_path.name
                )
                version = (
                    tuple(int(part) for part in version_match.groups())
                    if version_match
                    else (0, 0, 0)
                )
                if version >= (0, 5, 0) and "project-os/QUICKSTART.md" not in names:
                    findings.append(
                        Finding(
                            "FAIL",
                            rel_label,
                            "v0.5+ zip must contain project-os/QUICKSTART.md / v0.5+ zip 必须包含快速启动文件",
                        )
                    )
                if not all(name.startswith("project-os/") for name in names):
                    findings.append(
                        Finding(
                            "FAIL",
                            rel_label,
                            "Zip top-level must be project-os/ only / 顶层目录必须只有 project-os/",
                        )
                    )
        except zipfile.BadZipFile:
            findings.append(Finding("FAIL", rel_label, "Bad zip file / zip 损坏"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AI Project OS package.")
    parser.add_argument("--root", default=".", help="Repository root. Defaults to cwd.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures / 将 WARN 视为失败",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings: list[Finding] = []
    findings.extend(check_required_files(root))
    findings.extend(check_policy_phrases(root))
    findings.extend(check_template_drift(root))
    findings.extend(check_discovery_contract(root))
    findings.extend(check_safety_contract(root))
    findings.extend(check_train_a_contract(root))
    findings.extend(check_release_zips(root))

    failures = [finding for finding in findings if finding.level == "FAIL"]
    warnings = [finding for finding in findings if finding.level == "WARN"]

    print("AI Project OS Validation / AI Project OS 验证")
    print(f"Root / 根目录: {root}")

    if findings:
        for finding in findings:
            print(finding.render())
    else:
        print("[PASS] No issues found / 未发现问题")

    print("")
    print(
        "Summary / 摘要: "
        f"{len(failures)} failure(s), {len(warnings)} warning(s)"
        f" / {len(failures)} 个失败，{len(warnings)} 个警告"
    )

    if failures or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
