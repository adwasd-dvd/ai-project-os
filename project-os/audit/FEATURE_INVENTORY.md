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

