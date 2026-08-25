# UAT v0.6.0 - Development Train A

## UAT Header

```text
Version: v0.6.0 candidate
Date: 2026-08-24
Environment: local source repo + Linear DvdTeacher + GitHub Draft PR
Build / Commit: implementation commit fbcb331; Draft PR #4
Tester: Owner / dvdTeacher
Owner: dvdTeacher
Result: Pending Human UAT
```

## Version Goal / 版本目标

Safely automate Linear intake and explicitly authorized idempotent Linear writes, while making every formal change traceable from requirement through human UAT and release.

安全自动执行 Linear intake 与明确授权的幂等 Linear 写入，并让每个正式变更都能从需求追踪到人工 UAT 和 release。

## Included / 包含

- AIPOS-038 / DVD-219: scheduled/manual Linear intake configuration and runner.
- AIPOS-039 / DVD-220: deterministic queues, Ready checks, feedback classification, and old-version watch.
- AIPOS-040 / DVD-221: guarded writes, idempotency, plan freshness, retry, partial failure, and sanitized ledger.
- AIPOS-041 / DVD-222: manual, cron-compatible, and Codex recurring operations runbook.
- AIPOS-042 / DVD-223: requirement-to-release traceability manifest and validator.
- AIPOS-043 / DVD-224: seven-area change-impact gate and report.
- AIPOS-044 / DVD-225: validation, worked example, package, Draft PR, and this consolidated UAT.

## Excluded / 不包含

- Scheduled modification of local product code.
- Automatic Decision, scope, review, UAT, merge, tag, or release approval.
- Automatic movement of completed old issues into a new version.
- High-frequency webhook service; use webhooks later when polling scale requires it.
- v0.8 Development Train B release/rollback and self-upgrade implementation.

## Automated Preflight / 自动预检

| Check | Expected Result | Candidate Result | Status |
|---|---|---|---|
| Python compile | New tools compile with Python 3 | Passed | Pass |
| Full source tests | Intake, safety, traceability, validator, and whitebox tests pass | 36/36 passed | Pass |
| Strict validator | Source and template match; 0 failures, 0 warnings | 0 failures, 0 warnings | Pass |
| Fixture determinism | Repeated unchanged scan output matches | Covered by test + generated report | Pass |
| Missing credential | Live scan fails closed without exposing a token | Covered by test; local token unavailable | Pass |
| Write gates | Config + CLI + runtime authorization all required | Covered by tests | Pass |
| Incomplete/stale plan | Apply is refused | Covered by tests | Pass |
| Idempotency | Restart and remote marker prevent duplicate advisory comment | Covered by tests | Pass |
| Partial failure | Successful keys stay complete; failed key retries | Covered by test | Pass |
| Ledger boundary | No API key, comment body, or raw payload | Covered by test | Pass |
| Change impact | Seven areas complete; declared gate READY | `CHANGE_IMPACT_REPORT_v0.6.0.md` | Pass |
| Traceability | All features structurally justify `uat_pending` | Structural PASS; 7 features at `uat_pending` | Pass |
| Safety gates | Target private staged gate has Block 0 | Staged private: Block 0, Review 0; staged public: Block 0, 13 expected publication-review items | Pass |
| Candidate package | Zip, digest, extraction, strict validation, and tests pass | Archive valid; extracted validator clean; 36/36 tests; SHA-256 `c453e8732a4b77907055ebb82fb980a864201a7ffefd090d3ac2f95a4c65f217` | Pass |

## Human UAT Scenarios / 人工验收场景

