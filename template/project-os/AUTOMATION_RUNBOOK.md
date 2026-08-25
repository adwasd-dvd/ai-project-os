# AUTOMATION_RUNBOOK

This runbook turns the Linear intake policy into a repeatable manual, cron-compatible, or Codex scheduled scan.

本手册把 Linear intake policy 变成可重复执行的手动、cron-compatible 或 Codex 定时扫描。

## Safety Promise / 安全承诺

The runner may read Linear, classify queues, prepare advisory actions, and execute only explicitly allowlisted Linear mutations.

Runner 可以读取 Linear、分类队列、准备 advisory 动作，并且只能执行明确白名单内的 Linear mutation。

It never:

- modifies local product code;
- approves a Decision, scope change, review, or UAT;
- merges a PR or creates a tag/release;
- stores an API key in config, reports, or the run ledger;
- treats an assigned issue as automatic Codex work.

它绝不会：

- 修改本地产品代码；
- 批准 Decision、scope change、review 或 UAT；
- merge PR 或创建 tag/release；
- 把 API key 存入配置、报告或运行账本；
- 把有 assignee 的 issue 当成 Codex 自动任务。

## 1. Confirm Python / 确认 Python

```bash
python3 --version
```

The runner uses only the Python standard library.

Runner 只使用 Python 标准库。

## 2. Create Local Config / 创建本地配置

Copy the example to the ignored runtime directory:

把示例复制到已忽略的 runtime 目录：

```bash
cp project-os/automation/linear_intake.example.json \
  project-os/runtime/linear_intake.json
```

Edit only the local copy:

- `team.id`: Linear team UUID.
- `team.name`: readable team name.
- `projects`: exact current projects.
- `project_name_prefixes`: product prefix used to include adjacent/older versions.
- `lookback_days`: default `7`.
- `max_issues`: default `50`; keep the scope small.

只编辑本地副本。`project-os/runtime/` 的生成内容不会进入 Git。

Linear lets you copy a model UUID from the command menu. The official API endpoint is `https://api.linear.app/graphql`.

## 3. Run the Included Fixture / 运行内置示例

```bash
python3 project-os/tools/linear_intake.py --root . scan \
  --config project-os/automation/linear_intake.example.json \
  --snapshot project-os/automation/fixtures/train_a_snapshot.json \
  --as-of 2026-08-24T18:00:00Z
```

Expected result / 期待结果：

- one Ready issue in Codex Queue;
- one assigned Todo in Human Queue;
- one assigned In Review issue in Review Queue;
- one unassigned In Review inconsistency;
- one completed old-version issue in Closed Watch;
- one Todo issue blocked by missing Ready fields;
- `Write Actions: None. Dry run only.`

## 4. Run a Live Dry Scan / 实时只读扫描

Create a personal API key in Linear security/access settings and expose it only to the process:

在 Linear security/access settings 创建 personal API key，只通过进程环境提供：

```bash
export LINEAR_API_KEY='<placeholder-from-secure-secret-manager>'

python3 project-os/tools/linear_intake.py --root . scan \
  --config project-os/runtime/linear_intake.json \
  --json-out project-os/runtime/latest_linear_intake.json \
  --markdown-out project-os/runtime/latest_linear_intake.md
```

Do not paste a real key into a committed file, issue, comment, prompt, screenshot, or run ledger.

不要把真实 key 粘贴到提交文件、issue、comment、prompt、截图或运行账本中。

## 5. Review the Report / 审阅报告

Every report must include:

- scan scope;
- scanned issue/comment counts;
- Codex, Human, Review, inconsistent, blocked, and Closed Watch queues;
- created, updated, skipped, blockers, and next action;
- planned actions that were not executed.

报告只建议“交互式 Codex 下一步可以做什么”。scheduled scan 本身不会开始开发。

## 6. Schedule Read-only Runs / 配置只读定时运行

Use an absolute repository path and keep outputs in `project-os/runtime/`.

使用仓库绝对路径，并把输出保存在 `project-os/runtime/`。

Cron-compatible example, every weekday at 09:00:

```cron
0 9 * * 1-5 cd /ABSOLUTE/PATH/TO/PROJECT && /usr/bin/env python3 project-os/tools/linear_intake.py --root . scan --config project-os/runtime/linear_intake.json --json-out project-os/runtime/latest_linear_intake.json --markdown-out project-os/runtime/latest_linear_intake.md >> project-os/runtime/linear_intake.log 2>&1
```

