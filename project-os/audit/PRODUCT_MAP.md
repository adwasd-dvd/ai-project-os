# PRODUCT_MAP

## Product Summary

AI Project OS is a reusable project-control package for teams using local Codex, Linear, and GitHub.

## Users / Actors

| Actor | Description | Evidence | Confidence |
|---|---|---|---|
| Owner | Confirms scope, priorities, UAT | OS policies | High |
| Project Manager | Maintains Linear and release scope | Linear policy | High |
| Operator | Uses local Codex to execute work | AGENTS / WORKFLOW | High |
| Consultant | Reviews architecture and risky work | AGENTS | High |
| Codex | Executes audit, plans, code changes, tests | BOOTSTRAP / SELF_CHECK | High |

## Product Modules

| Module ID | Module Name | Purpose | Evidence | Confidence |
|---|---|---|---|---|
| CORE | Core Rules | Hard rules and role boundaries | `AGENTS.md` | High |
| INIT | Initialization | Phase 0 self-check and Phase 1 audit | `SELF_CHECK.md`, `BOOTSTRAP.md` | High |
| LINEAR | Linear Governance | Linear import and issue rules | `LINEAR_POLICY.md` | High |
| GITHUB | GitHub Governance | Branch, PR, tag, release rules | `GITHUB_POLICY.md` | High |
| RELEASE | Release/UAT | Version and human acceptance gates | `RELEASE_POLICY.md`, `UAT_TEMPLATE.md` | High |
| UPGRADE | OS Maintenance | Versioning and upgrade rules | `UPGRADE_POLICY.md`, `OS_VERSION.md` | High |
| PACKAGE | Distribution | Template source and zip package | `template/project-os/` | High |

## User Flows

| Flow ID | Flow Name | Actors | Steps | Evidence | Status |
|---|---|---|---|---|---|
| FLOW-INIT | Install and initialize OS in a repo | Owner, Operator, Codex | Copy OS, run Phase 0, then Phase 1 | `START_HERE.md` | Complete |
| FLOW-LINEAR | Import confirmed plan to Linear | PM, Codex | Confirm Baseline, approve import, create issues | `LINEAR_POLICY.md` | Partial |
| FLOW-DEV | Develop by Feature ID | Operator, Codex | Read issue, implement, test, PR | `WORKFLOW.md` | Complete |
| FLOW-UAT | Human version acceptance | Owner, PM | UAT, classify feedback, release or fix | `UAT_TEMPLATE.md` | Complete |
| FLOW-UPGRADE | Upgrade installed OS | Owner, Codex | Compare, plan, approve, apply, verify | `UPGRADE_POLICY.md` | Partial |

## Suggested Module Labels for Linear

```text
module:core
module:init
module:linear
module:github
module:release
module:upgrade
module:package
```

## Confirmation Questions

- [ ] Are these modules acceptable for Linear labels?
- [ ] Should OS upgrade work be v0.1 patch or v0.2 scope?
- [ ] Should packaging include GitHub Release automation later?

