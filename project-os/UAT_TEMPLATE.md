# UAT_TEMPLATE

每个正式版本必须使用本模板或 Linear 中等价记录完成人工验收。

## UAT Header

```text
Version:
Date:
Environment:
Build / Commit:
Tester:
Owner:
Result: Pass / Fail / Conditional Pass
```

## Version Goal

```text

```

## Scope

### Included

```text
- 
```

### Excluded

```text
- 
```

## Test Scenarios

| Scenario ID | Feature ID | Scenario | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|
| UAT-001 |  |  |  |  |  |  |
| UAT-002 |  |  |  |  |  |  |

## Linear / Version Scenarios

| Scenario ID | Check | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|
| LIN-001 | Codex-authored Linear comment is bilingual | Comment includes Chinese user-facing summary |  |  |  |
| LIN-002 | Project status update is bilingual | Status update includes Chinese summary |  |  |  |
| LIN-003 | Broad Linear scan covers older-version active feedback | Run summary lists scanned old-version issue |  |  |  |
| LIN-004 | Carry-over revalidation preserves source issue | Next-version issue links to source issue and expected result |  |  |  |
| LIN-005 | Scheduled dry-run is idempotent | Two runs do not duplicate comments or issues |  |  |  |
| LIN-006 | `Todo + unassigned` routes to Codex Queue | Codex reports it as Codex-ready only after Ready checks |  |  |  |
| LIN-007 | `Todo + assigned` routes to Human Queue | Codex does not start work and reports human next action |  |  |  |
| LIN-008 | `In Review + assigned` routes to Review Queue | Codex waits for human pass/fail and does not close it |  |  |  |
| LIN-009 | Human failed UAT handoff | Comment + unassign + `Todo` lets Codex process rework next scan |  |  |  |
| LIN-010 | `next:*` label is optional | Basic handoff works without changing workflow labels |  |  |  |

## Issues Found

| ID | Description | Severity | Category | Target Version | Linear Issue | Owner |
|---|---|---|---|---|---|---|
|  |  |  | Current Fix / Patch / Next / Backlog / Decision |  |  |  |

## Required Fixes Before Release

```text
- [ ] 
```

## Patch Candidates

```text
- [ ] 
```

## Next Version Candidates

```text
- [ ] 
```

## Carry-over Revalidation

| Source Issue | Source Comment | Next Version Issue | Revalidation Scenario | Expected Result | Trace Comment | Pass/Fail |
|---|---|---|---|---|---|---|
|  |  |  |  |  | Yes / No |  |

## Backlog

```text
- [ ] 
```

## Decisions

```text
- Decision:
  Owner:
  Blocking:
```

## Final UAT Decision

选择其一：

```text
UAT 通过，允许发布 <version>。
```

```text
UAT 未通过，必须先处理以下问题：
-
```

```text
有条件通过，允许发布 <version>，但以下问题必须进入 Patch：
-
```

## Sign-off

```text
Accepted By:
Date:
Notes:
```

## Codex Follow-up Prompt

```text
请读取 project-os/UAT_TEMPLATE.md、project-os/LINEAR_INTAKE.md、project-os/VERSION_PLANNING.md 和当前 UAT 记录。

把 UAT 发现的问题分类为：
- 当前版本立即修
- Patch 版本
- 下一版本
- Backlog
- Decision
- Carry-over revalidation

不要自动实现新需求。
如果需要修当前版本阻塞问题，请先列出对应 Feature ID 或 Bug ID 和目标版本。
```
