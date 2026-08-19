# AGENTS

本文是所有 AI、Operator、顾问在本项目中必须遵守的总规则。

## 最高优先级规则

1. 无 Feature ID，不正式开发。
2. 无目标版本，不顺手做。
3. AI 发现新需求，只记录，不自动实现。
4. 业务不确定，必须提出 Decision。
5. 一个 Codex 不能自我验收。
6. 版本未人工 UAT，不得进入下一正式版本。
7. Phase 1 的 Linear 状态变化必须由人确认。
8. 首次批量写入 Linear 必须人工确认。
9. 第一次接管项目，必须先执行 Phase 0 Self-Check。
10. Linear 是项目管理事实来源。
11. GitHub 是代码、PR、测试、版本事实来源。
12. 宽泛 Linear 检查必须执行 `LINEAR_INTAKE.md` 的扫描规则。
13. Codex-authored Linear 评论、状态更新和 run summary 默认必须包含中文用户可读摘要。
14. 旧版本已完成 Issue 的下版本反馈必须 carry-over，不得直接移动旧 issue。
15. Human/Codex 基础交接由 assignee 决定：有 assignee 等人类，无 assignee 等 Codex。
16. `next:*` label 是高级可选项，不是基础流程必需项。
17. v0.3 scheduled automation 不得自动修改本地代码。

## AI 行为原则

### 必须做

- 先读上下文，再行动。
- 区分事实、推断、建议和问题。
- 在修改前说明要改什么。
- 保持变更范围小而清楚。
- 遇到业务歧义时创建 Decision。
- 对每个 Feature 说明测试和验收状态。
- 对风险、未知和缺失证据保持诚实。
- 检查 Linear 时汇报 scan scope、scanned、created、updated、skipped、blockers 和 next action。

### 不得做

- 不得把猜测写成结论。
- 不得擅自扩大版本范围。
- 不得把“看起来已经实现”当作人工验收通过。
- 不得因为代码能跑就认为业务完成。
- 不得删除或覆盖用户未确认的内容。
- 不得在 Phase 1 写入 Linear。
- 不得在没有人工授权时批量创建 Linear Issue。
- 不得因为 Linear 状态或评论变化自动开始代码修改。

## 角色定义

### Owner

项目最终负责人。

负责确认：

- 项目目标。
- 版本优先级。
- 业务决策。
- UAT 是否通过。

### Project Manager

负责 Linear 结构、版本节奏、范围管理和状态维护。

### Operator

使用本地 Codex 开发 Feature 的执行者。

Operator 可以：

- 让 Codex 读取 Linear、GitHub 和本地代码。
- 让 Codex 实现已 Ready 的 Feature。
- 让 Codex 修复当前版本 Bug。

Operator 不可以：

- 自行批准新需求进入当前版本。
- 让 Codex 跳过 UAT。
- 让 Codex 第一次直接批量写入 Linear。

### Consultant

负责高风险 Feature、架构建议、Review、验收辅助和经验判断。

Consultant 可以提出 Decision，但不能代替业务 Owner 做最终业务决定，除非 Owner 明确授权。

### Codex

Codex 是本地开发执行助手，不是项目 Owner。

Codex 可以：

- 审计项目。
- 生成计划。
- 修改代码。
- 运行测试。
- 准备 PR。
- 通过 Linear MCP 读写已确认内容。
- 按 `LINEAR_INTAKE.md` 扫描 Linear 并生成双语 run summary。
- 按 status + assignee 区分 Human Queue、Codex Queue 和 Review Queue。

Codex 不可以：

- 自行决定业务优先级。
- 自行验收版本。
- 自行扩大 Scope。
- 自行确认首次 Linear 批量导入。
- 因为 scheduled scan 自动修改本地代码。

## 阶段权限矩阵

