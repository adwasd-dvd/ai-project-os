# VERSION_CLOSEOUT v0.5.0

This checklist records the AI Project OS v0.5.0 release closeout state.

本清单记录 AI Project OS v0.5.0 的发布关账状态。

## Current State

```text
Version: v0.5.0
Status: Released
Date Prepared: 2026-08-20
Prepared By: Codex
Human UAT: Pass - Owner approved 2026-08-20
GitHub: PR #3; tag v0.5.0; https://github.com/adwasd-dvd/ai-project-os/releases/tag/v0.5.0
Publication Decision: Go for current PRIVATE GitHub destination
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
| Release digest | SHA-256 recorded | `fb242467d1729c5cbee09cb06e5c06aabbcc234d8970b696026be19d3e8495dd` | Pass |
| Staged/private gate | Block 0 | Block 0, Review 0, Go | Pass |
| Public/tracked advisory | Block 0 + Review dispositions | Block 0; 30 Private Repo memory records and 2 Team Shared Agent docs; future public reclassification required | Pass for advisory, not public approval |
| GitHub review surface | Dedicated branch and Draft PR | `codex/v0.5-repo-safety`; PR #3 | Pass |
| Linear UAT handoff | Issues In Review + Owner, bilingual evidence | DVD-83 through DVD-89 In Review + dvdTeacher; project update `f71da708-bb04-4dd7-bcb5-2f20fa4a26d0` | Pass |
| Human UAT | Explicit Owner conclusion | `UAT 通过，允许发布 v0.5.0。` | Pass |
| Publication manifest | Human Go | Go for current PRIVATE GitHub destination | Pass |
| GitHub release/tag | Only after UAT | `v0.5.0`; release URL recorded above | Pass |

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
Human UAT passed. v0.5.0 is approved for release and closeout.
人类 UAT 已通过。v0.5.0 已批准发布并关账。
```
