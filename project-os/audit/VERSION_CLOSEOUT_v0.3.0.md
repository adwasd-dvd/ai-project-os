# VERSION_CLOSEOUT v0.3.0

This checklist records the AI Project OS v0.3.0 closeout state.

本清单记录 AI Project OS v0.3.0 的版本关账状态。

## Current State

```text
Version: v0.3.0
Status: Released
Date Prepared: 2026-08-19
Prepared By: Codex
Human UAT: Pass - Owner approved 2026-08-19
Release: Local package approved; GitHub v0.3.0 publication approved
```

## Required Before Done

| Gate | Required Evidence | Current Evidence | Status |
|---|---|---|---|
| Scope confirmed | DEC-006 Done | DVD-51 Done | Pass |
| Included features implemented | AIPOS-019 through AIPOS-023 in review with implementation comments | DVD-52, DVD-53, DVD-54, DVD-55, DVD-56 in `In Review` with bilingual implementation comments | Pass |
| Local validator | Validator output passes | `python3 project-os/tools/validate_project_os.py --root .` passed | Pass |
| Template validator | Template validator output passes | `python3 template/project-os/tools/validate_project_os.py --root .` passed | Pass |
| Python syntax | Validator compiles | `python3 -m py_compile ...` passed | Pass |
| Release zip | Zip exists and tests clean | `releases/ai-project-os-v0.3.0.zip`, `unzip -t` passed | Pass |
| Human UAT | Explicit human conclusion | Owner: `UAT 通过，允许发布 v0.3.0。` | Pass |
| Linear closeout | Issues moved to Done after UAT | DVD-51 through DVD-56 Done; v0.3 project Completed; bilingual status update posted | Pass |
| GitHub release/tag | Tag/release or explicit skip decision | `v0.3.0`; release asset `ai-project-os-v0.3.0.zip` | Pass |

## Closeout Actions After UAT Passes

Only perform these after the Owner gives:

```text
UAT 通过，允许发布 v0.3.0。
```

Actions:

1. Update `project-os/audit/UAT_v0.3.0.md` with the human UAT result.
2. Update `project-os/audit/RELEASE_NOTES_v0.3.0.md` UAT and GitHub sections.
3. Move AIPOS-019 through AIPOS-023 Linear issues to `Done`.
4. Post a bilingual Linear project status update recording UAT pass and closeout.
5. Complete the Linear v0.3 project if all included issues are Done.
6. If requested, create GitHub tag/release or record the Owner decision to defer GitHub release.
7. Run final validator and zip checks.

## Closeout Actions If UAT Fails

If the Owner says:

```text
UAT 未通过，必须先处理以下问题：
-
```

Actions:

1. Add each issue to `project-os/audit/UAT_v0.3.0.md`.
2. Classify each issue as Current Fix, Patch, Next, Backlog, or Decision.
3. Create/update Linear issues with target versions.
4. Do not move v0.3 included issues to `Done`.
5. Re-run validation after fixes.

## Closeout Decision

```text
Human UAT passed and Linear closeout completed. v0.4 may start.
人工 UAT 已通过，Linear 关账已完成。可启动 v0.4。
```
