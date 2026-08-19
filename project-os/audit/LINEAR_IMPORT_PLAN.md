# LINEAR_IMPORT_PLAN

## Import Status

```text
Status: Imported
Prepared By: Codex
Prepared Date: 2026-08-18
Last Preflight Date: 2026-08-18
Confirmed By: User
Write Approved By: User
Imported Date: 2026-08-18
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
Team: DvdTeacher
```

### Projects

| Project Name | Purpose | Version | Create / Use Existing | Notes |
|---|---|---|---|---|
| AI Project OS v0.1 | Initial OS source project and learning flow | v0.1.0 | Create | No existing matching project found |

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

Preflight completed against team `DvdTeacher`.

| Existing Item | Type | Possible Match | Risk | Action |
|---|---|---|---|---|
| No matching project | Project | `AI Project OS v0.1` | Safe | Create project after approval |
| No matching issues | Issue | `AIPOS-*` | Safe | Create issues after approval |

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
| DEC-002 | Confirm private GitHub repo owner/name | No | Owner | Completed |
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
- [x] Baseline confirmed.
- [x] Linear app connected.
- [x] Linear team confirmed.
- [x] Duplicate candidates reviewed.
- [x] First bulk write approved.
```

Explicit approval phrase:

```text
批准写入 Linear。
```

## Import Result Log

| Batch | Date | Created | Skipped | Failed | Notes |
|---|---|---|---|---|---|
| Labels / Project | 2026-08-18 | 12 labels and project `AI Project OS v0.1` | 0 | 0 | Create-only import |
| Batch 1 | 2026-08-18 | `DVD-5` through `DVD-15` | 0 | 0 | v0.1.0 issues plus decisions |
| Batch 2 | 2026-08-18 | `DVD-16`, `DVD-17` | 0 | 0 | v0.2.0 backlog |

## Codex Phase 3 Stop Conditions

Codex must stop if:

- Linear team is unknown.
- Duplicate preflight finds existing matching project/issues.
- The user has not explicitly approved the first bulk write.
- A write would modify existing Linear content.

## Phase 3 Preflight Update - 2026-08-18

### Current Project Status

| Check | Result | Notes |
|---|---|---|
| Repository | `adwasd-dvd/ai-project-os` | GitHub visibility verified as `PRIVATE` |
| Current branch | `main` | Tracks `origin/main` |
| Current HEAD | `30b1abc` | Latest local commit: `Record Linear preflight status` |
| Working tree before this update | Clean | `git status --porcelain` returned no changes |
| Release artifact | Exists | `releases/ai-project-os-v0.1.0.zip` |
| Zip shape | Valid | Zip top-level directory is `project-os/` |
| Runtime dependencies | None | Markdown/template project |
| Baseline status | Confirmed | Confirmed by user on 2026-08-18 |

### Linear Read Preflight

| Check | Result | Notes |
|---|---|---|
| Linear team list | One team found | `DvdTeacher` (`dccbecac-8445-458f-9f6b-d16f826c3c91`) |
| Project search: `AI Project OS` | No results | Safe to create after approval |
| Full project list | Empty | No existing project to overwrite |
| Issue search: `AIPOS` | No results | Low duplicate risk |
| Full-text search: `"AI Project OS"` | No results | Low duplicate risk |
| Existing unrelated issues | `DVD-1`, `DVD-2` | Default Linear onboarding issues; skip |
| Existing labels | `Feature`, `Bug`, `Improvement` | Field-mapping decision required before creating `type:*` labels |

### Available Linear Statuses

| Status | Linear Type |
|---|---|
| Backlog | backlog |
| Todo | unstarted |
| In Progress | started |
| In Review | started |
| Done | completed |
| Duplicate | duplicate |
| Canceled | canceled |

### Final Status Mapping

| AI Project OS Status | Linear Status | Notes |
|---|---|---|
| Backlog | Backlog | Direct match |
| Needs Decision | Todo | Use `type:decision` label and blocking text in description |
| Ready | Todo | Direct working queue |
| In Progress | In Progress | Direct match |
| In Review | In Review | Direct match |
| Ready for UAT | In Review | Closest available status; UAT details remain in description |
| Accepted | Done | Only after human UAT |
| Released | Done | Only after tag/release facts exist |
| Duplicate Candidate | Duplicate | Do not use automatically without human confirmation |
| Deferred | Backlog | Add note in description |
| Won't Do | Canceled | Do not use automatically without human confirmation |

### Label Mapping Decision

Linear currently has title-case default labels: `Feature`, `Bug`, `Improvement`.

AI Project OS policy recommends namespaced labels such as `type:feature` and `module:linear`.

Recommended Phase 3 import behavior:

| Label | Action | Risk |
|---|---|---|
| module:core | Create | Low |
| module:init | Create | Low |
| module:linear | Create | Low |
| module:github | Create | Low |
| module:release | Create | Low |
| module:upgrade | Create | Low |
| module:package | Create | Low |
| module:quality | Create | Low |
| module:docs | Create | Low |
| type:feature | Create | Medium; overlaps existing `Feature` |
| type:decision | Create | Low |
| type:chore | Create | Low |

Alternative conservative behavior:

| OS Label | Existing Label | Notes |
|---|---|---|
| type:feature | Feature | Avoids duplicate type label |
| type:bug | Bug | Not used in this import |
| type:chore | Improvement | Possible but less precise |

### Final Write List

This was the approved create-only list. Import completed on 2026-08-18.

#### Project

| Project | Team | Version | Duplicate Risk |
|---|---|---|---|
| AI Project OS v0.1 | DvdTeacher | v0.1.0 | Low |

#### Batch 1: v0.1.0 Project Issues

| Feature ID | Title | Type | Module | Target Version | OS Status | Linear Status | Labels | Depends On | Duplicate Risk |
|---|---|---|---|---|---|---|---|---|---|
| AIPOS-001 | Distributable `project-os/` lazy pack | feature | package | v0.1.0 | Ready for UAT | In Review | module:package,type:feature |  | Low |
| AIPOS-002 | Phase 0 Self-Check | feature | init | v0.1.0 | Ready for UAT | In Review | module:init,type:feature |  | Low |
| AIPOS-003 | Phase 1 Audit output specs | feature | init | v0.1.0 | Ready for UAT | In Review | module:init,type:feature |  | Low |
| AIPOS-004 | Linear MCP import policy | feature | linear | v0.1.0 | Ready for UAT | In Review | module:linear,type:feature |  | Low |
| AIPOS-005 | GitHub private repo and PR policy | feature | github | v0.1.0 | Ready for UAT | In Review | module:github,type:feature |  | Low |
| AIPOS-006 | OS versioning and upgrade policy | feature | upgrade | v0.1.0 | Ready for UAT | In Review | module:upgrade,type:feature |  | Low |
| AIPOS-007 | Release and UAT governance | feature | release | v0.1.0 | Ready for UAT | In Review | module:release,type:feature |  | Low |
| AIPOS-008 | Generate v0.1.0 release zip | chore | package | v0.1.0 | Ready for UAT | In Review | module:package,type:chore | AIPOS-001 | Low |

#### Batch 1: Decision Issues

| Decision ID | Title | Linear Status | Blocking | Owner | Needed By | Notes |
|---|---|---|---|---|---|---|
| DEC-001 | Choose Linear team for AI Project OS | Todo until confirmed, then Done | Yes | Owner | Before Phase 3 import | Must confirm `DvdTeacher` before any write |
| DEC-002 | Confirm private GitHub repo owner/name | Done | No | Owner | Completed | Final decision: `adwasd-dvd/ai-project-os` |
| DEC-003 | Decide whether release zips are committed or GitHub-release-only | Todo | No | Owner | Before v0.1.0 release | Recommendation: GitHub Releases only |

#### Batch 2: v0.2.0 Backlog

| Feature ID | Title | Type | Module | Target Version | OS Status | Linear Status | Labels | Depends On | Duplicate Risk |
|---|---|---|---|---|---|---|---|---|---|
| AIPOS-009 | Add automated policy validator | feature | quality | v0.2.0 | Backlog | Backlog | module:quality,type:feature |  | Low |
| AIPOS-010 | Add worked example for first real project | feature | docs | v0.2.0 | Backlog | Backlog | module:docs,type:feature |  | Low |

### Updated Approval Block

```text
- [x] Baseline drafted.
- [x] Baseline confirmed.
- [x] Linear app connected.
- [x] Linear team confirmed.
- [x] Duplicate candidates reviewed.
- [x] Status mapping confirmed.
- [x] Label mapping confirmed.
- [x] First bulk write approved.
```

Confirmation phrase received:

```text
Baseline 确认。Linear team 使用 DvdTeacher。状态映射确认。标签使用 namespaced OS labels。批准写入 Linear。
```

### Write Self-Check

| Check | Current Answer |
|---|---|
| Is this the first bulk write? | Yes |
| Has a human authorized the write? | Yes |
| Could this create duplicate issues? | Low issue/project risk; label mapping was explicitly confirmed |
| Will this modify existing Linear content? | No, proposed writes are create-only |
| Does this involve status changes? | No updates to existing issues; new issues need initial statuses |
| Are there business uncertainties? | No import-blocking uncertainty remains; DEC-003 remains open for release policy |

## Phase 3 Import Result - 2026-08-18

### Created Project

| Linear ID | Name | URL |
|---|---|---|
| `1ef51e67-aae6-4c89-bce8-21cfde105def` | AI Project OS v0.1 | https://linear.app/dvdteacher/project/ai-project-os-v01-43119fd36ee5 |

### Created Labels

```text
module:core
module:init
module:linear
module:github
module:release
module:upgrade
module:package
module:quality
module:docs
type:feature
type:decision
type:chore
```

### Created Issues

| Linear ID | Source ID | Title | Status |
|---|---|---|---|
| DVD-5 | AIPOS-001 | Distributable `project-os/` lazy pack | In Review |
| DVD-6 | AIPOS-002 | Phase 0 Self-Check | In Review |
| DVD-7 | AIPOS-003 | Phase 1 Audit output specs | In Review |
| DVD-8 | AIPOS-004 | Linear MCP import policy | In Review |
| DVD-9 | AIPOS-005 | GitHub private repo and PR policy | In Review |
| DVD-10 | AIPOS-006 | OS versioning and upgrade policy | In Review |
| DVD-11 | AIPOS-007 | Release and UAT governance | In Review |
| DVD-12 | AIPOS-008 | Generate v0.1.0 release zip | In Review |
| DVD-13 | DEC-001 | Choose Linear team for AI Project OS | Done |
| DVD-14 | DEC-002 | Confirm private GitHub repo owner/name | Done |
| DVD-15 | DEC-003 | Decide whether release zips are committed or GitHub-release-only | Todo |
| DVD-16 | AIPOS-009 | Add automated policy validator | Backlog |
| DVD-17 | AIPOS-010 | Add worked example for first real project | Backlog |

### Verification

```text
Project readback: OK
Issue readback: 13 imported issues found under project
Label readback: 12 namespaced OS labels found
Skipped: existing Linear onboarding issues DVD-1 and DVD-2
Failed: 0
```

## v0.2 Implementation Linear Update - 2026-08-19

### Project

| Linear ID | Name | Status | Notes |
|---|---|---|---|
| `a6e24ed6-d562-48b7-b3c3-313699badc64` | AI Project OS v0.2 | In Progress | Project status update posted with bilingual summary and verification results |

### Decisions

| Linear ID | Source ID | Status | Notes |
|---|---|---|---|
| DVD-18 | DEC-004 | Done | Automation boundary confirmed before implementation |
| DVD-23 | DEC-005 | Done | v0.2 scope and sequence confirmed before implementation |

### Issues Moved To Review

| Linear ID | Source ID | Status | Implementation Evidence |
|---|---|---|---|
| DVD-16 | AIPOS-009 | In Review | `project-os/tools/validate_project_os.py` |
| DVD-17 | AIPOS-010 | In Review | `project-os/examples/FIRST_PROJECT.md` |
| DVD-19 | AIPOS-011 | In Review | `AUTOMATION_POLICY.md`, `LINEAR_INTAKE.md` |
| DVD-20 | AIPOS-012 | In Review | `REQUIREMENT_MANAGEMENT.md` |
| DVD-21 | AIPOS-013 | In Review | `VERSION_PLANNING.md` |
| DVD-22 | AIPOS-014 | In Review | `START_HERE.md`, `LINEAR_INTAKE.md` |
| DVD-24 | AIPOS-015 | In Review | `LINEAR_INTAKE.md` |
| DVD-25 | AIPOS-016 | In Review | `AUTOMATION_POLICY.md` |
| DVD-26 | AIPOS-017 | In Review | `LINEAR_POLICY.md`, `UAT_TEMPLATE.md` |
| DVD-27 | AIPOS-018 | In Review | `RELEASE_POLICY.md`, `VERSION_PLANNING.md` |

### Verification

```text
python3 project-os/tools/validate_project_os.py --root .
python3 template/project-os/tools/validate_project_os.py --root .
python3 -m py_compile project-os/tools/validate_project_os.py template/project-os/tools/validate_project_os.py
unzip -t releases/ai-project-os-v0.2.0.zip
```

Result:

```text
Passed
```

### Remaining Human Gate

v0.2 is implemented and ready for human review/UAT.

Do not move AIPOS-009 through AIPOS-018 to `Done` until the Owner gives an explicit UAT/sign-off conclusion.

## v0.2 Closeout Linear Update - 2026-08-19

Owner approved proceeding on 2026-08-19. Codex recorded v0.2 UAT as Pass, moved AIPOS-009 through AIPOS-018 to `Done`, posted a bilingual project status update, and completed the v0.2 Linear project.

Owner 于 2026-08-19 批准继续。Codex 已记录 v0.2 UAT Pass，将 AIPOS-009 到 AIPOS-018 移到 `Done`，发布双语项目状态更新，并完成 v0.2 Linear project。

## v0.3 Implementation Linear Update - 2026-08-19

### Project

| Linear ID | Name | Status | Notes |
|---|---|---|---|
| `8d1e72c7-e0f1-4eff-bcb6-b883f4c37ce9` | AI Project OS v0.3 | In Progress | Project created for assignee-driven Human/Codex handoff |

### Decisions

| Linear ID | Source ID | Status | Notes |
|---|---|---|---|
| DVD-51 | DEC-006 | Done | Assignee-driven handoff model confirmed from Owner discussion |

### Issues Moved To Review

| Linear ID | Source ID | Status | Assignee | Implementation Evidence |
|---|---|---|---|---|
| DVD-52 | AIPOS-019 | In Review | dvdTeacher | `LINEAR_POLICY.md`, `WORKFLOW.md`, `PROJECT.md`, `START_HERE.md` |
| DVD-53 | AIPOS-020 | In Review | dvdTeacher | `LINEAR_INTAKE.md`, `AUTOMATION_POLICY.md`, `QUALITY_GATE.md`, `AGENTS.md` |
| DVD-54 | AIPOS-021 | In Review | dvdTeacher | `START_HERE.md`, `UAT_TEMPLATE.md`, `examples/FIRST_PROJECT.md` |
| DVD-55 | AIPOS-022 | In Review | dvdTeacher | `tools/validate_project_os.py`, `ROADMAP.md` |
| DVD-56 | AIPOS-023 | In Review | dvdTeacher | `ROADMAP.md`, `README.md`, `CHANGELOG.md`, `PROJECT.md` |

### Verification

```text
python3 project-os/tools/validate_project_os.py --root .
python3 template/project-os/tools/validate_project_os.py --root .
python3 -m py_compile project-os/tools/validate_project_os.py template/project-os/tools/validate_project_os.py
unzip -t releases/ai-project-os-v0.3.0.zip
```

Result:

```text
Passed
```

### Remaining Human Gate

v0.3 is implemented and ready for human review/UAT.

Do not move AIPOS-019 through AIPOS-023 to `Done` until the Owner gives an explicit UAT/sign-off conclusion.
