# VERSION_CLOSEOUT v0.5.0

This checklist records the AI Project OS v0.5.0 candidate closeout state.

本清单记录 AI Project OS v0.5.0 的候选关账状态。

## Current State

```text
Version: v0.5.0
Status: Ready for human UAT
Date Prepared: 2026-08-20
Prepared By: Codex
Human UAT: Pending
GitHub: branch codex/v0.5-repo-safety; Draft PR https://github.com/adwasd-dvd/ai-project-os/pull/3
Publication Decision: Review for current PRIVATE GitHub destination
```

## Required Before Release

| Gate | Required Evidence | Current Evidence | Status |
|---|---|---|---|
| Scope confirmed | DEC-008 Done | DVD-82 Done | Pass |
| Included features implemented | AIPOS-031 through AIPOS-037 | Local implementation complete | Pass |
| Source/template validator | Strict validator passes | 0 failures, 0 warnings | Pass |
| Automated tests | Validator + whitebox + safety scanner tests | 10 passed | Pass |
| Safety dry run | No Block/Review in local worktree | Block 0, Review 0, Go | Pass |
| Release zip | Correct root and standalone validation | `ai-project-os-v0.5.0.zip`, passed | Pass |
| Release digest | SHA-256 recorded | `75eee07ddc40075399ae237044676dfb419f257c7e55461c04205d1fdda44120` | Pass |
| Staged/private gate | Block 0 | Block 0, Review 0, Go | Pass |
| Public/tracked advisory | Block 0 + Review dispositions | Block 0; 30 Private Repo memory records and 2 Team Shared Agent docs; future public reclassification required | Pass for advisory, not public approval |
| GitHub review surface | Dedicated branch and Draft PR | `codex/v0.5-repo-safety`; PR #3 | Pass |
| Linear UAT handoff | Issues In Review + Owner, bilingual evidence | Pending | Pending |
| Human UAT | Explicit Owner conclusion | Pending | Pending |
| Publication manifest | Human Go | Review pending Owner | Pending |
| GitHub release/tag | Only after UAT | Not created | Correctly blocked |

## Closeout Actions After UAT Passes

Only perform these after the Owner gives:

```text
UAT 通过，允许发布 v0.5.0。
```

1. Record the UAT result and change the publication decision from Review to Go.
2. Move DVD-83 through DVD-89 to `Done` and complete the v0.5 Linear project.
3. Mark the GitHub Draft PR ready, merge it, and verify `main`.
4. Run the final tracked/private gate against the release commit; retain public/tracked results as advisory only.
5. Create and push tag `v0.5.0`.
6. Publish the GitHub Release with `ai-project-os-v0.5.0.zip`.
7. Compare the remote asset SHA-256 and update permanent evidence links.

## Closeout Decision

```text
Human UAT is pending. v0.5.0 must not be merged, tagged, released, or marked complete yet.
人工 UAT 尚未完成。v0.5.0 暂不得合并、打 tag、发布或标记完成。
```