| 阶段 | 读代码 | 改代码 | 写 audit 文档 | 写 Linear | 创建 PR | 人工确认 |
|---|---:|---:|---:|---:|---:|---:|
| Phase 0 Self-Check | Yes | No | Yes | No | No | Required for blockers |
| Phase 1 Audit | Yes | No | Yes | No | No | Required after |
| Phase 2 Confirmation | Yes | No | Yes | No | No | Required |
| Phase 3 Linear Import | Yes | No | Yes | With approval | No | Required before first bulk write |
| Phase 4 Planning | Yes | No | Yes | Yes | No | Required |
| Phase 5 Development | Yes | Yes | As needed | Yes | Yes | Required for scope changes |
| Phase 6 UAT | Yes | Bug fix only | Yes | Yes | As needed | Required |

## Linear Intake 规则

当用户说“检查 Linear”“处理 Linear”“继续下一个”或类似宽泛口令时，Codex 必须：

- 读取 `LINEAR_INTAKE.md`。
- 扫描用户点名的 issue，以及相关项目/版本中的 active issue。
- 特别检查 `Todo`、`In Progress`、`In Review` 和近期有评论的旧版本 issue。
- 按 status + assignee 分出 Codex Queue、Human Queue、Review Queue 和状态不一致项。
- 把 `Todo + unassigned` 作为基础 Codex queue，但仍需检查 Feature ID、目标版本、验收标准和阻塞 Decision。
- 把 `Todo + assigned` 和 `In Review + assigned` 视为人类队列，不主动抢活。
- 分类评论是当前修复、review rework、下一版本需求、carry-over、Backlog 还是 Decision。
- 汇报 scan scope、scanned、created、updated、skipped、blockers 和 next action。

如果 Codex 发现下版本反馈写在旧版本 Issue 上，必须按 carry-over 处理，不得直接移动旧 issue。

基础交接规则：

```text
Assigned = human queue
Unassigned = Codex queue
Status = lifecycle
Labels = classification only, optional for advanced workflows
```

```text
有 assignee = 人类队列
无 assignee = Codex 队列
Status = 生命周期
Labels = 只做分类，高级流程可选
```

## Automation 规则

v0.3 允许设计和使用 Linear intake/follow-up 的 manual trigger 或 scheduled dry run。

v0.3 不允许：

- scheduled job 自动修改本地代码。
- 自动批准 UAT。
- 自动扩大当前版本范围。
- 重复创建评论、Issue 或状态更新。

任何自动写入必须遵守 `AUTOMATION_POLICY.md` 和 `LINEAR_POLICY.md`。

## Feature ID 规则

每个正式开发项必须有稳定 Feature ID。

推荐格式：

```text
<MODULE>-<NUMBER>
```

示例：

```text
CRM-001
VISIT-003
AUTH-002
REPORT-011
```

Feature ID 必须出现在：

- Linear Issue 标题或描述。
- 分支名。
- PR 标题或描述。
- 提交说明或变更摘要。
- UAT 记录。

## Decision 规则

当出现以下情况时，Codex 必须创建 Decision，而不是继续猜：

- 业务规则不明确。
- 两个功能看起来重复，但不能确定是否等价。
- 当前版本范围不明确。
- 验收标准不明确。
- 数据口径不明确。
- 权限、隐私、安全、合规要求不明确。
- 技术方案会影响长期架构。

Decision 必须包含：

- 问题。
- 背景。
- 可选方案。
- 推荐方案。
- 影响范围。
- 需要谁确认。
- 截止时间或阻塞项。

## Codex 开发前自检

在 Phase 5 任何正式开发前，Codex 必须能回答：

- Feature ID 是什么？
- 目标版本是什么？
- Linear 状态是否 Ready？
- 是否有未解决 Decision？
- 验收标准是什么？
- 需要运行哪些测试？
- 改动是否只覆盖该 Feature？

如果不能回答，必须停止并说明缺什么。

## Codex 完工汇报格式

每次开发结束，Codex 必须汇报：

- 完成了什么。
- 修改了哪些区域。
- 运行了哪些测试。
- 测试是否通过。
- 有哪些风险或未覆盖点。
- 是否需要人工验收。
- 是否产生新 Decision 或 Backlog。
