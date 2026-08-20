# VERSION_CLOSEOUT v0.4.0

This checklist records the AI Project OS v0.4.0 closeout state.

本清单记录 AI Project OS v0.4.0 的版本关账状态。

## Current State

```text
Version: v0.4.0
Status: Ready for Human UAT
Date Prepared: 2026-08-19
Prepared By: Codex
Human UAT: Pending
GitHub: Draft PR https://github.com/adwasd-dvd/ai-project-os/pull/2; no v0.4 tag or release
```

## Required Before Release

| Gate | Required Evidence | Current Evidence | Status |
|---|---|---|---|
| Scope confirmed | DEC-007 Done | DVD-58 Done | Pass |
| Included features implemented | AIPOS-024 through AIPOS-030 with evidence comments | DVD-59 through DVD-65 `In Review`, assigned to dvdTeacher, with bilingual evidence comments | Pass |
| Source validator | Strict validator passes | 0 failures, 0 warnings | Pass |
| Template validator | Strict validator passes | 0 failures, 0 warnings | Pass |
| Scanner tests | Source and template tests pass | 8 tests passed | Pass |
| Release zip | Top-level `project-os/`, archive test clean | `releases/ai-project-os-v0.4.0.zip`; `unzip -t` passed | Pass |
| GitHub review surface | Clean dedicated branch and Draft PR | `codex/v0.4-whitebox`; PR #2 | Pass |
| Human UAT | Explicit human conclusion | Not received | Pending |
| Linear closeout | Included issues Done only after UAT | Not allowed yet | Pending |
| GitHub release/tag | Publish only after UAT | Not allowed yet | Pending |

## Closeout Actions After UAT Passes

Only perform these after the Owner gives:

```text
UAT 通过，允许发布 v0.4.0。
```

1. Record the UAT result and update release notes.
2. Move DVD-59 through DVD-65 to `Done` and complete the v0.4 Linear project.
3. Mark the GitHub PR ready, merge it, and confirm `main` is clean.
4. Create and push the `v0.4.0` tag.
5. Publish a GitHub Release and attach `ai-project-os-v0.4.0.zip`.
6. Run final validator, scanner test, archive, and remote-reference checks.

## Closeout Decision

```text
Implementation may enter human UAT after all pending technical and handoff gates pass.
全部技术与交接门槛通过后，实现可以进入人类 UAT。
```
