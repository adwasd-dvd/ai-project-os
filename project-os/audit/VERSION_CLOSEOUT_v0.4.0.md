# VERSION_CLOSEOUT v0.4.0

This checklist records the AI Project OS v0.4.0 closeout state.

本清单记录 AI Project OS v0.4.0 的版本关账状态。

## Current State

```text
Version: v0.4.0
Status: Released
Date Prepared: 2026-08-19
Prepared By: Codex
Human UAT: Pass - Owner approved 2026-08-19
GitHub: PR #2; tag v0.4.0; https://github.com/adwasd-dvd/ai-project-os/releases/tag/v0.4.0
```

## Required Before Release

| Gate | Required Evidence | Current Evidence | Status |
|---|---|---|---|
| Scope confirmed | DEC-007 Done | DVD-58 Done | Pass |
| Included features implemented | AIPOS-024 through AIPOS-030 with evidence comments | DVD-59 through DVD-65 `In Review`, assigned to dvdTeacher, with bilingual evidence comments | Pass |
| Source validator | Strict validator passes | 0 failures, 0 warnings | Pass |
| Template validator | Strict validator passes | 0 failures, 0 warnings | Pass |
| Automated tests | Source/template scanner and validator-layout tests pass | 10 tests passed | Pass |
| Release zip | Top-level `project-os/`, archive and standalone strict validation clean | `releases/ai-project-os-v0.4.0.zip`; archive and extracted-package validation passed | Pass |
| GitHub review surface | Clean dedicated branch and Draft PR | `codex/v0.4-whitebox`; PR #2 | Pass |
| Human UAT | Explicit human conclusion | Owner: `UAT 通过，允许发布 v0.4.0。` | Pass |
| Linear closeout | Included issues Done only after UAT | DVD-58 through DVD-65 Done; v0.4 project Completed | Pass |
| GitHub release/tag | Publish only after UAT | `v0.4.0`; release asset `ai-project-os-v0.4.0.zip` | Pass |

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
Human UAT passed. v0.4.0 is approved for release and closeout.
人类 UAT 已通过。v0.4.0 已批准发布并关账。
```
