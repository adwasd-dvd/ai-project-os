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
请读取 project-os/UAT_TEMPLATE.md 和当前 UAT 记录。

把 UAT 发现的问题分类为：
- 当前版本立即修
- Patch 版本
- 下一版本
- Backlog
- Decision

不要自动实现新需求。
如果需要修当前版本阻塞问题，请先列出对应 Feature ID 或 Bug ID 和目标版本。
```

