# FEATURE_TEMPLATE

复制本模板创建 Feature。

## Feature Header

```text
Feature ID:
Title:
Module:
Type: Feature
Target Version:
Linear Issue:
Linear Description Language: English + Chinese
Source:
Source Issues:
Source Comments:
Carry-over From:
GitHub PR:
Owner:
Status:
Current Assignee:
Handoff Route: Human Queue / Codex Queue / Review Queue / Blocked
Confidence:
```

## Problem

要解决什么问题？

```text

```

## Whitebox Trace / 白盒追踪

如果本 Feature 来自既有项目白盒发现，必须填写；新项目或非白盒来源可写 `N/A`。

```text
Finding ID:
Finding State: Observed / Derived / Claimed / Inferred / Contradicted / Unknown
Evidence:
Evidence Freshness:
Confidence: High / Medium / Low / Unknown
Unknowns:
Contradictions:
Next Verification:
```

高影响但低置信度、`Inferred`、`Contradicted` 或 `Unknown` 的发现，默认只能创建验证任务或 Decision，不能把推测直接当作目标行为开发。

## Safety / Publication Trace

所有将进入 Git、团队共享或 Release 的 Feature 都必须填写。

```text
Asset Classification: Local Only / Team Shared / Private Repo / Public Safe
Publication Profile: local / private / team / public
Publication Destination:
Safety Evidence:
Block Findings:
Review Findings:
Review Dispositions:
Agent Document Mode:
Project Memory / Doc Gaps:
Human Safety Decision:
```

证据只记录规则 ID、路径、分类、处置和修复建议，不得复制命中值、源文件行、环境变量值或文件正文。

## User / Actor

谁会使用或受影响？

```text

```

## Expected Behavior

完成后应该是什么样？

```text

```

## Action Steps

执行者需要做什么？写给 Operator / Codex / Owner 看。

```text
1.
2.
3.
```

## Human/Codex Handoff

基础路由：

```text
Assigned = human queue
Unassigned = Codex queue
Status = lifecycle
Labels = classification only, optional for advanced workflows
```

当前交接：

```text
Current Status:
Current Assignee:
Next Actor: Human / Codex
Next Action:
If Human Fails UAT: comment feedback + unassign + Todo
If Human Passes UAT: Done
```

## Expected Result

执行后应该看到、得到或验证到什么？

```text

```

## Acceptance Criteria

必须可以被人工验收。

```text
- [ ] 
- [ ] 
- [ ] 
```

## Out of Scope

本 Feature 明确不做什么？

```text

```

## Dependencies

依赖哪些 Feature、Decision、数据、接口、权限或第三方服务？

```text

```

## Technical Notes

给 Codex 和开发者的技术上下文。

```text

```

## Test Plan

```text
- Unit:
- Integration:
- E2E:
- Manual:
```

## UAT Notes

```text
UAT Owner:
UAT Scenario:
UAT Data:
Pass Criteria:
```

## Carry-over Revalidation

如果本 Feature 是旧版本反馈承接项，必须填写：

```text
Source Issue:
Source Comment:
Original Version:
Next Version:
Revalidation Scenario:
Expected Result:
Owner Acceptance Path:
Trace Comment Added: Yes / No
```

## Risks

```text

```

## Decisions Needed

```text
- Decision:
  Owner:
  Needed By:
  Blocking:
```

## Codex Development Prompt

```text
请读取 project-os/AGENTS.md、project-os/WORKFLOW.md、project-os/QUALITY_GATE.md 和 project-os/REPO_PUBLICATION_POLICY.md。

我要开发 Feature ID: <Feature ID>。
目标版本: <Target Version>。

请先读取本 Feature、Linear Issue、相关代码和测试。
确认 Feature Ready 后再开始。
在创建 PR 前运行目标 profile 的 staged safety gate。
如果这是宽泛 Linear 扫描选中的事项，基础 Codex-ready 条件必须是 Todo + unassigned。
如果缺少 Feature ID、目标版本、验收标准或存在未解决 Decision，请停止并说明缺口。
```
