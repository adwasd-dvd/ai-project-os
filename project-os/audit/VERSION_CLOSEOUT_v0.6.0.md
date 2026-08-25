# VERSION_CLOSEOUT v0.6.0 Candidate

This checklist records the pre-release closeout state for Development Train A.

本清单记录 Development Train A 的发布前关账状态。

## Current State

```text
Version: v0.6.0 candidate
Status: In Review preparation
Date Prepared: 2026-08-24
Prepared By: Codex
Human UAT: Pending
GitHub: branch codex/v0.6-train-a; Draft PR https://github.com/adwasd-dvd/ai-project-os/pull/4
Publication Decision: Review
```

## Required Before Release

| Gate | Required Evidence | Current Evidence | Status |
|---|---|---|---|
| Scope confirmed | DEC-009 Done | DVD-218 Done | Pass |
| Included features implemented | AIPOS-038 through AIPOS-044 | Local candidate implementation | Pass |
| Change impact | Seven areas, no blocker | `CHANGE_IMPACT_REPORT_v0.6.0.md`: READY | Pass |
| Traceability | Every included feature justified as `uat_pending` | `TRACEABILITY_REPORT_v0.6.0.md` | Pass |
| Source/template validator | 0 failures, 0 warnings | Source and extracted package both clean | Pass |
| Automated tests | Full source suite | Source 36/36; extracted package 36/36 | Pass |
| Safety gates | Private Block 0; public advisory classified | Staged private Block 0 / Review 0; staged public Block 0 / 13 expected review items | Pass |
| Candidate zip | Correct root, digest, standalone validation/tests | SHA-256 `c453e8732a4b77907055ebb82fb980a864201a7ffefd090d3ac2f95a4c65f217`; archive/validation/tests pass | Pass |
| GitHub review | Dedicated Draft PR | PR #4 created and kept Draft for Owner UAT | Pass |
| Linear handoff | DVD-219 through DVD-225 In Review + Owner | Pending | Pending |
| Human UAT | Explicit Owner conclusion | Pending | Block |
| Publication manifest | Human Go | Review | Block |

## Actions Only After UAT Pass / 仅 UAT 通过后执行

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

Do not perform these closeout actions before explicit human UAT Pass.

在明确人工 UAT Pass 前，不执行这些关账动作。
