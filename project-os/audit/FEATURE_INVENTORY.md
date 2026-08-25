# FEATURE_INVENTORY

## Feature Inventory

| Feature ID | Module | Title | Current Status | Target Version | Evidence | Missing Tests | Acceptance Gap | Linear Action | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| AIPOS-001 | PACKAGE | Distributable `project-os/` lazy pack | Done | v0.1.0 | `template/project-os/` | Automated inventory check | Human package smoke test | Create | High |
| AIPOS-002 | INIT | Phase 0 Self-Check | Done | v0.1.0 | `SELF_CHECK.md`, `SELF_CHECK_REPORT.md` | Automated checklist validation | Human run-through in a real repo | Create | High |
| AIPOS-003 | INIT | Phase 1 Audit output specs | Done | v0.1.0 | `template/project-os/audit/*.md` | Template completeness check | Human review | Create | High |
| AIPOS-004 | LINEAR | Linear MCP import policy | Done | v0.1.0 | `LINEAR_POLICY.md` | None | Confirm first import workflow | Create | High |
| AIPOS-005 | GITHUB | GitHub private repo and PR policy | Partial | v0.1.0 | `GITHUB_POLICY.md` | GitHub repo not created | Private repo confirmation | Create | High |
| AIPOS-006 | UPGRADE | OS versioning and upgrade policy | Done | v0.1.0 | `OS_VERSION.md`, `UPGRADE_POLICY.md`, `CHANGELOG.md` | Upgrade dry run | Human review | Create | High |
| AIPOS-007 | RELEASE | Release and UAT governance | Done | v0.1.0 | `RELEASE_POLICY.md`, `UAT_TEMPLATE.md` | No release checklist automation | Human UAT for OS package | Create | High |
| AIPOS-008 | PACKAGE | Generate v0.1.0 release zip | Partial | v0.1.0 | `releases/` planned | Zip content verification | Need final package build | Create | High |
| AIPOS-009 | QUALITY | Add automated policy validator | Not Started | v0.2.0 | Gap identified | All automated tests missing | Define validator scope | Create | Medium |
| AIPOS-010 | DOCS | Add worked example for first real project | Not Started | v0.2.0 | User learning goal | Example QA | Need sample walkthrough | Create | Medium |

## Features By Module

### Module: PACKAGE

- AIPOS-001 Distributable `project-os/` lazy pack - Done
- AIPOS-008 Generate v0.1.0 release zip - Partial

### Module: INIT

- AIPOS-002 Phase 0 Self-Check - Done
- AIPOS-003 Phase 1 Audit output specs - Done

### Module: LINEAR

- AIPOS-004 Linear MCP import policy - Done

### Module: GITHUB

- AIPOS-005 GitHub private repo and PR policy - Partial

### Module: UPGRADE

- AIPOS-006 OS versioning and upgrade policy - Done

### Module: RELEASE

- AIPOS-007 Release and UAT governance - Done

### Module: QUALITY

- AIPOS-009 Add automated policy validator - Not Started

### Module: DOCS

- AIPOS-010 Add worked example for first real project - Not Started

## Human Review Checklist

- [ ] Feature IDs are acceptable.
- [ ] Target versions are acceptable.
- [ ] v0.1.0 scope is acceptable.
- [ ] v0.2.0 backlog is acceptable.

## Development Train A - v0.6.0

DEC-009 combines the former v0.6 Linear automation and v0.7 traceability scope into one formal v0.6.0 candidate and one consolidated UAT.

