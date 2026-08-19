# AUTOMATION_POLICY

本文定义 AI Project OS v0.3 的 Linear follow-up automation 和 cron-ready runner 边界。

v0.3 的自动化目标是：

```text
自动扫描 Linear。
自动总结风险和下一步。
在安全模式内写入有限 Linear 内容。
不自动批准 UAT。
不自动扩大 scope。
不自动修改本地代码。
```

## 触发类型

| 类型 | 说明 | v0.3 是否允许 |
|---|---|---|
| Manual Trigger | 用户在 Codex 中明确要求检查或处理 Linear | Yes |
| Scheduled Check | cron/scheduled job 自动扫描 Linear | Yes, dry-run default |
| Automatic Linear Write | 自动评论、建议状态、创建承接 Issue | Limited by mode |
| Automatic Code Execution | 自动拉代码、改文件、跑开发任务 | No in v0.3 |

## DEC-004 边界

v0.3 采用以下边界：

- 首次设置默认 dry-run/read-only。
- 可以自动生成双语摘要和建议。
- 只允许文档化的 safe Linear writes。
- 所有写入必须幂等，不能重复评论或重复建 Issue。
- 不得批准 UAT。
- 不得静默扩大当前版本范围。
- 不得在 v0.3 自动开始或修改本地代码，除非用户在 Codex 对话里明确要求。
- Scheduled scans must route by status + assignee before suggesting action.
- 定时扫描必须先按 status + assignee 路由，再建议动作。

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

All automation modes use the same v0.3 routing rule:

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

## Cron-ready Runner Interface

The runner can be implemented later, but v0.3 defines the contract:

```text
Command:
  run-linear-intake

Inputs:
  --team
  --projects
  --statuses
  --lookback
  --labels
  --include-issues
  --exclude-issues
  --mode
  --dry-run
  --max-issues

Outputs:
  run summary
  changed issues
  skipped issues
  ambiguous items
  blockers
  suggested next actions
```

## Schedule Config

Recommended config shape:

```text
enabled: false
timezone: America/Toronto
interval: daily
dry_run: true
mode: read-only
team: DvdTeacher
projects:
  - AI Project OS v0.3
active_statuses:
  - Todo
  - In Progress
  - In Review
lookback_days: 7
max_issues_per_run: 50
labels:
  - type:feature
  - type:decision
exclude_statuses:
  - Canceled
```

Safe defaults:

- `enabled: false`
- `dry_run: true`
- `mode: read-only`
- small `max_issues_per_run`
- explicit team/project filters

## Idempotency

Each run must produce a stable run key:

```text
linear-intake:<team>:<project-or-scope>:<date>:<mode>
```

Before writing, the runner must check whether it already wrote an equivalent summary or trace comment.

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

v0.3 UAT must include:

- Manual Linear scan.
- Simulated scheduled dry run.
- Two consecutive runs with no duplicate comments.
- Cross-version Todo comment detection.
- `Todo + unassigned` enters Codex Queue.
- `Todo + assigned` enters Human Queue.
- `In Review + assigned` enters Review Queue.
- Bilingual summary inspection.
- Confirmation that no code work starts automatically.