| ID | Feature | Action Steps / 执行动作 | Expected Result / 期待结果 | Actual | Pass/Fail | Notes |
|---|---|---|---|---|---|---|
| UAT-0601 | AIPOS-038/039 | Run the fixture command in `AUTOMATION_RUNBOOK.md` / 运行手册里的 fixture 命令 | Six in-scope issues and one skipped issue; Codex, Human, Review, inconsistent, Closed Watch, and blocked queues appear / 六个范围内 issue、一个 skipped，各队列正确出现 |  |  |  |
| UAT-0602 | AIPOS-039 | Read EX-905 and EX-906 in `TRAIN_A_INTAKE_REPORT.md` / 阅读报告中的 EX-905 与 EX-906 | EX-905 is carry-over without moving old scope; EX-906 is blocked by missing Ready fields / EX-905 承接但不移动旧范围；EX-906 被 Ready 缺口阻塞 |  |  |  |
| UAT-0603 | AIPOS-038/041 | Follow local config and live dry-run setup without pasting a token into a file / 按手册配置本地 live dry-run，不把 token 写入文件 | Report is generated under ignored runtime; no Linear mutation occurs / 报告进入 ignored runtime；没有 Linear mutation |  |  | Requires Owner-created Linear API key |
| UAT-0604 | AIPOS-040 | Read the three write gates and run apply without one gate / 阅读三层写入门禁，并故意缺一层运行 apply | Apply returns BLOCK and writes nothing / Apply 返回 BLOCK 且不写入 |  |  |  |
| UAT-0605 | AIPOS-041 | Read the cron-compatible and Codex recurring examples / 阅读 cron-compatible 与 Codex recurring 示例 | Owner can explain schedule, report location, alert path, and why code cannot change / Owner 能说明 schedule、报告位置、提醒路径及为何不会改代码 |  |  |  |
| UAT-0606 | AIPOS-043 | Read `CHANGE_IMPACT_REPORT_v0.6.0.md` / 阅读 change-impact report | Owner can identify affected areas, risks, tests, UAT, rollout, rollback, and the READY/BLOCKED rule / Owner 能识别影响、风险、测试、UAT、上线、回滚与门禁规则 |  |  |  |
| UAT-0607 | AIPOS-042 | Read `TRACEABILITY_REPORT_v0.6.0.md` / 阅读 traceability report | Every AIPOS-038..044 row links requirement, Linear, impact, evidence, tests, and pending human UAT; it does not claim accepted/released / 每行证据可追，且不冒充 accepted/released |  |  |  |
| UAT-0608 | AIPOS-044 | Inspect Draft PR scope, test/safety evidence, zip digest, and excluded actions / 检查 Draft PR、测试/安全证据、zip digest 与排除动作 | Candidate is reviewable and GitHub remains clean; no zip is committed / 候选可审查、GitHub 整洁、zip 未提交 |  |  |  |

## Known Limitations / 已知限制

- This environment has no `LINEAR_API_KEY`; the live API path is implemented against the current official Linear GraphQL schema but requires the Owner's credential for human UAT.
- The default planner emits advisory comments only. `issue_update` and `issue_create` are supported by the guarded executor but require an explicitly reviewed action plan and narrow local allowlist.
- Polling is bounded and project-scoped. An incomplete project catalog or issue cap blocks apply instead of silently claiming coverage.
- Webhooks are recommended when a future deployment needs near-real-time updates or larger scale.

## Release Blockers / 发布阻塞

```text
- [x] Final full test and strict validation evidence recorded.
- [x] Final safety gates recorded.
- [x] Candidate zip and digest verified.
- [x] GitHub Draft PR created: https://github.com/adwasd-dvd/ai-project-os/pull/4
- [x] Linear DVD-219 through DVD-225 moved to In Review and assigned to Owner.
- [ ] Owner completes human scenarios and explicitly passes v0.6.0.
```

## UAT Decision / UAT 决定

Pass:

```text
UAT 通过，允许发布 v0.6.0。
```

Fail:

```text
UAT 未通过，请根据我在 Linear 或 Codex 中的反馈继续修改 v0.6.0。
```

Do not merge, tag, publish a GitHub Release, complete DVD-219 through DVD-225, or complete the v0.6 Linear project before explicit Pass.

在明确 Pass 前，不得 merge、tag、发布 GitHub Release、完成 DVD-219 到 DVD-225，或完成 v0.6 Linear project。
