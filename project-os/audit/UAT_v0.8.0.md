# UAT v0.8.0 - Development Train B

## UAT Header

```text
Version: v0.8.0
Date: 2026-08-26
Environment: local source repo + isolated v0.6-to-v0.8 dogfood + GitHub Draft PR
Build / Commit: package source 6ea9e8fe4b004f415c530a118f9f28fa02931e11; accepted PR head 86696a3d37fc4501e9ea970d979bf26b0ae4340f
Candidate SHA-256: ec81d2439a4802fc19e1d03cc3a9b7bd739c7c92cd37af4134385d016bd3df92
Final release-metadata package SHA-256: cf9989b993b28689da367d532db233a6d369a8edbe041712951ddc5e99cdfc1f
Tester: Owner / dvdTeacher
Owner: dvdTeacher
Result: Pass
```

## Version Goal / 版本目标

Make release state explicit, generate release and recovery evidence, and safely upgrade AI Project OS without overwriting project memory.

明确区分发布阶段，生成发布与恢复证据，并在不覆盖项目记忆的情况下安全升级 AI Project OS。

## Included / 包含

- AIPOS-045: release lifecycle and human UAT evidence model.
- AIPOS-046: deterministic release readiness and notes generator.
- AIPOS-047: feedback classification, rollback guidance, and post-release checks.
- AIPOS-048: installed/upstream version discovery.
- AIPOS-049: deterministic three-way upgrade plan and conflict report.
- AIPOS-050: guarded branch-based apply, restart, and verification.
- AIPOS-051: real v0.6-to-v0.8 dogfood, package verification, Draft PR, and consolidated UAT.

## Excluded / 不包含

- Automatic human UAT approval, merge, tag, GitHub Release, production rollback, or Git history rewrite.
- Automatic conflict resolution when installed and upstream content both changed.
- Automatic modification of project product code during an OS upgrade.
- v1.0 end-to-end mature-project rescue certification.

## Automated Preflight / 自动预检

| Check | Candidate Result | Status |
|---|---|---|
| Change impact | Seven areas complete; gate READY | Pass |
| Traceability | Seven features structurally complete for `uat_pending` | Pass |
| Source tests | 59/59 passed | Pass |
| Source strict validator | 0 failures, 0 warnings | Pass |
| Candidate determinism | Two delayed builds byte-identical | Pass |
| Candidate digest | `ec81d2439a4802fc19e1d03cc3a9b7bd739c7c92cd37af4134385d016bd3df92` | Pass |
| Final release-metadata package | Two builds byte-identical; archive valid; strict validator clean; 59/59 tests; `cf9989b993b28689da367d532db233a6d369a8edbe041712951ddc5e99cdfc1f` | Pass |
| Extracted candidate | Archive, strict validation, and 59/59 tests passed | Pass |
| Isolated dogfood | v0.6.0 to v0.8.0 apply + verify passed | Pass |
| Protected memory | Four protected areas byte-identical | Pass |
| Idempotent restart | Second apply reported already applied | Pass |
| Safety | Dogfood private gate Go; Block 0; Review 0 | Pass |

## Human UAT Scenarios / 人工验收场景

| ID | Feature | Action Steps / 执行动作 | Expected Result / 期待结果 | Actual | Pass/Fail | Notes |
|---|---|---|---|---|---|---|
| UAT-0801 | AIPOS-045 | Read the lifecycle section in `RELEASE_CONTROL.md` and this UAT header. / 阅读 `RELEASE_CONTROL.md` 的生命周期说明和本页 Header。 | You can distinguish implemented, verified, UAT pending, accepted, released, and post-release checked; only the Owner can turn UAT into Pass. / 能清楚区分各阶段，且只有 Owner 能把 UAT 变成 Pass。 | Owner accepted version evidence | Pass | Explicit v0.8.0 UAT approval |
| UAT-0802 | AIPOS-046 | Read `RELEASE_READINESS_v0.8.0.md` and `RELEASE_NOTES_v0.8.0.md`. / 阅读发布就绪报告和发布说明。 | The report names every remaining blocker and the notes clearly explain scope, verification, limitations, and rollback. / 报告列出全部剩余阻塞，说明清楚范围、验证、限制和回滚。 | Owner accepted version evidence | Pass | Explicit v0.8.0 UAT approval |
| UAT-0803 | AIPOS-048/049 | Read the Inputs and Plan Result sections in `DOGFOOD_REPORT_v0.8.0.md`. / 阅读 dogfood 报告的输入与计划结果。 | Installed and target versions are clear; add/update/migrate/preserve/conflict are understandable; conflict is zero. / 版本来源清楚，各类升级动作可理解，冲突为零。 | Owner accepted version evidence | Pass | Explicit v0.8.0 UAT approval |
| UAT-0804 | AIPOS-050 | Review the Protected Memory table in the dogfood report. / 检查 dogfood 报告的受保护项目记忆表。 | All four before/after digests match, and no protected content appears in the report. / 四组升级前后摘要一致，报告没有暴露受保护内容。 | Owner accepted version evidence | Pass | Explicit v0.8.0 UAT approval |
| UAT-0805 | AIPOS-050 | Review Apply And Restart and the rollback rule. / 检查重复执行和回滚规则。 | Re-running is harmless; failed verification stops with guidance; the tool never rewrites Git history or rolls production back by itself. / 重复执行无害；验证失败会停下并给出指导；工具不自行改历史或回滚生产。 | Owner accepted version evidence | Pass | Explicit v0.8.0 UAT approval |
| UAT-0806 | AIPOS-047 | Read the feedback and recovery sections in `RELEASE_CONTROL.md`. / 阅读反馈分类与恢复章节。 | You can tell current UAT fixes, hotfixes, patches, carry-over revalidation, next-version work, Backlog, and Decision apart. / 能区分当前修复、hotfix、patch、承接复验、下版本、Backlog 和 Decision。 | Owner accepted version evidence | Pass | Explicit v0.8.0 UAT approval |
| UAT-0807 | AIPOS-051 | Inspect the Draft PR and candidate evidence. / 检查 Draft PR 与候选证据。 | GitHub contains source and reviewed evidence only; the zip remains a Release asset, and merge/tag/release are still pending your approval. / GitHub 只含源码和审查证据，zip 仍只作为 Release asset，合并、tag、发布继续等待你的批准。 | Owner accepted PR #7 and candidate evidence | Pass | Explicit v0.8.0 UAT approval |

## Known Limitations / 已知限制

- A GitHub release lookup needs network access; local directory, zip, and metadata inputs remain available offline.
- The planner intentionally blocks ambiguous both-modified files for human review instead of guessing.
- Apply updates OS-owned files only. Project product code and protected project memory are outside its automatic write boundary.
- Rollback is documented and branch-based; production rollback and Git history rewrite always remain human-controlled.
- Linear could not create individual AIPOS-045 through AIPOS-051 issues because the free workspace reached 250 non-archived issues. The Train B Project Document is the temporary equivalent requirement record.

## UAT Decision / UAT 决定

Pass:

```text
UAT 通过，允许发布 v0.8.0。
```

Fail:

```text
UAT 未通过，请根据我在 Linear 或 Codex 中的反馈继续修改 v0.8.0。
```

## Sign-off / 签署

```text
Accepted By: dvdTeacher / Owner
Date: 2026-08-26
Decision: UAT 通过，允许发布 v0.8.0。
Known Limitation Disposition: Accepted; network lookup, human conflict resolution, protected write boundaries, human-controlled rollback, and temporary Linear Project Document remain documented.
```
