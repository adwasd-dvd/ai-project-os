# LINEAR_INTAKE

本文定义 AI Project OS v0.3 的 Linear intake scan 规则。

这套规则同时用于：

- 手动 prompt，例如 `检查 Linear，然后按 AI Project OS 规则继续工作`。
- cron 或 scheduled automation 的 dry-run/advisory scan。

## Intake Scan Contract

每次 intake scan 必须做：

1. 读取用户点名的 Issue、Project 或版本。
2. 读取相关 AI Project OS Project 中的 active Issue。
3. 检查近期更新、评论、状态、assignee、labels、project/version、blockers 和 duplicate risk。
4. 按 status + assignee 归入 Codex Queue、Human Queue、Review Queue、Blocked/Ambiguous 或 Done/Closed。
5. 分类每条需要处理的反馈。
6. 对 off-scope feedback 创建或建议正确承接位置。
7. 输出 bilingual run summary。

## Assignee-driven Routing

v0.3 的基础路由规则：

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

扫描时必须先把 issue 分到这些队列：

| Queue | Status + Assignee | Meaning / 含义 | Codex Behavior / Codex 行为 |
|---|---|---|---|
| Codex Queue | `Todo + unassigned` | 等 Codex 开工 | 若 Ready 条件满足，可建议或开始处理 |
| Codex Active | `In Progress + unassigned` | Codex 正在处理或应继续 | 继续上下文，检查是否有阻塞 |
| Human Queue | `Todo + assigned` | 等人类补信息、决定或操作 | 不开工；总结人类下一步 |
| Human Active | `In Progress + assigned` | 人类正在处理 | 不抢活；只做 advisory |
| Review Queue | `In Review + assigned` | 等人类 review 或 UAT | 不关 issue；等待人类 pass/fail |
| Inconsistent | `In Review + unassigned` | 完工后无人验收 | 报告不一致，建议 assign 给 Owner |
| Closed Watch | `Done + recent active comment` | 原范围完成但出现新反馈 | 分类为 carry-over、patch、backlog 或 decision |

`next:*` labels are optional in the basic path. They may be used by advanced teams, but Codex must not require humans to maintain them for normal routing.

`next:*` label 在基础路径中是可选项。高级团队可以使用，但 Codex 不得要求人类为了普通路由去维护它们。

## Mandatory Scan Scope

宽泛 Linear 命令必须扫描：

- 用户明确点名的 Issue。
- 当前目标版本 Project。
- 同一 team 中名称匹配当前产品或 OS 的相邻版本 Project。
- `Todo`、`In Progress`、`In Review` 的 active Issue。
- lookback window 内有更新的 `Backlog` Issue。
- 被点名或近期有评论的旧版本 Issue，即使它们不在当前版本 Project。
- 当前版本阻塞 Decision。

默认 lookback window：

```text
7 days
```

如果 scan 范围太大，Codex 可以先汇报将扫描的范围，并分批执行。

## Status Sanity Rules

| 状态 | 应代表 | 异常信号 |
|---|---|---|
| Backlog | 记录但未排期 | 有明确当前版本动作却长期不动 |
| Todo | 下一步可处理，具体看 assignee | 无 assignee 但缺 Feature ID、目标版本、验收标准或有阻塞 Decision |
| In Progress | Codex 或人正在处理，具体看 assignee | 长期无最近进展、阻塞 Decision 未解决、负责人和评论矛盾 |
| In Review | 等代码/文档 review 或 UAT 准备 | 无 assignee、或人类已要求修改但仍停在 Review |
| Done | 原范围完成 | 新评论提出下版本反馈，需要 carry-over |
| Canceled | 明确不做 | 后续又出现有效需求，需要新 Issue 或 Decision |

Codex 不得把 `Done` 当作 UAT 通过，除非有人工 UAT 结论。

## Comment Classification

每条新评论或近期评论必须分类为：

- Context only：只补充背景。
- Current fix：当前版本阻塞修复。
- Review rework：review 后要求修改。
- Next-version requirement：下一版本需求。
- Carry-over revalidation：旧版本完成后，下版本重新验证。
- Backlog：保留但不排期。
- Decision needed：需要人类决定。
- Duplicate candidate：疑似重复。

如果分类不清，Codex 必须问问题或创建 Decision，不得静默处理。

## Assignee Rules

Assignee 表示下一动作负责人。

推荐解释：

- 无 assignee：默认进入 Codex queue，但仍需通过 Ready 检查。
- 有 assignee：默认进入 human queue 或 review queue，Codex 不主动抢活。
- Owner/PM：需要业务确认、范围确认或 UAT。
- Reviewer/Consultant：需要 review 或高风险判断。

不要只靠 assignee 触发自动开发。

单用户默认规则：

```text
交给人类 = assign 给这个人
交给 Codex = unassign + Todo
Codex 做完 = In Review + assign 给 Owner
人类验收通过 = Done
人类验收失败 = 留反馈 + unassign + Todo
```

## Off-scope Feedback

当反馈有效但不属于原 Issue 或当前版本：

1. 不移动旧 Issue。
2. 判断是否更新已有下一版本 Issue。
3. 如果没有合适 Issue，创建或草拟新 Issue。
4. 在来源 Issue 留 trace comment。
5. 新 Issue 写明 source issue、source comment、target version、validation scenario、expected result。

Trace comment 示例：

```text
Carry-over / 承接说明:
This feedback belongs to v0.2 revalidation and is tracked in DVD-24.
这条反馈属于 v0.2 重新验证，已在 DVD-24 跟进。
The original v0.1 scope remains closed.
原 v0.1 范围保持关闭。
```

## Run Summary Template

每次 scan 必须输出：

```text
Linear Intake Run / Linear 扫描结果

Scan Scope / 扫描范围:
- Team:
- Projects:
- Statuses:
- Lookback:
- Explicit Issues:

Scanned / 已扫描:
- Issues:
- Comments:

Codex Queue / Codex 队列:
-

Human Queue / 人类队列:
-

Review Queue / Review/UAT 队列:
-

Inconsistent / 状态不一致:
-

Created / 已创建:
-

Updated / 已更新:
-

Skipped / 已跳过:
- Issue:
  Reason:

Blockers / 阻塞项:
-

Next Action / 下一步:
-
```

如果没有写入，也要明确：

```text
Write Actions / 写入动作: None. Dry run only.
```

## UAT Scenario

v0.3 UAT 必须覆盖：

1. 创建或选择 `Todo + unassigned` issue，确认它进入 Codex Queue。
2. 创建或选择 `Todo + assigned` issue，确认它进入 Human Queue。
3. 创建或选择 `In Review + assigned` issue，确认它进入 Review Queue。
4. 模拟人类验收失败：留言、unassign、改回 `Todo`，确认 Codex 下次扫描会处理。
5. 模拟人类验收通过：改为 `Done`，确认 Codex 不再处理原范围。
6. 在旧版本 Issue 留一个下版本反馈，确认 scan 仍能识别 carry-over。
7. 确认输出包含 scanned、Codex Queue、Human Queue、Review Queue、created、updated、skipped、blockers、next action。
