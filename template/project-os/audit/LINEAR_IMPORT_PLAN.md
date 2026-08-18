# LINEAR_IMPORT_PLAN

本文件由 Codex 在 Phase 1 Audit 中生成或更新。

用途：在写入 Linear 前，先提供可审查、可确认、可分批执行的导入计划。

未经人工确认，不得通过 Linear MCP 写入。

## Import Status

```text
Status: Draft / Confirmed / Approved for Write / Imported / Partially Imported
Prepared By:
Prepared Date:
Confirmed By:
Write Approved By:
Imported Date:
```

## Safety Rules

- 首次批量写入 Linear 前必须人工确认。
- Phase 1 不得写入 Linear。
- 不得删除 Linear 既有内容。
- 不得覆盖 Linear 既有 Issue。
- 疑似重复必须停下来问人。
- 状态变化必须由人确认。

## Proposed Linear Structure

### Team

```text
Team:
```

### Projects

| Project Name | Purpose | Version | Create / Use Existing | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

### Labels

| Label | Type | Purpose | Create / Use Existing |
|---|---|---|---|
| module: | Module |  |  |
| type:feature | Type |  |  |
| type:bug | Type |  |  |
| type:decision | Type |  |  |
| type:uat-feedback | Type |  |  |

### Status Mapping

| AI Project OS Status | Linear Status | Notes |
|---|---|---|
| Backlog |  |  |
| Needs Decision |  |  |
| Ready |  |  |
| In Progress |  |  |
| In Review |  |  |
| Ready for UAT |  |  |
| Accepted |  |  |
| Released |  |  |

## Existing Linear Preflight

如果 Linear MCP 可用，Phase 3 写入前必须填充。

| Existing Item | Type | Possible Match | Risk | Action |
|---|---|---|---|---|
|  |  |  | Duplicate / Conflict / Safe |  |

## Proposed Issues To Create

| Batch | Feature ID | Title | Type | Module | Target Version | Status | Labels | Depends On | Duplicate Risk |
|---|---|---|---|---|---|---|---|---|---|
| 1 |  |  | feature |  |  |  |  |  | Low / Medium / High |

## Proposed Issues To Update

默认不更新现有 Issue。只有人工确认后才允许更新。

| Existing Issue | Proposed Change | Reason | Requires Approval |
|---|---|---|---|
|  |  |  | Yes |

## Proposed Decisions To Create

| Decision ID | Title | Blocking | Owner | Needed By |
|---|---|---|---|---|
|  |  |  |  |  |

## Proposed UAT Items

| UAT Item | Version | Related Feature | Notes |
|---|---|---|---|
|  |  |  |  |

## Items To Skip

| Item | Reason | Follow-up |
|---|---|---|
|  |  |  |

## Batch Plan

### Batch 1

```text
Purpose:
Items:
Risk:
```

### Batch 2

```text
Purpose:
Items:
Risk:
```

## Approval Block

人工确认前保持未勾选。

```text
- [ ] Baseline confirmed.
- [ ] Import plan reviewed.
- [ ] Duplicate candidates reviewed.
- [ ] Linear workspace/team confirmed.
- [ ] First bulk write approved.
```

明确授权语：

```text
批准写入 Linear。
```

## Import Result Log

每批写入后追加记录。

| Batch | Date | Created | Skipped | Failed | Notes |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Codex Phase 3 Stop Conditions

Codex 在以下情况必须停止并询问：

- 没有明确授权写入。
- Linear 中发现疑似重复。
- 目标 team/project 不确定。
- 状态映射不确定。
- 写入会覆盖既有内容。
- 业务状态和代码证据冲突。

