# LINEAR_POLICY

本文定义 Linear 使用规则。

Linear 是项目管理事实来源。

## 基本结构

推荐结构：

- Project：按版本或主要产品阶段组织，例如 `App v0.1.0`。
- Issue：具体 Feature、Bug、Decision、UAT Feedback、Chore。
- Label：模块、类型、版本、风险、来源。
- Status：反映工作流阶段。

如果 Linear workspace 已有不同结构，Codex 必须先读取现状并提出映射建议，不得强行重建。

## v0.4 Project Whitebox Summary

成熟项目完成 Phase 0.5 后，Linear Project Description 应包含一个紧凑的双语白盒摘要，详细证据仍保存在 GitHub/本地 `project-os/discovery/`。

白盒摘要必须包含：

- Evidence freshness：日期 + commit SHA。
- System shape：系统的主要组件和运行方式。
- Confidence：总体置信度和重要低置信度区域。
- Top risks：最高影响发现及 Finding ID。
- Contradictions：未解矛盾和下一步验证。
- Unknowns：重要未知项和 owner。
- Evidence links：六份白盒报告的 GitHub 链接或仓库路径。
- Next verification：下一个验证动作和期待结果。

可直接使用的格式见 `discovery/WHITEBOX_IMPORT_REPORT.md`。

Linear 里的摘要不得：

- 复制 secret 值。
- 把 Inferred 或 Claimed 改写为 Observed。
- 隐藏高影响 Unknown 或 Contradicted 发现。
- 代替 GitHub/本地详细证据。
- 绕过 Baseline 确认和首次 Linear 批量写入授权。

## Linear 输出语言

Phase 0 初始化时，Codex 必须询问或确认 Linear Issue 描述语言。

默认建议：

```text
English + Chinese
```

如果用户没有指定其他语言，Linear Issue 应使用 `English + Chinese`。Codex-authored Linear comments、project status updates、decision notes、review notes、UAT notes 和 automation/cron summaries 也默认必须包含中文用户可读摘要。

推荐写法是：

- 字段名优先使用英文，方便跨工具和自动化读取。
- 字段内容可以中英双语，先写清事实，再补中文解释。
- 关键验收信息必须同时清楚表达执行动作和期待结果。
- 评论和 run summary 可以更紧凑，但必须让中文用户读得懂下一步。

允许保持原语言的内容：

- 代码标识符。
- 文件路径。
- 命令。
- Linear label/status 名称。
- URL。
- 原始错误文本。

如果团队只想使用一种语言，必须在 `SELF_CHECK_REPORT.md` 和 `LINEAR_IMPORT_PLAN.md` 中记录。

## Issue 类型

推荐类型：

- `type:feature`
- `type:bug`
- `type:decision`
- `type:uat-feedback`
- `type:chore`
- `type:duplicate-candidate`

## 模块标签

推荐格式：

```text
module:crm
module:visit
module:auth
module:reporting
module:admin
```

模块名称应来自 `audit/PRODUCT_MAP.md` 和人工确认结果。

## 状态流

推荐状态：

```text
Backlog
Needs Decision
Ready
In Progress
In Review
Ready for UAT
Accepted
Released
Blocked
Duplicate Candidate
Deferred
Won't Do
```

如果 Linear 现有状态不同，Codex 必须建立映射表。

## Status、Assignee、Comment 的关系

- Status 表示工作阶段。
- Assignee 表示下一动作负责人。
- Comment 表示讨论、证据、review、UAT、decision 或 carry-over trace。
- Labels 只表示分类、模块、风险或来源；基础流程不要求人类维护 `next:*` label。

## v0.3 Human/Codex Handoff

v0.3 的基础交接规则：

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

基础路由表：

| Status | Assignee | Meaning / 含义 | Next Action / 下一步 |
|---|---|---|---|
| Todo | Empty | Codex queue / 等 Codex | Codex 可在 intake 后开始，前提是 Feature ID、目标版本、验收标准和阻塞 Decision 都清楚 |
| Todo | Human | Human queue / 等人类 | 人类补信息、做决定、处理 review 或准备交接 |
| In Progress | Empty | Codex working / Codex 正在处理 | Codex 继续处理并定期汇报 |
| In Progress | Human | Human working / 人类正在处理 | Codex 不抢活，只做 advisory |
| In Review | Human | Human review or UAT / 等人类 review 或 UAT | 人类验收，通过则 Done，不通过则评论后交回 Codex |
| In Review | Empty | Inconsistent / 状态不一致 | Codex 应报告或 assign 给 Owner，不应静默视为完成 |
| Done | Any | Original scope complete / 原范围完成 | 只有有人工验收或 closeout 依据时才可视为完成 |

重要限制：

- `Unassigned + Todo` 不是“任何空负责人 issue 都能开工”。它仍然必须满足 Ready 条件。
- `Assigned + Todo` 表示人类下一步，不是 Codex-ready。
- `In Review + assigned` 是最常见的 Codex 完工交给人类检查状态。
- `Done + new active comment` 不自动 reopen；先按 intake 分类，必要时创建 carry-over 或新 issue。

人类常用动作：

| 场景 | 操作 |
|---|---|
| 验收通过 | 把 issue 改为 `Done` |
| 验收失败，需要 Codex 修改 | 留评论说明问题，清空 assignee，把状态改为 `Todo` |
| 需要自己补信息或决定 | assign 给自己，状态保持 `Todo` 或 `Blocked` |
| 是下一版本需求 | 不移动旧 issue；创建或更新下一版本 issue |

Codex 常用动作：

