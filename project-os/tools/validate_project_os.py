#!/usr/bin/env python3
"""Lightweight AI Project OS validator.

Checks required files, key policy guardrails, template drift, and release zip
shape. It is intentionally small because AI Project OS is a Markdown-first
package, not a build system.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


CORE_FILES = [
    "AGENTS.md",
    "AUTOMATION_POLICY.md",
    "BOOTSTRAP.md",
    "CHANGELOG.md",
    "DAILY_MEETING.md",
    "FEATURE_TEMPLATE.md",
    "GITHUB_POLICY.md",
    "LINEAR_INTAKE.md",
    "LINEAR_POLICY.md",
    "LOCAL_OVERRIDES.md",
    "OS_VERSION.md",
    "PROJECT.md",
    "QUALITY_GATE.md",
    "ROADMAP.md",
    "RELEASE_POLICY.md",
    "REQUIREMENT_MANAGEMENT.md",
    "SELF_CHECK.md",
    "START_HERE.md",
    "UAT_TEMPLATE.md",
    "UPGRADE_POLICY.md",
    "VERSION_PLANNING.md",
    "WORKFLOW.md",
    "examples/FIRST_PROJECT.md",
    "tools/validate_project_os.py",
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
    ],
    "RELEASE_POLICY.md": [
        "UAT 通过，允许发布",
        "Patch 版本不得塞入新 Feature",
        "carry-over",
        "不要直接移动旧 issue",
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
    ],
    "ROADMAP.md": [
        "Project Whitebox",
        "Repo Safety & Project Memory Boundary",
        "OS Self-Upgrade",
        "v1.0",
    ],
    "OS_VERSION.md": [
        "v0.3.0",
    ],
    "CHANGELOG.md": [
        "v0.3.0",
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


def check_required_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for base in [root / "project-os", root / "template" / "project-os"]:
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
    for base in [root / "project-os", root / "template" / "project-os"]:
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


def check_release_zips(root: Path) -> list[Finding]:
    findings: list[Finding] = []
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
