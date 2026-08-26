# VERSION CLOSEOUT v0.8.0

This checklist records the candidate closeout state for Development Train B.

本清单记录 Development Train B 的候选版关账状态。

## Current State

```text
Version: v0.8.0
Status: Accepted - Release Authorized
Date Prepared: 2026-08-26
Prepared By: Codex
Human UAT: Pass - Owner approved 2026-08-26
GitHub: Draft PR #7 open; tag and Release not created
Publication Decision: Go
```

## Release Gates

| Gate | Evidence | Status |
|---|---|---|
| Scope confirmed | DEC-009 + Train B Project Document | Pass |
| Included features implemented | AIPOS-045 through AIPOS-051 | Pass |
| Change impact | `CHANGE_IMPACT_REPORT_v0.8.0.md` | Pass |
| Traceability | `TRACEABILITY_REPORT_v0.8.0.md` | Pass for declared candidate state |
| Source validator/tests | 0 failures, 0 warnings; 59/59 tests | Pass |
| Deterministic package | two identical final builds; SHA-256 `cf9989b993b28689da367d532db233a6d369a8edbe041712951ddc5e99cdfc1f` | Pass |
| Extracted package | archive, validator, 59/59 tests from final release-metadata package | Pass |
| Upgrade dogfood | v0.6.0 to v0.8.0; protected memory preserved | Pass |
| Private safety gate | Block 0; Review 0 in isolated dogfood | Pass |
| GitHub review | Draft PR #7 open and merge state clean | Pass for candidate handoff |
| Human UAT | `UAT 通过，允许发布 v0.8.0。` | Pass |
| Publication manifest | human Go | Pass |
| Tag and GitHub Release | only after UAT and Go | Pending |
| Post-release verification | remote digest and checks | Pending |
| Linear UAT handoff | Project update `8ef6411d-303b-4eb4-b5ff-31d3ab2bbc64`; Project remains In Progress | Pass for candidate handoff |
| Linear release closeout | Project completion and final post-release update | Pending |

## Remaining Authorized Sequence / 剩余授权顺序

1. [x] Create and review the Draft PR.
2. [x] Owner completes `UAT_v0.8.0.md` and explicitly passes.
3. [x] Record accepted traceability and publication Go.
4. [ ] Merge the approved PR, build from the merge commit, and re-run final gates.
5. [ ] Create tag `v0.8.0`, publish the verified zip, and verify the remote digest.
6. [ ] Record post-release checks, update stable links, and advance the canonical Linear Project to v1.0.0.

1. [x] 创建并审查 Draft PR。
2. [x] Owner 完成 `UAT_v0.8.0.md` 并明确通过。
3. [x] 记录 accepted traceability 和 publication Go。
4. [ ] 合并已批准 PR，从 merge commit 构建并重跑最终门禁。
5. [ ] 创建 `v0.8.0` tag，发布已验证 zip，并核对远端摘要。
6. [ ] 记录发布后检查、更新 stable 链接，并将唯一 Linear Project 推进到 v1.0.0。

## Current Decision / 当前决定

```text
Owner passed human UAT and authorized the v0.8.0 release transaction.
Owner 已通过人工 UAT，并授权执行 v0.8.0 发布事务。
```
