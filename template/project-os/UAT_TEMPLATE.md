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

## Whitebox Scenarios

| Scenario ID | Check | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|
| WBX-001 | Scanner dry run | Command reports repository evidence and creates no file |  |  |  |
| WBX-002 | Deterministic write and check | `--write` followed by `--check` passes without evidence drift |  |  |  |
| WBX-003 | Ignore behavior | Git-ignored and common generated/vendor paths do not enter evidence |  |  |  |
| WBX-004 | Secret-value boundary | Setting names and secret-like paths may appear; their values do not |  |  |  |
| WBX-005 | Evidence vocabulary | Important findings distinguish Observed, Claimed, Inferred, Contradicted, and Unknown |  |  |  |
| WBX-006 | Confidence honesty | High-impact low-confidence findings have a Next Verification or Decision |  |  |  |
| WBX-007 | Six report handoff | All detailed reports are usable and linked by `WHITEBOX_IMPORT_REPORT.md` |  |  |  |
| WBX-008 | Linear project summary | Bilingual summary shows freshness, shape, confidence, risks, contradictions, unknowns, and evidence links |  |  |  |
| WBX-009 | Human usefulness | Owner can explain the system shape and choose the next verification from the reports |  |  |  |
| WBX-010 | No automatic repair/import | Discovery does not change product code or bypass Linear first-write approval |  |  |  |

## Safety / Publication Scenarios

| Scenario ID | Check | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|
| SAF-001 | Four-level classification | Assets can be classified as Local Only, Team Shared, Private Repo, or Public Safe |  |  |  |
| SAF-002 | Read-only default | Scanner dry run creates no file and changes no source |  |  |  |
| SAF-003 | No secret-value output | Findings omit matched values, source lines, environment values, and file contents |  |  |  |
| SAF-004 | Scope selection | Worktree, staged, and tracked scans examine the documented file sets |  |  |  |
| SAF-005 | Profile disposition | Local, private, team, and public profiles produce deterministic Block/Review/Info dispositions |  |  |  |
| SAF-006 | Output confinement | `--write` refuses destinations outside the repository |  |  |  |
| SAF-007 | Private repo boundary | A private repository still blocks credentials and private keys |  |  |  |
| SAF-008 | Agent document mode | Local-only and shared Agent documents have an explicit owner and sharing decision |  |  |  |
| SAF-009 | Project memory audit | Chat-only claims, contradictions, and stale decisions remain visible as gaps |  |  |  |
| SAF-010 | Publication manifest | Human can record destination, evidence, Review dispositions, and Go/Block decision |  |  |  |
| SAF-011 | Release artifact digest | Generated zip has a recorded SHA-256 that matches the uploaded asset |  |  |  |
| SAF-012 | 60-second GitHub start | User can download, place `project-os/`, paste the Codex prompt, and receive the expected initial assessment |  |  |  |

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
请读取 project-os/UAT_TEMPLATE.md、project-os/LINEAR_INTAKE.md、project-os/VERSION_PLANNING.md、project-os/REPO_PUBLICATION_POLICY.md 和当前 UAT 记录。

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
