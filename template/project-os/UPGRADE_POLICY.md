# UPGRADE_POLICY

This file defines how the installed AI Project OS copy should be upgraded inside this repository.

## Core Principle

An OS upgrade is not a blind file overwrite.

Codex must compare, plan, ask for approval, apply approved changes, and verify.

## Upgrade Phases

```text
Phase U0 - OS Self-Check
Phase U1 - Compare Current OS vs New OS
Phase U2 - Generate Upgrade Plan
Phase U3 - Human Approval
Phase U4 - Apply Upgrade
Phase U5 - Verify Project Still Works
```

Executable Train B flow:

```text
inspect -> plan -> human review -> apply on upgrade branch -> verify -> project UAT -> accept or abandon branch
```

可执行 Train B 流程：先检查版本，再生成计划，经人工 review 后只在 upgrade branch 执行，随后验证和项目 UAT，最后接受或放弃该分支。

## Version Discovery

Start from `upgrade/UPGRADE_CONFIG.example.json` or `upgrade/UPSTREAM_GITHUB.example.json`:

```bash
python3 project-os/tools/upgrade_project_os.py --root . inspect \
  --config project-os/upgrade/UPGRADE_CONFIG.example.json \
  --report project-os/runtime/OS_UPGRADE_INSPECTION.md
```

Supported sources:

- local `project-os` directory;
- local release zip with one `project-os/` root;
- offline metadata JSON;
- configured GitHub latest Release metadata.

GitHub credentials, when required, come only from the configured environment variable. The report never stores a token value. Missing network, malformed versions, ambiguous sources, and unapproved downgrades fail closed.

如需 GitHub 凭证，只能来自配置指定的环境变量，报告绝不保存 token 值。网络不可用、版本格式错误、来源不明确或未批准降级都会 fail closed。

## Required Upgrade Plan

Before applying an upgrade, Codex must generate:

```text
project-os/audit/OS_UPGRADE_PLAN.md
```

The plan must include:

- Current version.
- Target version.
- Files to add.
- Files to update.
- Files to leave unchanged.
- Conflicts.
- Risk level.
- Required human decisions.

Generate a deterministic three-way plan from installed, base, and target copies:

```bash
python3 project-os/tools/upgrade_project_os.py --root . plan \
  --config project-os/upgrade/UPGRADE_CONFIG.example.json \
  --json-output project-os/audit/OS_UPGRADE_PLAN.json \
  --report project-os/audit/OS_UPGRADE_PLAN.md
```

Actions are classified as:

```text
identical
add
safe_update
migrate
preserve
conflict
remove_candidate
```

Planning is read-only. Reports contain file paths, hashes, classifications, risk, decisions, validation, and rollback guidance; they do not contain file content or secret values.

计划阶段只读。报告只包含路径、hash、分类、风险、Decision、验证和回滚指引，不包含文件正文或 secret 值。

## Human Approval

Accepted approval language:

```text
批准升级 AI Project OS。
```

## Never Overwrite Automatically

Codex must not overwrite:

- `LOCAL_OVERRIDES.md`
- Project-specific audit output.
- Linear import results.
- UAT records.
- Project-specific decisions.
- `safety/PROJECT_MEMORY_AUDIT.md` project findings.
- `safety/DOC_GAP_REGISTER.md` project findings.
- `safety/SECRET_SCAN_REPORT.md` project evidence.
- `safety/PUBLICATION_MANIFEST.md` human dispositions.

The executable planner also protects project-specific discovery outputs and runtime/private context. Protected files are preserved byte-for-byte when they already exist. An absent protected template may be added, but an existing protected file is never blind-overwritten.

可执行 planner 也保护项目专属 discovery 产物和 runtime/private context。已有保护文件必须逐字节保留；缺失的保护模板可以新增，但不能盲目覆盖已有文件。

## Guarded Apply

Apply requires all of the following:

- plan status is `READY` with no conflict;
- plan is within its explicit freshness window;
- source digest and installed file hashes still match the plan;
- current branch starts with the configured upgrade branch prefix;
- no unrelated tracked worktree change exists;
- CLI includes `--authorize-upgrade`;
- runtime authorization environment equals `APPROVED`;
- every write stays inside the installed `project-os/` directory;
- receipts stay inside ignored `project-os/runtime/`.

```bash
export AIPOS_OS_UPGRADE_APPROVED=APPROVED

python3 project-os/tools/upgrade_project_os.py --root . apply \
  --plan project-os/audit/OS_UPGRADE_PLAN.json \
  --as-of 2026-08-25T12:15:00Z \
  --authorize-upgrade \
  --receipt project-os/runtime/OS_UPGRADE_RECEIPT.json
```

The command never deletes remove-candidates, resolves conflicts, rewrites Git history, merges a branch, rotates credentials, approves UAT, or accepts the upgrade automatically.

命令绝不自动删除 remove-candidate、解决冲突、改写 Git 历史、merge 分支、轮换凭证、批准 UAT 或接受升级。

## Verify After Upgrade

Codex must verify:

- Required OS files exist.
- `START_HERE.md` points to the correct startup flow.
- `SELF_CHECK.md` protects first-run permissions.
- `LINEAR_POLICY.md` requires first bulk write approval.
- `RELEASE_POLICY.md` requires human UAT.
- `OS_VERSION.md` and `CHANGELOG.md` are updated.
- `REQUIREMENT_MANAGEMENT.md`, `VERSION_PLANNING.md`, `LINEAR_INTAKE.md`, and `AUTOMATION_POLICY.md` are present.
- `SECURITY_BOUNDARY.md`, `REPO_PUBLICATION_POLICY.md`, `AGENT_DOC_POLICY.md`, and `QUICKSTART.md` are present.
- `tools/safety_scan.py` passes its tests and still omits matched values and source content.
- `tools/validate_project_os.py` passes for the upgraded repository.

First verify every planned hash:

```bash
python3 project-os/tools/upgrade_project_os.py --root . verify \
  --plan project-os/audit/OS_UPGRADE_PLAN.json \
  --receipt project-os/runtime/OS_UPGRADE_VERIFY.json
```

Then run the strict validator, full tool tests, target-profile safety gate, and project-specific human UAT. A verification failure stops the workflow and produces rollback guidance. It does not perform destructive automatic recovery.

随后运行 strict validator、完整工具测试、目标 profile 安全门禁和项目专属人工 UAT。验证失败会停止流程并给出回滚指引，不执行破坏性自动恢复。