| Feature ID | Linear | Module | Title | Current Status | Target Version | Evidence | Automated Tests | Human Acceptance Gap | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| AIPOS-038 | DVD-219 | AUTOMATION / LINEAR | Scheduled Linear intake configuration and runner | Done | v0.6.0 | `AUTOMATION_RUNBOOK.md`, `automation/`, `tools/linear_intake.py` | `test_linear_intake.py` | Closed by v0.6.0 UAT Pass | High |
| AIPOS-039 | DVD-220 | AUTOMATION / HANDOFF | Deterministic queue routing, readiness, and feedback classification | Done | v0.6.0 | `LINEAR_INTAKE.md`, fixture report | `test_linear_intake.py` | Closed by v0.6.0 UAT Pass | High |
| AIPOS-040 | DVD-221 | AUTOMATION / SAFETY | Authorized idempotent Linear write executor and run ledger | Done | v0.6.0 | `AUTOMATION_POLICY.md`, `tools/linear_intake.py` | gate, idempotency, partial-failure tests | Closed by v0.6.0 UAT Pass | High |
| AIPOS-041 | DVD-222 | AUTOMATION / DOCS | Cron and Codex automation operations runbook | Done | v0.6.0 | `AUTOMATION_RUNBOOK.md` | validator phrases | Closed by v0.6.0 UAT Pass | High |
| AIPOS-042 | DVD-223 | TRACEABILITY / QUALITY | Requirement-to-release traceability manifest and validator | Done | v0.6.0 | `TRACEABILITY.md`, `tools/trace_project.py` | `test_trace_project.py` | Closed by v0.6.0 UAT Pass | High |
| AIPOS-043 | DVD-224 | TRACEABILITY / WORKFLOW | Change-impact planner and evidence report | Done | v0.6.0 | `CHANGE_IMPACT.md`, `tools/trace_project.py` | impact gate tests | Closed by v0.6.0 UAT Pass | High |
| AIPOS-044 | DVD-225 | QUALITY / PACKAGE / RELEASE | Train A validation, example, package, and consolidated UAT | Done | v0.6.0 | validator, example, final package, UAT and release records | full suite and extracted package | Closed by v0.6.0 UAT Pass | High |

## Development Train B - v0.8.0

DEC-009 combines the former v0.8 release/rollback and v0.9 self-upgrade scope into one formal v0.8.0 candidate and one consolidated UAT.

Linear Project: `2a8e9515-50be-40fe-981b-8cd29690d513`
Temporary equivalent requirement record: `f8583467-5009-4f8a-bb3f-f312ece4c704`

The free Linear workspace reached its 250 non-archived issue limit on 2026-08-25. Individual issue creation for AIPOS-045 through AIPOS-051 was attempted and rejected. No issue ID is claimed; the Project Document is the durable Linear requirement record until capacity is available.

| Feature ID | Linear Record | Module | Title | Current Status | Target Version | Planned Evidence | Planned Tests | Human Acceptance Gap | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| AIPOS-045 | Train B Feature Register | RELEASE / ACCEPTANCE | Release lifecycle and human UAT evidence model | Verified | v0.8.0 | schema v2, `TRACEABILITY.md`, validator | lifecycle and evidence-state tests pass | Owner confirms states and UAT evidence are understandable | High |
| AIPOS-046 | Train B Feature Register | RELEASE / TOOLING | Deterministic release readiness and notes generator | Verified | v0.8.0 | structured release input and `tools/release_project.py` | deterministic readiness and blocker tests pass | Owner reviews generated release plan and notes | High |
| AIPOS-047 | Train B Feature Register | RELEASE / RECOVERY | Rollback, hotfix, and post-release verification control | Verified | v0.8.0 | `RELEASE_CONTROL.md`, feedback classification, sanitized receipt | offline recovery and digest failure tests pass | Owner confirms recovery path is usable | High |
| AIPOS-048 | Train B Feature Register | UPGRADE / DISCOVERY | Installed and upstream OS version discovery | Verified | v0.8.0 | upstream configs and `tools/upgrade_project_os.py` | local/metadata/version/downgrade tests pass | Owner confirms version/source explanation | High |
| AIPOS-049 | Train B Feature Register | UPGRADE / PLANNING | Upgrade planner, migration order, and preservation conflicts | Verified | v0.8.0 | three-way hash plan and conflict report | identical/local/upstream/both-modified tests pass | Owner reviews preservation and conflicts | High |
| AIPOS-050 | Train B Feature Register | UPGRADE / APPLY | Guarded branch-based OS migration and rollback | Verified | v0.8.0 | authorized apply/verify flow and receipt | authorization, path, stale-plan, idempotency tests pass | Owner confirms branch and rollback boundary | High |
| AIPOS-051 | Train B Feature Register | QUALITY / PACKAGE / RELEASE | Train B dogfood, package validation, and consolidated UAT | Planned | v0.8.0 | dogfood report, candidate package, Draft PR, UAT | full source and extracted-package suites | Explicit v0.8.0 UAT conclusion | High |
