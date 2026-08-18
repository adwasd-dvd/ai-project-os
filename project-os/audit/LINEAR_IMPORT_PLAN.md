# LINEAR_IMPORT_PLAN

## Import Status

```text
Status: Draft - blocked on Linear app connection
Prepared By: Codex
Prepared Date: 2026-08-18
Confirmed By:
Write Approved By:
Imported Date:
```

## Safety Rules

- First bulk write to Linear requires human approval.
- Do not delete or overwrite existing Linear content.
- Check for duplicate project/issues before creating.
- Confirm Linear team before writing.
- Stop if state mapping or project target is unclear.

## Proposed Linear Structure

### Team

```text
Team: TBD
```

### Projects

| Project Name | Purpose | Version | Create / Use Existing | Notes |
|---|---|---|---|---|
| AI Project OS v0.1 | Initial OS source project and learning flow | v0.1.0 | Create if not existing | Blocked until Linear app is connected |

### Labels

| Label | Type | Purpose | Create / Use Existing |
|---|---|---|---|
| module:core | Module | Hard rules | Create if missing |
| module:init | Module | Self-check and audit | Create if missing |
| module:linear | Module | Linear governance | Create if missing |
| module:github | Module | GitHub governance | Create if missing |
| module:release | Module | Release and UAT | Create if missing |
| module:upgrade | Module | OS upgrades | Create if missing |
| module:package | Module | Distribution package | Create if missing |
| type:feature | Type | Feature work | Create if missing |
| type:decision | Type | Decisions | Create if missing |
| type:chore | Type | Maintenance | Create if missing |

### Status Mapping

| AI Project OS Status | Linear Status | Notes |
|---|---|---|
| Backlog | Backlog | If available |
| Needs Decision | Triage / Backlog | Depends on team statuses |
| Ready | Todo | If available |
| In Progress | In Progress | If available |
| In Review | In Review | If available |
| Ready for UAT | Todo / Review | Needs team mapping |
| Accepted | Done | After human UAT |
| Released | Done | After tag/release |

## Existing Linear Preflight

Must be filled before write. Current blocker: Linear app is not connected in Codex.

| Existing Item | Type | Possible Match | Risk | Action |
|---|---|---|---|---|
| TBD after team selection |  |  |  |  |

## Proposed Issues To Create

| Batch | Feature ID | Title | Type | Module | Target Version | Status | Labels | Depends On | Duplicate Risk |
|---|---|---|---|---|---|---|---|---|---|
| 1 | AIPOS-001 | Distributable `project-os/` lazy pack | feature | package | v0.1.0 | Ready for UAT | module:package,type:feature |  | Low |
| 1 | AIPOS-002 | Phase 0 Self-Check | feature | init | v0.1.0 | Ready for UAT | module:init,type:feature |  | Low |
| 1 | AIPOS-003 | Phase 1 Audit output specs | feature | init | v0.1.0 | Ready for UAT | module:init,type:feature |  | Low |
| 1 | AIPOS-004 | Linear MCP import policy | feature | linear | v0.1.0 | Ready for UAT | module:linear,type:feature |  | Low |
| 1 | AIPOS-005 | GitHub private repo and PR policy | feature | github | v0.1.0 | In Progress | module:github,type:feature |  | Low |
| 1 | AIPOS-006 | OS versioning and upgrade policy | feature | upgrade | v0.1.0 | Ready for UAT | module:upgrade,type:feature |  | Low |
| 1 | AIPOS-007 | Release and UAT governance | feature | release | v0.1.0 | Ready for UAT | module:release,type:feature |  | Low |
| 1 | AIPOS-008 | Generate v0.1.0 release zip | chore | package | v0.1.0 | Todo | module:package,type:chore | AIPOS-001 | Low |
| 2 | AIPOS-009 | Add automated policy validator | feature | quality | v0.2.0 | Backlog | type:feature |  | Low |
| 2 | AIPOS-010 | Add worked example for first real project | feature | docs | v0.2.0 | Backlog | type:feature |  | Low |

## Proposed Decisions To Create

| Decision ID | Title | Blocking | Owner | Needed By |
|---|---|---|---|---|
| DEC-001 | Choose Linear team for AI Project OS | Yes | Owner | Before Phase 3 import |
| DEC-002 | Confirm private GitHub repo owner/name | Yes | Owner | Before repo creation |
| DEC-003 | Decide whether release zips are committed or GitHub-release-only | No | Owner | Before v0.1.0 release |

## Items To Skip

| Item | Reason | Follow-up |
|---|---|---|
| Existing Linear updates | No existing target confirmed | Preflight after team selection |

## Batch Plan

### Batch 1

```text
Purpose: Create v0.1.0 source project issues and immediate setup tasks.
Items: AIPOS-001 through AIPOS-008, DEC-001 through DEC-003.
Risk: Low, after team confirmation and duplicate preflight.
```

### Batch 2

```text
Purpose: Create v0.2.0 learning and automation backlog.
Items: AIPOS-009 through AIPOS-010.
Risk: Low.
```

## Approval Block

```text
- [x] Baseline drafted.
- [ ] Baseline confirmed.
- [ ] Linear app connected.
- [ ] Linear team confirmed.
- [ ] Duplicate candidates reviewed.
- [ ] First bulk write approved.
```

Explicit approval phrase:

```text
批准写入 Linear。
```

## Import Result Log

| Batch | Date | Created | Skipped | Failed | Notes |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Codex Phase 3 Stop Conditions

Codex must stop if:

- Linear app is not connected.
- Linear team is unknown.
- Duplicate preflight finds existing matching project/issues.
- The user has not explicitly approved the first bulk write.
- A write would modify existing Linear content.
