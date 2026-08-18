# FEATURE_INVENTORY

本文件由 Codex 在 Phase 1 Audit 中生成或更新。

用途：列出项目中已发现的 Feature，判断当前状态，并为 Linear Import Plan 提供基础。

状态必须谨慎。看见部分代码不等于 Feature 完成。

## Status Definitions

| Status | Meaning |
|---|---|
| Done | 代码、流程、测试或证据显示基本完成，但仍需人工确认 |
| Partial | 有部分实现，但缺少关键行为、测试或验收 |
| Not Started | 未发现实现证据 |
| Unknown | 证据不足，不能判断 |
| Duplicate Candidate | 疑似与其他 Feature 重复 |
| Needs Decision | 业务或技术规则不明确 |

## Feature Inventory

| Feature ID | Module | Title | Current Status | Target Version | Evidence | Missing Tests | Acceptance Gap | Linear Action | Confidence |
|---|---|---|---|---|---|---|---|---|---|
|  |  |  | Done / Partial / Not Started / Unknown |  |  |  |  | Create / Update / Skip / Needs Review | High / Medium / Low |

## Features By Module

### Module: `<name>`

```text
- <FEATURE-ID> <title> - <status>
```

## Completed Candidates

这些只是候选完成，仍需人工确认。

| Feature ID | Why It Looks Done | Evidence | Remaining Risk |
|---|---|---|---|
|  |  |  |  |

## Partial Candidates

| Feature ID | Implemented | Missing | Evidence |
|---|---|---|---|
|  |  |  |  |

## Not Started Candidates

| Feature ID | Expected Behavior | Evidence of Absence | Notes |
|---|---|---|---|
|  |  |  |  |

## Unknown Candidates

| Feature ID | Why Unknown | What To Ask / Inspect Next |
|---|---|---|
|  |  |

## Suggested Target Version Assignment

| Version | Features | Reason |
|---|---|---|
| v0.1.0 |  |  |
| v0.1.1 |  |  |
| v0.2.0 |  |  |
| Backlog |  |  |

## Human Review Checklist

```text
- [ ] Feature IDs are acceptable.
- [ ] Module mapping is acceptable.
- [ ] Status judgments are acceptable.
- [ ] Target versions are acceptable.
- [ ] Missing tests and acceptance gaps are understood.
```

