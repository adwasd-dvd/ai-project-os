# AUTOMATION_POLICY

本文定义 AI Project OS v0.6 的 Linear follow-up automation、cron-ready runner 和 guarded write 边界。

v0.6 的自动化目标是：

```text
自动扫描 Linear。
自动总结风险和下一步。
在安全模式内写入有限 Linear 内容。
不自动批准 UAT。
不自动扩大 scope。
不自动修改本地代码。
```

## 触发类型

| 类型 | 说明 | v0.6 是否允许 |
|---|---|---|
| Manual Trigger | 用户在 Codex 中明确要求检查或处理 Linear | Yes |
| Scheduled Check | cron/scheduled job 自动扫描 Linear | Yes, dry-run default |
| Automatic Linear Write | 自动评论、建议状态、创建承接 Issue | Limited by mode |
| Automatic Code Execution | 自动拉代码、改文件、跑开发任务 | No in v0.6 scheduled runs |

## DEC-004 + DEC-009 边界

v0.6 采用以下边界：

- 首次设置默认 dry-run/read-only。
- 可以自动生成双语摘要和建议。
- 只允许文档化的 safe Linear writes。
- 所有写入必须幂等，不能重复评论或重复建 Issue。
- 不得批准 UAT。
- 不得静默扩大当前版本范围。
- 不得在 v0.6 scheduled run 中自动开始或修改本地代码；只有用户在交互式 Codex 对话中明确要求，才可进入正常开发流程。
- Scheduled scans must route by status + assignee before suggesting action.
- 定时扫描必须先按 status + assignee 路由，再建议动作。
- Train A 合并 Linear automation 与 change traceability，但仍只在统一人工 UAT 后发布。
- Scheduled scan 可以产生交互式 Codex 开工口令，但不能自己修改本地产品代码。

## Automation Modes

| Mode | Reads Linear | Writes Comments | Updates Status | Creates Issues | Starts Code Work |
|---|---:|---:|---:|---:|---:|
| read-only | Yes | No | No | No | No |
| advisory | Yes | Summary only if approved | No | Draft only | No |
| semi-automatic | Yes | Yes, safe/idempotent | Limited, documented | Approved follow-up only | No |
| forbidden execution | No automation run | No | No | No | No |

Safe Linear writes in `semi-automatic`:

- Bilingual run summary comment.
- Source trace comment for carry-over feedback.
- Status recommendation comment.
- Creation of approved carry-over revalidation Issue.

Not safe without explicit human approval:

- Closing or canceling user-owned Issue.
- Changing assignee.
- Moving Issue across projects.
- Editing existing issue description.
- Changing target version.
- Marking UAT accepted.

## Status + Assignee Routing

All automation modes use the same status + assignee routing rule:

```text
Assigned = human queue
Unassigned = Codex queue
Status = lifecycle
Labels = classification only, optional for advanced workflows
```

中文规则：

```text
有 assignee = 人类队列
无 assignee = Codex 队列
Status = 生命周期
Labels = 只做分类，高级流程可选
```

Automation must never treat labels as the only proof that an issue is ready. Basic routing is based on status + assignee, then Ready checks.

自动化不得只靠 label 判断 issue ready。基础路由必须先看 status + assignee，再做 Ready 检查。

## Implemented Runner Interface

v0.6 provides `tools/linear_intake.py`:

```text
Commands:
  linear_intake.py scan
  linear_intake.py apply

Inputs:
  --config
  --snapshot
  --as-of
  --json-out
  --markdown-out
  --plan
  --authorize-writes

Outputs:
  deterministic JSON run report
  bilingual Markdown run summary
  queue routing and readiness blockers
  planned actions with idempotency keys
  sanitized apply receipts
```

`scan` is always dry-run for Linear mutations. `apply` is a separate command.

## Schedule Config

The versioned JSON config shape is defined in:

```text
project-os/automation/linear_intake.example.json
```

Safe defaults:

- `enabled: false`
- scan and apply are separate commands
- `write_policy.enabled: false`
- empty or narrowly scoped operation/field allowlists
- small `max_issues`
- explicit team/project filters

Runtime config, reports, and ledger belong in ignored `project-os/runtime/`.

## Write Authorization

Every write requires all of these controls:

```text
apply command
+ write_policy.enabled=true and operation/field allowlist
+ --authorize-writes
+ AIPOS_LINEAR_WRITE_APPROVED=1
```

Missing any control means fail closed. Supported operation names are not automatically authorized.

Apply also requires `scan_complete=true` and a plan newer than `max_plan_age_minutes`. Missing project scope, truncated issue/comment/relation pagination, GraphQL partial errors, stale plans, and future-dated plans block every mutation.

## Idempotency

Each run and planned action must produce a stable key:

```text
linear-run:<stable digest>
linear-intake:<stable digest>
```

Before writing, the runner must check the local sanitized ledger for a successful equivalent action.

Comment actions also include the stable marker in Linear. Scanner-authored marker comments are ignored as feedback and suppress equivalent future actions.

Duplicate prevention rules:

- Do not create a new Issue if an open Issue already references the same source issue and target version.
- Do not write a second trace comment with the same source issue and target issue pair.
- Do not update status if the status is already correct.
- Do not repeat advisory comments unless the underlying facts changed.

## Failure Handling

| Failure | Behavior |
|---|---|
| Linear auth failure | Stop, report auth blocker |
| API partial result | Mark run partial, do not write status changes |
| Rate limit | Stop batch, report cursor or retry hint |
| Ambiguous human reply | Ask question or create Decision |
| Stale cursor | Re-run read-only scan before writing |
| Write failure | Report affected Issue and keep next action manual |

Partial GraphQL responses are failures even when HTTP status is 200. Retrying is bounded; successful idempotency keys are never repeated while failed keys remain retryable.

## Handoff Behavior

When automation finds work that needs Codex or a human:

- It writes or returns a bilingual summary.
- It gives an explicit Codex prompt the user can paste.
- It lists blockers and missing decisions.
- It does not start code work by itself.
- It separates Codex Queue, Human Queue, Review Queue, inconsistent items, skipped items, and blockers.

Handoff prompt example:

```text
请读取 project-os/LINEAR_INTAKE.md 和 Linear run summary。
处理 run summary 中 Codex Queue 的下一个 Ready issue。
如果需要修改代码，请先确认 Feature ID、目标版本、验收标准和测试计划。
```

## UAT Checks

v0.6 UAT must include:

- Manual Linear scan.
- Simulated scheduled dry run.
- Two consecutive runs with no duplicate comments.
- Cross-version Todo comment detection.
- `Todo + unassigned` enters Codex Queue.
- `Todo + assigned` enters Human Queue.
- `In Review + assigned` enters Review Queue.
- Bilingual summary inspection.
- Confirmation that no code work starts automatically.
- Missing live credentials fail closed.
- Config-disabled, CLI-unauthorized, or runtime-unauthorized writes all fail closed.
- A partial failure retries only failed actions.
- The ledger contains no API key or comment body.
- Fixture and live dry-run reports use the same queue contract.

The copy-ready setup, cron-compatible example, Codex recurring prompt, and failure handoff are in `AUTOMATION_RUNBOOK.md`.