| 场景 | 操作 |
|---|---|
| 开始处理 Codex queue | 将 `Todo + unassigned` 改为 `In Progress + unassigned` |
| 完成实现或文档更新 | 将 issue 改为 `In Review`，assign 给 Owner 或可识别 reviewer |
| 无法识别 Owner | 保持/改为 `In Review`，评论说明需要人工 assign |
| 发现缺信息 | 评论问题，assign 给 Owner 或保持人类队列，不继续猜 |

`next:*` label 可以在多人团队或高级自动化中作为辅助信号，但它不是基础流程必需项。人类日常只需要维护 status 和 assignee。

评论本身不会让 Codex 自动开工。用户想让 Codex 处理评论时，应在 Codex 中发出明确 prompt，例如：

```text
请读取 DVD-123 的最新评论，并按 AI Project OS 判断下一步。
```

如果用户留下评论后希望 Codex 处理，推荐状态：

| 场景 | 推荐状态 | 推荐 assignee |
|---|---|---|
| 希望 Codex 重新处理 | Todo | Empty |
| Codex 正在处理 | In Progress | Empty |
| 等 review 或 UAT 准备 | In Review | Owner / reviewer |
| 原范围完成但有下版本反馈 | Done，并创建/更新 carry-over Issue | Any |

Codex 读取宽泛 Linear 请求时，必须执行 `LINEAR_INTAKE.md`，而不是只扫描当前项目。

## Feature Issue 标题

推荐格式：

```text
[FEATURE_ID] 简短标题
```

示例：

```text
[CRM-001] 客户列表支持搜索和分页
```

## Feature Issue 描述最小内容

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
Evidence:
Dependencies:
Risks:
Decisions:
GitHub:
UAT:
```

说明：

- `Action Steps` 必须写清 Operator、Owner 或用户要执行什么。
- `Expected Result` 必须写清完成后应该看到、得到或验证到什么。
- 不得只写抽象目标，例如“完成初始化”；必须能被人照着检查。

## Decision Issue 描述最小内容

```text
Decision:
Context:
Options:
Recommendation:
Action After Decision:
Impact:
Owner:
Needed By:
Blocking:
Final Decision:
Date:
```

Decision 中的 `Action After Decision` 必须写明决定后谁要做什么，例如“Codex 更新 LINEAR_POLICY，Owner 把 DEC-003 移到 Done”。

## Carry-over Revalidation Issue 最小内容

当旧版本 Issue 原范围已完成，但后续反馈应在下一版本重新验证时，必须创建或更新下一版本承接 Issue。

```text
Feature ID:
Module:
Target Version:
Type: carry-over revalidation
Source Issues:
Source Comments:
Problem:
Revalidation Scenarios:
Expected Result:
Acceptance Criteria:
Owner Acceptance Path:
Trace Comments:
```

旧 Issue 必须留下 bilingual closeout comment，新 Issue 必须链回来源 Issue。不要直接移动旧 issue。

## 首次导入规则

首次导入 Linear 必须分三步：

1. 生成 `audit/LINEAR_IMPORT_PLAN.md`。
2. 人工确认 Import Plan。
3. 人工明确批准后，Codex 才能使用 Linear MCP 写入。

授权语必须明确，例如：

```text
批准写入 Linear。
```

没有明确授权，不得写入。

硬规则：首次批量写入 Linear 必须人工确认。

## Phase 1 特别限制

Phase 1 中，Codex 不得改变 Linear 状态。

如果 Codex 读取 Linear 后发现状态可能错误，只能写入审计建议：

```text
建议把 <Issue> 从 <old status> 改为 <new status>，原因是...
```

状态变化必须由人确认。

## 疑似重复处理

Codex 发现疑似重复时：

允许：

- 标记为 Duplicate Candidate。
- 记录重复证据。
- 建议合并或关闭。

禁止：

- 自动关闭 Issue。
- 自动删除 Issue。
- 自动合并描述。
- 自动迁移状态。

## Linear Intake Scan

宽泛 Linear 命令必须使用 `LINEAR_INTAKE.md`。

每次 scan 的输出必须包含：

- Scan Scope / 扫描范围。
- Scanned / 已扫描。
- Created / 已创建。
- Updated / 已更新。
- Skipped / 已跳过。
- Blockers / 阻塞项。
- Next Action / 下一步。

如果是 dry-run，必须明确：

```text
Write Actions / 写入动作: None. Dry run only.
```

## Automation Boundary

v0.3 允许 manual trigger 和 scheduled dry-run/advisory Linear intake。

v0.3 禁止：

- scheduled job 自动修改本地代码。
- 自动批准 UAT。
- 自动扩大当前版本 scope。
- 未经批准自动关闭、取消、移动或重新分配 Issue。
- 重复创建 comment、Issue 或 status update。

自动化详细规则见 `AUTOMATION_POLICY.md`。

## 批量写入规则

每批建议不超过 20 个 Issue。

每批写入前，Codex 必须说明：

- 本批准备创建什么。
- 是否有重复风险。
- 是否有字段缺失。

每批写入后，Codex 必须说明：

- 成功创建的 Issue。
- 跳过的 Issue。
- 失败的 Issue。
- 需要人工处理的问题。

## 不得覆盖规则

Codex 不得在未确认情况下覆盖：

- Issue 标题。
- Issue 描述。
- Issue 状态。
- Assignee。
- Project。
- Label。
- 评论。
- Decision 结论。

## Linear MCP 操作前自检

在任何写操作前，Codex 必须回答：

- 这是首次批量写入吗？
- 人工是否已授权？
- 是否可能创建重复 Issue？
- 是否会修改现有内容？
- 是否涉及状态变化？
- 是否有业务不确定？

任一答案不清楚时，停止并询问。
