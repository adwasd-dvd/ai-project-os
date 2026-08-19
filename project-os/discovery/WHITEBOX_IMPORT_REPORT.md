# WHITEBOX_IMPORT_REPORT

This report is the management handoff from detailed discovery to human baseline confirmation and Linear planning.

本报告把详细 discovery 交接给人工 baseline 确认和 Linear 规划。

## Header / 头部

```text
Project:
Repository:
Git Commit:
Evidence Generated:
Prepared By:
Prepared Date:
Linear Description Language: English + Chinese
Status: Draft / Ready for Human Review / Confirmed
```

## Detailed Evidence / 详细证据

| Report | Status | Last Updated | Important Finding | Confidence | Link or Path |
|---|---|---|---|---|---|
| Project Map | Draft / Partial / Complete |  |  |  | `PROJECT_MAP.md` |
| Dependency Map |  |  |  |  | `DEPENDENCY_MAP.md` |
| Document Inventory |  |  |  |  | `DOCUMENT_INVENTORY.md` |
| Settings and Data Register |  |  |  |  | `SETTINGS_AND_DATA_REGISTER.md` |
| Logic and Boundary Audit |  |  |  |  | `LOGIC_BOUNDARY_AUDIT.md` |
| Scanner Evidence |  |  |  | Derived | `SCAN_EVIDENCE.json` |

## Executive Whitebox Summary / 白盒执行摘要

```text
What the project does:
How it is structured:
How it runs:
Where its important data lives:
Which external systems it depends on:
Most important verified fact:
Most important contradiction:
Most important unknown:
Highest-priority verification:
Overall confidence:
Coverage limit:
```

## Confidence Dashboard / 置信度仪表盘

| Area | High | Medium | Low | Unknown | High-Impact Low-Confidence | Owner Action |
|---|---:|---:|---:|---:|---:|---|
| Project shape |  |  |  |  |  |  |
| Dependencies |  |  |  |  |  |  |
| Documentation |  |  |  |  |  |  |
| Settings and data |  |  |  |  |  |  |
| Logic and boundaries |  |  |  |  |  |  |

## Contradictions and Unknowns / 矛盾与未知项

| Finding ID | Summary | Impact | Evidence | Confidence | Next Verification | Blocks Baseline | Owner |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  | Yes / No |  |

## Proposed Linear Creates / 建议创建的 Linear 事项

| Feature ID | Type | Title | Target Version | Source Finding | Action Steps | Expected Result | Acceptance Criteria | Labels | Assignee | Risk |
|---|---|---|---|---|---|---|---|---|---|---|
|  | Feature / Bug / Decision / Chore |  |  |  |  |  |  |  |  |  |

## Proposed Linear Updates / 建议更新的 Linear 事项

| Existing Issue | Source Finding | Current Claim | Proposed Change | Action Steps | Expected Result | Conflict Risk | Human Confirmation Needed |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  | Yes |

## Proposed Decisions / 建议决策

| Decision ID | Question | Context | Options | Recommendation | Impact | Owner | Needed By | Blocking |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |

## Skipped or Deferred / 跳过或延期

| Finding | Reason | Disposition | Target Version or Backlog | Evidence |
|---|---|---|---|---|
|  | Duplicate / Insufficient Evidence / Out of Scope / v0.5 Security / Needs Access |  |  |  |

## Copy-ready Linear Project Description / 可直接使用的 Linear 项目说明

Replace placeholders and keep this block compact.

替换占位符，保持该区块紧凑。

```markdown
## Project Whitebox / 项目白盒

Evidence freshness / 证据更新: <date + commit>

System shape / 系统形态: <one paragraph English + Chinese>

Confidence / 置信度: <overall + important low-confidence area>

Top risks / 主要风险:
- <risk + finding ID>

Contradictions / 矛盾:
- <contradiction + next verification>

Unknowns / 未知项:
- <unknown + owner>

Evidence / 证据:
- Project map: <GitHub link>
- Dependency map: <GitHub link>
- Document inventory: <GitHub link>
- Settings and data register: <GitHub link>
- Logic and boundary audit: <GitHub link>
- Whitebox import report: <GitHub link>

Next verification / 下一步验证: <action + expected result>
```

## Human Confirmation / 人工确认

Before Phase 3 Linear writes, record:

Phase 3 Linear 写入前必须记录：

```text
Whitebox reports reviewed by:
Date:
Coverage accepted: Yes / No
Blocking contradictions resolved or routed: Yes / No
Baseline confirmed: Yes / No
Linear write approved: Yes / No
Notes:
```

No approval means no first bulk write.

未批准就不得首次批量写入。
