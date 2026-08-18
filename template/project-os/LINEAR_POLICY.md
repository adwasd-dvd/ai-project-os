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
Expected Behavior:
Acceptance Criteria:
Evidence:
Dependencies:
Risks:
Decisions:
GitHub:
UAT:
```

## Decision Issue 描述最小内容

```text
Decision:
Context:
Options:
Recommendation:
Impact:
Owner:
Needed By:
Blocking:
Final Decision:
Date:
```

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

