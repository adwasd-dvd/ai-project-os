# UAT v0.6.0 - Development Train A

## UAT Header

```text
Version: v0.6.0
Date: 2026-08-25
Environment: local source repo + Linear DvdTeacher + GitHub Release
Build / Commit: release commit a3076d69793ee62ff0c758018984f1b201cc32bb; tag v0.6.0
Tester: Owner / dvdTeacher
Owner: dvdTeacher
Result: Pass
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
| Full source tests | Packaging, intake, safety, traceability, validator, and whitebox tests pass | 38/38 passed | Pass |
| Strict validator | Source and template match; 0 failures, 0 warnings | 0 failures, 0 warnings | Pass |
| Fixture determinism | Repeated unchanged scan output matches | Covered by test + generated report | Pass |
| Missing credential | Live scan fails closed without exposing a token | Covered by test; local token unavailable | Pass |
| Write gates | Config + CLI + runtime authorization all required | Covered by tests | Pass |
| Incomplete/stale plan | Apply is refused | Covered by tests | Pass |
| Idempotency | Restart and remote marker prevent duplicate advisory comment | Covered by tests | Pass |
| Partial failure | Successful keys stay complete; failed key retries | Covered by test | Pass |
| Ledger boundary | No API key, comment body, or raw payload | Covered by test | Pass |
| Change impact | Seven areas complete; declared gate READY | `CHANGE_IMPACT_REPORT_v0.6.0.md` | Pass |
| Traceability | All features structurally justify the declared state | Structural PASS; 7 features released after human UAT and publication | Pass |
| Safety gates | Target private gate has Block 0 | Final tracked private: Block 0, Review 0; public advisory: Block 0, 40 expected audit/Agent classification review items | Pass |
| Final release package | Zip, digest, extraction, strict validation, and tests pass | Two delayed builds byte-identical; extracted validator clean; 38/38 tests; SHA-256 `565e81b722ddba1b02514c2a8485e2f831332125428f2ae7284f55be3c45639b` | Pass |

## Human UAT Scenarios / 人工验收场景

| ID | Feature | Action Steps / 执行动作 | Expected Result / 期待结果 | Actual | Pass/Fail | Notes |
|---|---|---|---|---|---|---|
| UAT-0601 | AIPOS-038/039 | Run the fixture command in `AUTOMATION_RUNBOOK.md` / 运行手册里的 fixture 命令 | Six in-scope issues and one skipped issue; Codex, Human, Review, inconsistent, Closed Watch, and blocked queues appear / 六个范围内 issue、一个 skipped，各队列正确出现 | Owner accepted version evidence | Pass | Explicit version UAT approval |
| UAT-0602 | AIPOS-039 | Read EX-905 and EX-906 in `TRAIN_A_INTAKE_REPORT.md` / 阅读报告中的 EX-905 与 EX-906 | EX-905 is carry-over without moving old scope; EX-906 is blocked by missing Ready fields / EX-905 承接但不移动旧范围；EX-906 被 Ready 缺口阻塞 | Owner accepted version evidence | Pass | Explicit version UAT approval |
| UAT-0603 | AIPOS-038/041 | Follow local config and live dry-run setup without pasting a token into a file / 按手册配置本地 live dry-run，不把 token 写入文件 | Report is generated under ignored runtime; no Linear mutation occurs / 报告进入 ignored runtime；没有 Linear mutation | Owner accepted documented setup and known credential limitation | Pass | No credential was provided; missing-credential fail-closed path was tested |
| UAT-0604 | AIPOS-040 | Read the three write gates and run apply without one gate / 阅读三层写入门禁，并故意缺一层运行 apply | Apply returns BLOCK and writes nothing / Apply 返回 BLOCK 且不写入 | Owner accepted version evidence | Pass | Gate failures covered by automated tests |
| UAT-0605 | AIPOS-041 | Read the cron-compatible and Codex recurring examples / 阅读 cron-compatible 与 Codex recurring 示例 | Owner can explain schedule, report location, alert path, and why code cannot change / Owner 能说明 schedule、报告位置、提醒路径及为何不会改代码 | Owner accepted version evidence | Pass | Explicit version UAT approval |
| UAT-0606 | AIPOS-043 | Read `CHANGE_IMPACT_REPORT_v0.6.0.md` / 阅读 change-impact report | Owner can identify affected areas, risks, tests, UAT, rollout, rollback, and the READY/BLOCKED rule / Owner 能识别影响、风险、测试、UAT、上线、回滚与门禁规则 | Owner accepted version evidence | Pass | Explicit version UAT approval |
| UAT-0607 | AIPOS-042 | Read `TRACEABILITY_REPORT_v0.6.0.md` / 阅读 traceability report | Every AIPOS-038..044 row links requirement, Linear, impact, evidence, tests, and human UAT without claiming release early / 每行证据可追，且不会提前冒充 released | Owner accepted version evidence | Pass | State promoted to `released` only after tag and Release verification |
| UAT-0608 | AIPOS-044 | Inspect PR scope, test/safety evidence, zip digest, and excluded actions / 检查 PR、测试/安全证据、zip digest 与排除动作 | Candidate is reviewable and GitHub remains clean; no zip is committed / 候选可审查、GitHub 整洁、zip 未提交 | Owner accepted version evidence | Pass | PRs #4 and #5 merged; release asset remains outside Git source history |

## Known Limitations / 已知限制

- This environment has no `LINEAR_API_KEY`; the live API path is implemented against the current official Linear GraphQL schema but requires the Owner's credential for human UAT.
- The default planner emits advisory comments only. `issue_update` and `issue_create` are supported by the guarded executor but require an explicitly reviewed action plan and narrow local allowlist.
- Polling is bounded and project-scoped. An incomplete project catalog or issue cap blocks apply instead of silently claiming coverage.
- Webhooks are recommended when a future deployment needs near-real-time updates or larger scale.

## Release Blockers / 发布阻塞

```text
- [x] Final full test and strict validation evidence recorded.
- [x] Final safety gates recorded.
- [x] Final zip and local/remote digest verified: `565e81b722ddba1b02514c2a8485e2f831332125428f2ae7284f55be3c45639b`.
- [x] GitHub PR #4 and deterministic-packaging PR #5 merged.
- [x] Tag `v0.6.0` and GitHub Release published.
- [x] Linear DVD-219 through DVD-225 moved to Done; Train A project completed.
- [x] Owner explicitly passed v0.6.0 on 2026-08-25.
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

## Sign-off / 签署

```text
Accepted By: dvdTeacher / Owner
Date: 2026-08-25
Decision: UAT 通过，允许发布 v0.6.0。
Known Limitation Accepted: standalone live Linear dry-run still requires an Owner-managed credential
```