For a Codex recurring automation, set the project as the working directory and use this prompt:

Scheduled scans never modify local product code.

```text
读取 project-os/AUTOMATION_RUNBOOK.md 和 project-os/LINEAR_INTAKE.md。
运行已配置的 Linear intake dry scan。
读取 project-os/runtime/latest_linear_intake.md，给我双语摘要。
不要修改本地代码，不要批准 UAT，不要扩大版本范围，不要执行 Linear writes。
如果发现 Codex Queue，只给出下一条交互式 Codex 启动口令。
```

Start with one or two scans per day. Linear recommends filtering, limiting fetched fields, sorting by update time, and using webhooks instead of frequent polling at larger scale.

初期每天扫描一到两次。规模增大后，应使用更窄过滤或 webhook，避免高频轮询。

## 7. Enable Limited Linear Writes / 开启有限 Linear 写入

Write mode is intentionally separate from scheduling.

写入模式与定时扫描故意分开。

1. Review `planned_actions` in the JSON report.
2. Confirm `scan_complete` is `true`; unresolved project scope or a reached issue limit blocks apply.
3. In the local config, set `write_policy.enabled` to `true`.
4. Allow only the required operation, normally `comment_create` first.
5. Run apply interactively before `max_plan_age_minutes` expires, with the runtime authorization environment variable.

```bash
export AIPOS_LINEAR_WRITE_APPROVED=1

python3 project-os/tools/linear_intake.py --root . apply \
  --config project-os/runtime/linear_intake.json \
  --plan project-os/runtime/latest_linear_intake.json \
  --authorize-writes
```

Three gates are required:

```text
apply command
+ config write_policy.enabled=true and operation allowlist
+ AIPOS_LINEAR_WRITE_APPROVED=1
```

三层门禁缺一不可。

The default example allows comments only. `issue_update` additionally requires exact `allowed_update_fields`. Creating an issue requires a bilingual description containing Action Steps / 执行动作 and Expected Result / 期待结果.

## Idempotency and Partial Failure / 幂等与部分失败

Every planned action has a stable idempotency key. A sanitized receipt is stored in:

```text
project-os/runtime/linear_intake_ledger.json
```

Successful actions are skipped on later runs. Failed actions remain retryable. The ledger records operation, target ID, status, attempts, result ID, and time; it does not record API keys or comment bodies.

成功动作以后会跳过；失败动作仍可重试。账本只记录操作、目标 ID、状态、尝试次数、结果 ID 和时间，不记录 API key 或评论正文。

Advisory comments also carry their idempotency marker in Linear. A later scan ignores its own automation comment as user feedback and suppresses a matching planned action even if local runtime state was restored from backup.

Advisory comment 也会在 Linear 中携带幂等 marker。后续扫描不会把自己的自动评论当成人类反馈；即使本地 runtime state 从备份恢复，也会抑制相同计划动作。

## Failure Handoff / 失败交接

| Failure | Required Action / 必需动作 |
|---|---|
| Missing API key | Stop; restore secure runtime credential / 停止并恢复安全运行凭证 |
| GraphQL partial/error response | Treat scan as failed; do not apply its plan / 扫描失败，不执行该 plan |
| Project scope missing, issue cap reached, or nested comments/relations are truncated | Mark scan incomplete; narrow/raise safe limit and rerun / 标记扫描不完整，调整范围或安全上限后重跑 |
| Plan older than configured maximum | Reject apply and rerun dry scan / 拒绝 apply 并重新 dry scan |
| Rate limit or server error | Bounded retry, then human alert / 有限重试后提醒人类 |
| Ambiguous feedback | Create/recommend Decision; do not guess / 创建或建议 Decision，不猜 |
| Write partially fails | Retry failed keys only / 只重试失败 key |
| Scheduled task finds Codex work | Produce an interactive handoff prompt / 生成交互式开工口令 |

Exit code `0` means the command completed. Exit code `2` means blocked, invalid, or partially failed and needs review.

## Official References / 官方参考

- Linear GraphQL getting started: <https://linear.app/developers/graphql>
- Linear rate limits and polling guidance: <https://linear.app/developers/rate-limiting>
- Linear webhooks: <https://linear.app/developers/webhooks>
