# VERSION CLOSEOUT v0.8.0

This checklist records the completed release closeout state for Development Train B.

本清单记录 Development Train B 已完成的发布关账状态。

## Current State

```text
Version: v0.8.0
Status: Released - Post-Release Verified
Date Prepared: 2026-08-26
Prepared By: Codex
Human UAT: Pass - Owner approved 2026-08-26
GitHub: PR #7 merged; tag v0.8.0; https://github.com/adwasd-dvd/ai-project-os/releases/tag/v0.8.0
Merge Commit: 4cd2412f06f7fe1e368c1efafa862bd62f560a4e
Publication Decision: Published to current PRIVATE GitHub destination
```

## Release Gates

| Gate | Evidence | Status |
|---|---|---|
| Scope confirmed | DEC-009 + Train B Project Document | Pass |
| Included features implemented | AIPOS-045 through AIPOS-051 | Pass |
| Change impact | `CHANGE_IMPACT_REPORT_v0.8.0.md` | Pass |
| Traceability | `TRACEABILITY_REPORT_v0.8.0.md` | Pass for released state |
| Source validator/tests | 0 failures, 0 warnings; 59/59 tests | Pass |
| Deterministic package | two identical final builds; SHA-256 `cf9989b993b28689da367d532db233a6d369a8edbe041712951ddc5e99cdfc1f` | Pass |
| Extracted package | archive, validator, 59/59 tests from final release-metadata package | Pass |
| Upgrade dogfood | v0.6.0 to v0.8.0; protected memory preserved | Pass |
| Private safety gate | Block 0; Review 0 in isolated dogfood | Pass |
| GitHub review | PR #7 merged to `main` | Pass |
| Human UAT | `UAT 通过，允许发布 v0.8.0。` | Pass |
| Publication manifest | human Go | Pass |
| Tag and GitHub Release | tag points to merge commit; Release asset published | Pass |
| Post-release verification | `POST_RELEASE_RECEIPT_v0.8.0.md`; remote asset byte-identical | Pass |
| Linear UAT handoff | Project update `8ef6411d-303b-4eb4-b5ff-31d3ab2bbc64`; Project remains In Progress | Pass for candidate handoff |
| Linear release closeout | v0.8 Milestone released; update `fcc2a3c0-70eb-4002-87e5-c4d0a44d3bed`; canonical Project remains active for v1.0 | Pass |

## Authorized Release Sequence / 已批准发布顺序

1. [x] Create and review the Draft PR.
2. [x] Owner completes `UAT_v0.8.0.md` and explicitly passes.
3. [x] Record accepted traceability and publication Go.
4. [x] Merge the approved PR, build the final package, and re-run final gates.
5. [x] Create tag `v0.8.0`, publish the verified zip, and verify the remote digest.
6. [x] Record post-release checks, update stable links, and advance the canonical Linear Project to v1.0.0.

1. [x] 创建并审查 Draft PR。
2. [x] Owner 完成 `UAT_v0.8.0.md` 并明确通过。
3. [x] 记录 accepted traceability 和 publication Go。
4. [x] 合并已批准 PR，构建最终安装包并重跑最终门禁。
5. [x] 创建 `v0.8.0` tag，发布已验证 zip，并核对远端摘要。
6. [x] 记录发布后检查、更新 stable 链接，并将唯一 Linear Project 推进到 v1.0.0。

## Closeout Decision / 关账决定

```text
Human UAT passed. v0.8.0 was released and post-release verification passed.
人工 UAT 已通过。v0.8.0 已成功发布，发布后验证通过。
```
