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
| AIPOS-038 | DVD-219 | AUTOMATION / LINEAR | Scheduled Linear intake configuration and runner | In Review | v0.6.0 | `AUTOMATION_RUNBOOK.md`, `automation/`, `tools/linear_intake.py` | `test_linear_intake.py` | Live dry-run and setup usability | High |
| AIPOS-039 | DVD-220 | AUTOMATION / HANDOFF | Deterministic queue routing, readiness, and feedback classification | In Review | v0.6.0 | `LINEAR_INTAKE.md`, fixture report | `test_linear_intake.py` | Human inspection of queue output | High |
| AIPOS-040 | DVD-221 | AUTOMATION / SAFETY | Authorized idempotent Linear write executor and run ledger | In Review | v0.6.0 | `AUTOMATION_POLICY.md`, `tools/linear_intake.py` | gate, idempotency, partial-failure tests | Human confirms write boundary | High |
| AIPOS-041 | DVD-222 | AUTOMATION / DOCS | Cron and Codex automation operations runbook | In Review | v0.6.0 | `AUTOMATION_RUNBOOK.md` | validator phrases | Non-engineering Owner follows setup | Medium |
| AIPOS-042 | DVD-223 | TRACEABILITY / QUALITY | Requirement-to-release traceability manifest and validator | In Review | v0.6.0 | `TRACEABILITY.md`, `tools/trace_project.py` | `test_trace_project.py` | Human confirms evidence chain is understandable | High |
| AIPOS-043 | DVD-224 | TRACEABILITY / WORKFLOW | Change-impact planner and evidence report | In Review | v0.6.0 | `CHANGE_IMPACT.md`, `tools/trace_project.py` | impact gate tests | Owner confirms impact summary is useful | High |
| AIPOS-044 | DVD-225 | QUALITY / PACKAGE / RELEASE | Train A validation, example, package, and consolidated UAT | In Review | v0.6.0 | validator, example, candidate package, UAT record | full suite and extracted package | Explicit v0.6.0 UAT approval | High |
