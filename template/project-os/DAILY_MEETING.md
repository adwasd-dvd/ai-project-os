# DAILY_MEETING

本文定义每日同步方式。

目标是让 Owner、项目经理、Operator、顾问和 Codex 保持同一张图。

## 建议时长

15 分钟。

## 参与者

- Owner 或业务代表。
- Project Manager。
- Operator A/B。
- Consultant，如有。
- 本地 Codex，由 Operator 操作。

## 固定议程

1. 当前版本目标是否变化？
2. 昨天完成了哪些 Feature / Bug？
3. 今天计划做哪些 Feature / Bug？
4. 有哪些 Blocker？
5. 有哪些 Decision 等人拍板？
6. 有哪些新需求只记录不执行？
7. 当前版本是否仍能进入 UAT？

## 每日状态表

| Item | Feature ID | Version | Owner | Status | Blocker | Next Action |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## Codex 会前准备 Prompt

```text
请读取 project-os/DAILY_MEETING.md、project-os/RELEASE_POLICY.md、project-os/QUALITY_GATE.md。

请整理今天的项目同步摘要：
- 当前版本状态
- 昨天完成项
- 今天建议推进项
- Blocker
- Decision
- 新发现但不得自动实现的需求
- UAT 风险

只整理，不修改代码，不写入 Linear，除非我明确要求。
```

## Codex 会后整理 Prompt

```text
请根据刚才会议内容整理行动项。

要求：
- 明确哪些是当前版本必须做。
- 哪些进入 Patch。
- 哪些进入下一版本。
- 哪些进入 Backlog。
- 哪些需要 Decision。
- 不要自动实现任何新需求。
- 如需写入 Linear，请先输出写入计划，等待确认。
```

## 禁止事项

- 不在会议中直接把新想法塞进当前版本。
- 不用口头共识替代 Linear 状态。
- 不让 Codex 根据模糊描述直接开工。
- 不把 Review 通过当作 UAT 通过。

