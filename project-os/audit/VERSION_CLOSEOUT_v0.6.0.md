# VERSION_CLOSEOUT v0.6.0

This checklist records the approved release closeout state for Development Train A.

本清单记录 Development Train A 已批准的发布关账状态。

## Current State

```text
Version: v0.6.0
Status: Approved for release
Date Prepared: 2026-08-25
Prepared By: Codex
Human UAT: Pass - Owner approved 2026-08-25
GitHub: branch codex/v0.6-train-a; PR https://github.com/adwasd-dvd/ai-project-os/pull/4
Publication Decision: Go for current PRIVATE GitHub destination
```

## Required Before Release

| Gate | Required Evidence | Current Evidence | Status |
|---|---|---|---|
| Scope confirmed | DEC-009 Done | DVD-218 Done | Pass |
| Included features implemented | AIPOS-038 through AIPOS-044 | Local candidate implementation | Pass |
| Change impact | Seven areas, no blocker | `CHANGE_IMPACT_REPORT_v0.6.0.md`: READY | Pass |
| Traceability | Every included feature justified as `accepted` | `TRACEABILITY_REPORT_v0.6.0.md` | Pass |
| Source/template validator | 0 failures, 0 warnings | Source and extracted package both clean | Pass |
| Automated tests | Full source suite | Source 38/38; extracted deterministic package pending final rebuild | Pending |
| Safety gates | Private Block 0; public advisory classified | Staged private Block 0 / Review 0; staged public Block 0 / 13 expected review items | Pass |
| Release zip | Correct root, digest, standalone validation/tests | Pending deterministic rebuild from merged release-fix commit | Pending |
| GitHub review | Dedicated Draft PR | PR #4 created and kept Draft for Owner UAT | Pass |
| Linear handoff | DVD-219 through DVD-225 In Review + Owner | Completed; project update `1e2cd8a5-0f80-4828-a692-6ab6ffc9da1c` | Pass |
| Human UAT | Explicit Owner conclusion | `UAT 通过，允许发布 v0.6.0。` | Pass |
| Publication manifest | Human Go | Go for current PRIVATE GitHub destination | Pass |
| GitHub release/tag | Only after UAT | Authorized; pending release transaction | Pending |

## Authorized Release Actions / 已批准发布动作

```text
UAT 通过，允许发布 v0.6.0。
```

1. Record human UAT Pass and update traceability features from `uat_pending` to `accepted`.
2. Change publication decision from Review to Go.
3. Mark the Draft PR ready and merge it.
4. Run final release-commit validation and safety gates.
5. Build the final zip from the merge commit and record its SHA-256.
6. Create and push tag `v0.6.0`; publish the GitHub Release asset.
7. Verify the remote asset digest.
8. Update traceability to `released`, then complete DVD-219 through DVD-225 and the Linear project.

## Closeout Decision / 关账决定

```text
Human UAT passed. v0.6.0 is approved for release and closeout.
人类 UAT 已通过。v0.6.0 已批准发布并关账。
```
