# UPGRADE_POLICY

This file defines how AI Project OS upgrades itself and how installed copies should be upgraded inside other repositories.

## Core Principle

AI Project OS is software-like documentation.

It has:

- Versions.
- Changelog.
- Upgrade plans.
- Local overrides.
- Human approval gates.

An OS upgrade is not a blind file overwrite.

## Upgrade Phases

```text
Phase U0 - OS Self-Check
Phase U1 - Compare Current OS vs New OS
Phase U2 - Generate Upgrade Plan
Phase U3 - Human Approval
Phase U4 - Apply Upgrade
Phase U5 - Verify Project Still Works
```

## Phase U0 - OS Self-Check

Codex must read:

- `OS_VERSION.md`
- `CHANGELOG.md`
- `UPGRADE_POLICY.md`
- `LOCAL_OVERRIDES.md`
- `project-os/SELF_CHECK.md`

Codex must identify:

- Current installed OS version.
- Target OS version.
- Local overrides.
- Modified project-specific files.
- Risk level of the upgrade.

## Phase U1 - Compare

Codex compares the current installed OS with the target OS.

It must classify changes as:

- New file.
- Removed file.
- Safe text update.
- Policy change.
- Permission change.
- Linear behavior change.
- GitHub behavior change.
- Local override conflict.

## Phase U2 - Upgrade Plan

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

## Phase U3 - Human Approval

Codex must wait for explicit approval before applying upgrade changes.

Accepted approval language:

```text
批准升级 AI Project OS。
```

## Phase U4 - Apply Upgrade

Codex may apply only the approved changes.

Codex must not overwrite:

- `LOCAL_OVERRIDES.md`
- Project-specific audit output.
- Linear import results.
- UAT records.
- Project-specific decisions.

## Phase U5 - Verify

After upgrade, Codex must verify:

- Required OS files exist.
- `START_HERE.md` still points to the correct startup flow.
- `SELF_CHECK.md` still protects first-run permissions.
- `LINEAR_POLICY.md` still requires first bulk write approval.
- `RELEASE_POLICY.md` still requires human UAT.
- `OS_VERSION.md` and `CHANGELOG.md` are updated.
- `project-os/tools/validate_project_os.py` passes.

## Risk Levels

| Risk | Meaning | Approval |
|---|---|---|
| Low | Template wording or typo fixes | Approval recommended |
| Medium | New template or workflow step | Approval required |
| High | Permission, Linear, GitHub, release, or UAT policy changes | Approval required |

## Hard Rules

- Never overwrite local overrides automatically.
- Never remove human approval gates automatically.
- Never loosen Linear write rules without explicit approval.
- Never remove UAT gates without explicit approval.
- Never treat OS upgrade as product code development.
