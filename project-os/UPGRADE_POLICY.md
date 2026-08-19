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

## Verify After Upgrade

Codex must verify:

- Required OS files exist.
- `START_HERE.md` points to the correct startup flow.
- `SELF_CHECK.md` protects first-run permissions.
- `LINEAR_POLICY.md` requires first bulk write approval.
- `RELEASE_POLICY.md` requires human UAT.
- `OS_VERSION.md` and `CHANGELOG.md` are updated.
- `REQUIREMENT_MANAGEMENT.md`, `VERSION_PLANNING.md`, `LINEAR_INTAKE.md`, and `AUTOMATION_POLICY.md` are present.
- `tools/validate_project_os.py` passes for the upgraded repository.
