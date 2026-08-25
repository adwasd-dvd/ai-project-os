# VERSION CLOSEOUT v0.8.0

This checklist records the candidate closeout state for Development Train B.

本清单记录 Development Train B 的候选版关账状态。

## Current State

```text
Version: v0.8.0
Status: Candidate - Human UAT Pending
Date Prepared: 2026-08-25
Prepared By: Codex
Human UAT: Pending
GitHub: Draft PR #7 open; tag and Release not created
Publication Decision: Review
```

## Release Gates

| Gate | Evidence | Status |
|---|---|---|
| Scope confirmed | DEC-009 + Train B Project Document | Pass |
| Included features implemented | AIPOS-045 through AIPOS-051 | Pass |
| Change impact | `CHANGE_IMPACT_REPORT_v0.8.0.md` | Pass |
| Traceability | `TRACEABILITY_REPORT_v0.8.0.md` | Pass for declared candidate state |
| Source validator/tests | 0 failures, 0 warnings; 59/59 tests | Pass |
| Deterministic package | two identical builds; recorded digest | Pass |
| Extracted package | archive, validator, 59/59 tests | Pass |
| Upgrade dogfood | v0.6.0 to v0.8.0; protected memory preserved | Pass |
| Private safety gate | Block 0; Review 0 in isolated dogfood | Pass |
| GitHub review | Draft PR #7 open and merge state clean | Pass for candidate handoff |
| Human UAT | explicit Owner conclusion | Pending |
| Publication manifest | human Go | Pending |
| Tag and GitHub Release | only after UAT and Go | Pending |
| Post-release verification | remote digest and checks | Pending |
| Linear closeout | project completion and final update | Pending |

## Remaining Authorized Sequence / 剩余授权顺序

1. Create and review the Draft PR.
2. Owner completes `UAT_v0.8.0.md` and explicitly passes or fails.
3. On Pass, record accepted traceability and publication Go.
4. Merge the approved PR, build from the merge commit, and re-run final gates.
5. Create tag `v0.8.0`, publish the verified zip, and verify the remote digest.
6. Record post-release checks, update stable links, and close the Linear Project.

1. 创建并审查 Draft PR。
2. Owner 完成 `UAT_v0.8.0.md` 并明确通过或失败。
3. 通过后记录 accepted traceability 和 publication Go。
4. 合并已批准 PR，从 merge commit 构建并重跑最终门禁。
5. 创建 `v0.8.0` tag，发布已验证 zip，并核对远端摘要。
6. 记录发布后检查、更新 stable 链接并关闭 Linear Project。

## Current Decision / 当前决定

```text
Technically verified candidate. Human UAT and publication remain pending.
候选版已完成技术验证，人工 UAT 与发布仍待批准。
```
