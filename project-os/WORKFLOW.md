# WORKFLOW

本文定义从想法到发布的统一流程。

## 总流程

```text
Idea
-> Triage
-> Decision if needed
-> Feature
-> Ready
-> Development
-> PR
-> Review
-> UAT
-> Accepted
-> Release
```

## Existing Project Intake / 现有项目接管

对已存在的成熟、混乱或上下文不完整项目，业务开发流程前必须先执行：

```text
Phase 0 Self-Check
-> Phase 0.5 Whitebox Discovery
-> Phase 1 Audit
-> Human Baseline Confirmation
-> Linear Import
-> Release Planning
-> Development
```

Phase 0.5 必须读取 `WHITEBOX_PROTOCOL.md`，生成 `discovery/` 下的白盒报告。

重要结论必须区分：

```text
Observed
Derived
Claimed
Inferred
Contradicted
Unknown
```

且必须记录 Evidence、Confidence 和 Next Verification。

Scanner 发现不等于可直接开发。新发现仍必须进入 Decision、Feature、Bug、Backlog 或验证队列。

## 1. Idea

Idea 是任何新想法、需求、反馈、灵感或用户抱怨。

Idea 不等于 Feature。

Codex 看到新 Idea 时必须：

- 记录来源。
- 判断是否属于当前版本。
- 如果不确定，创建 Decision。
- 不得自动实现。

## 2. Triage

Triage 负责决定这个事项属于哪一类：

- Feature
- Bug
- Chore
- Decision
- UAT Feedback
- Duplicate
- Backlog

详细分类规则见 `REQUIREMENT_MANAGEMENT.md`。

Triage 必须回答：

- 是否已有类似事项？
- 是否影响当前版本？
- 是否阻塞开发或验收？
- 是否需要业务确认？
- 是否需要技术确认？

## 3. Decision

当业务或技术方向不明确时，必须先 Decision。

Decision 没解决前，相关 Feature 不得进入 Ready。

Decision 结果必须写入：

- Linear Decision Issue。
- 相关 Feature 描述。
- 必要时写入 `audit/RISKS_AND_DECISIONS.md` 或项目文档。

## 4. Feature

Feature 是可以被开发、测试、验收的一块产品能力。

每个 Feature 必须有：

- Feature ID。
- 标题。
- 模块。
- 目标版本。
- 用户价值。
- 验收标准。
- 状态。
- Owner 或确认人。

缺少 Feature ID 或目标版本时，不得进入正式开发。

## 5. Ready

Ready 表示可以开发。

Ready 前必须满足：

- Feature ID 已定。
- 目标版本已定。
- 验收标准已定。
- 主要业务规则已定。
- 依赖项已识别。
- 无阻塞 Decision。
- 测试要求已说明。

## 6. Development

Development 由 Operator 使用本地 Codex 执行。

开发期间 Codex 必须：

- 保持改动范围对应 Feature。
- 记录发现的新需求。
- 遇到业务不确定停下来。
- 更新测试。
- 汇报风险。

不得：

- 顺手做当前 Feature 之外的事。
- 自动把新需求加入当前版本。
- 因为发现代码问题就大范围重构。

如果开发请求来自宽泛 Linear 口令，Codex 必须先执行 `LINEAR_INTAKE.md`，确认目标 Feature、目标版本和阻塞 Decision。

## 7. PR

每个 PR 应该对应：

- 一个 Feature。
- 或一个清楚的 Bug。
- 或一个明确的 Chore。

PR 必须包含：

- Feature ID 或 Linear Issue。
- 目标版本。
- 变更摘要。
- 测试结果。
- 风险说明。
- UAT 影响。

## 8. Review

Review 负责检查代码、风险、测试和范围。

Review 不等于 UAT。

Review 通过表示代码层面可以进入下一步，不表示业务验收通过。

## 9. UAT

UAT 必须由人执行。

UAT 必须使用 `UAT_TEMPLATE.md` 或 Linear 中等价记录。

UAT 期间发现的问题必须分类：

- 当前版本立即修。
- Patch 版本。
- 下一版本。
- Backlog。
- Decision。

## 10. Accepted

Accepted 表示人工确认该 Feature 或版本满足验收标准。

Codex 不能单独把任何正式版本标记为 Accepted。

## 11. Release

Release 以 GitHub tag/release 为事实来源。

正式发布前必须满足：

- 当前版本 UAT 通过。
- 关键测试通过。
- 已知阻塞项清零。
- release notes 已准备。
- tag 已创建。

版本范围、patch、分阶段交付和旧版本 carry-over 规则见 `VERSION_PLANNING.md` 和 `RELEASE_POLICY.md`。

## 状态流转建议

```text
Backlog
-> Needs Decision
-> Ready
-> In Progress
-> In Review
-> Ready for UAT
-> Accepted
-> Released
```

辅助状态：

```text
Blocked
Duplicate Candidate
Won't Do
Deferred
```

## v0.3 Human/Codex Handoff

v0.3 的基础流程不再要求人类维护 `next:*` label。

基础规则：

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

常见循环：

```text
Human writes requirement or feedback
-> If Codex should work: Todo + unassigned
-> Codex starts: In Progress + unassigned
-> Codex finishes: In Review + assigned to Owner/reviewer
-> Human passes: Done
-> Human fails: comment feedback + Todo + unassigned
```

中文循环：

```text
人类写需求或反馈
-> 如果要交给 Codex：Todo + unassigned
-> Codex 开工：In Progress + unassigned
-> Codex 完成：In Review + assign 给 Owner/reviewer
-> 人类通过：Done
-> 人类不通过：评论反馈 + Todo + unassigned
```

Codex 看到 `Todo + unassigned` 时，仍然必须先检查 Ready 条件：Feature ID、目标版本、验收标准、阻塞 Decision 和测试计划。

Codex 完成后不得把正式版本或 Feature 直接验收为通过。`In Review + assigned` 是交给人类，不是完成证明。

## Codex 遇到新发现时的处理

| 新发现 | Codex 应做 | Codex 不得做 |
|---|---|---|
| 新需求 | 记录为 Backlog 或 Decision | 直接实现 |
| 疑似 Bug | 记录证据并建议分类 | 擅自加入当前版本 |
| 重复 Feature | 标记疑似重复 | 自动关闭其中一个 |
| 业务规则不清 | 创建 Decision | 猜一个规则继续做 |
| 测试缺失 | 标记测试缺口 | 声称已验收 |
| 文档与代码冲突 | 记录 Contradicted、证据和下一步验证 | 静默选一个当真 |
| 高影响但低置信度 | 转入验证 Feature 或 Decision | 直接按推断改代码 |

## v0.3 日常 Linear Loop

```text
Check Linear
-> Intake Scan
-> Route by status + assignee
-> Classify comments/status changes
-> Decide: start work, ask Decision, carry over, backlog, or stop
-> Execute only if Feature ID + Target Version + Acceptance Criteria are ready
-> Report changes, tests, Linear writes, skipped items, blockers
```

宽泛 Linear loop 必须防止：

- 只扫描当前版本而漏掉旧版本 active feedback。
- 把评论当作自动批准。
- 把下版本反馈直接塞进当前版本。
- 把旧版本已完成 Issue 直接移动到下一版本。
- 把 scheduled scan 当作自动开发触发器。
- 把 `Todo + assigned` 误判为 Codex-ready。
- 要求人类维护 `next:*` label 才能完成普通交接。
