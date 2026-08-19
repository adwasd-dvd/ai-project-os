# REQUIREMENT_MANAGEMENT

本文定义 AI Project OS v0.3 的需求和 issue 管理规则。

核心原则：

```text
不是所有想法都立刻变成 Feature。
不是所有 Linear 内容都需要新 Issue。
进入开发前必须有 Feature ID、目标版本和验收标准。
```

## 分类

| 类型 | 用途 | 何时创建 Issue |
|---|---|---|
| Idea | 灵感、抱怨、模糊想法 | 先记录来源；不清楚时留评论或进入 Backlog |
| Requirement | 用户需要或业务规则 | 影响范围、版本或验收时创建 Issue |
| Feature | 可开发、可测试、可验收的产品能力 | 必须创建 Issue，并有 Feature ID 和目标版本 |
| Bug | 现有行为与预期不一致 | 有复现步骤、影响和目标版本时创建 Issue |
| Chore | 不直接改变产品能力的维护工作 | 会消耗开发时间或影响发布时创建 Issue |
| Decision | 业务或技术方向不明确 | 会阻塞范围、实现或验收时创建 Issue |
| UAT Feedback | 人工验收中的发现 | 影响当前版本、patch、下一版本或决策时创建 Issue |
| Backlog | 记录但不排期的事项 | 需要保留、比较或未来规划时创建 Issue |

## Comment、Issue、Multiple Issues

留在评论里：

- 补充上下文，不改变范围。
- 说明人类已经验证了什么。
- 提供截图、链接、错误原文或运行结果。
- 对同一个 Issue 的验收细节做轻量补充。

创建一个新 Issue：

- 需要独立开发、测试或验收。
- 目标版本和原 Issue 不同。
- 需要单独 Decision。
- 需要单独负责人或执行节奏。
- 是旧版本 Issue 的 carry-over revalidation。

拆成多个 Issue：

- 一个请求包含多个用户可见能力。
- 不同部分属于不同版本。
- 不同部分有不同验收标准或风险。
- 一部分是当前版本修复，另一部分是下一版本 Feature。
- 一个大能力需要 staged delivery。

如果不确定，Codex 必须先创建 Decision 或给出拆分建议，不得直接开发。

## Feature Ready 最小字段

Feature 进入开发前必须有：

```text
Feature ID:
Module:
Target Version:
Type:
Source:
Problem:
Action Steps:
Expected Behavior:
Expected Result:
Acceptance Criteria:
Dependencies:
Risks:
Decisions:
UAT:
```

说明：

- `Action Steps` 写谁要做什么。
- `Expected Result` 写完成后应该看到、得到或验证到什么。
- `Acceptance Criteria` 写可以被人工验收的清单。
- 缺 Feature ID 或 Target Version 时，Codex 只能整理需求，不能正式开发。

## Assignee、Status、Labels、Comments

推荐用法：

- Assignee 表示当前下一动作负责人，不表示最终责任人。
- 有 assignee 表示 human queue；无 assignee 表示 Codex queue。
- Status 表示工作阶段，不表示用户已经验收。
- Labels 用 namespaced OS labels，例如 `type:feature`、`module:linear`。
- `next:*` labels are optional in the basic path; do not require humans to maintain them for normal handoff.
- Comments 用来保留讨论、证据、决策摘要和 carry-over trace。

不要用 Assignee 代替状态，也不要用评论代替目标版本。

基础交接：

| 场景 | Status | Assignee |
|---|---|---|
| 等 Codex 开工 | Todo | Empty |
| Codex 正在处理 | In Progress | Empty |
| 等人类补信息或做决定 | Todo | Human |
| 等人类 review 或 UAT | In Review | Human |
| 人类验收通过 | Done | Any |
| 人类验收失败，交回 Codex | Todo | Empty |

即使 issue 是 `Todo + unassigned`，Codex 也必须先检查 Feature ID、目标版本、验收标准和阻塞 Decision。

## 宽泛需求拆分

当用户说：

```text
我想让系统自动跟进 Linear，然后自己推进任务。
```

Codex 应拆成：

| Issue | Target Version | Why |
|---|---|---|
| Automation boundary Decision | v0.2.0 | 先定义能不能自动写、能不能自动改代码 |
| Linear intake scan contract | v0.2.0 | 手动和 cron 都要复用同一套扫描规则 |
| Assignee-driven handoff | v0.3.0 | 先降低人类维护 label 的操作负担 |
| Cron-ready runner design | v0.6.0 | 定义配置、dry-run、输出、幂等 |
| Actual automatic code execution | Future | 高风险，必须有后续 Decision |

## 用户口令

只记录，不开发：

```text
请把下面这个想法按 AI Project OS 分类并整理成 Linear 草案。
不要写代码，不要改变状态。如果缺 Feature ID、目标版本或验收标准，请列出缺口。
```

把大需求拆成版本计划：

```text
请读取 Linear 和 project-os/VERSION_PLANNING.md。
把这个需求拆成当前版本、下一版本、Backlog 或 Decision。
先给拆分建议，不要直接改代码。
```

把人类反馈交回 Codex：

```text
我已经在 Linear 留了反馈，并把 issue 改成 Todo、清空 assignee。
请检查这个 issue 是否 Ready，然后继续处理。
如果不是 Codex-ready，请说明缺口。
```

根据评论继续整理：

```text
请检查这个 Linear issue 的最新评论。
判断它是补充说明、当前版本修复、下一版本需求、Backlog 还是 Decision。
如果需要新 issue，请先给草案和理由。
```

## Example Feature Issue / 示例 Feature Issue

```text
Feature ID: AIPOS-015
Module: workflow
Target Version: v0.2.0
Type: feature
Source: Owner feedback on older-version issues
Linear Description Language: English + Chinese

Problem / 问题:
Codex can miss active Linear feedback if it scans only one project.
如果 Codex 只扫描一个项目，就可能漏掉仍需处理的 Linear 反馈。

Action Steps / 执行动作:
1. Scan named issues and active AI Project OS issues across versions.
   扫描用户点名的 issue，以及跨版本 active issue。
2. Classify comments by current fix, next version, backlog, duplicate, or decision.
   按当前修复、下一版本、backlog、重复或 decision 分类评论。

Expected Result / 期待结果:
The run summary lists scanned, created, updated, skipped, blockers, and next action.
运行摘要列出 scanned、created、updated、skipped、blockers 和 next action。

Acceptance Criteria / 验收标准:
- Broad Linear prompts scan active issues across versions.
- Off-scope feedback leaves source trace comments.
- Summary is bilingual.
```

## Example Decision Issue / 示例 Decision Issue

```text
Decision: Allow semi-automatic Linear writes?
决策：是否允许半自动 Linear 写入？

Context / 背景:
Scheduled scans can find actionable feedback, but write actions may create duplicates.
定时扫描可以发现反馈，但写入动作可能制造重复。

Options / 选项:
1. Read-only only.
2. Advisory comments only.
3. Semi-automatic safe writes.

Action After Decision / 决定后的动作:
Codex updates AUTOMATION_POLICY and the related Linear issue status.
Codex 更新 AUTOMATION_POLICY 和相关 Linear issue 状态。
```
