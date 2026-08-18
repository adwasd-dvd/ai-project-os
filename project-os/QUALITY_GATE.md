# QUALITY_GATE

本文定义每个阶段的质量门禁。

质量门禁的目的不是增加流程，而是防止 AI 和人把“做了一点”误认为“可以交付”。

## Ready for Development

Feature 进入开发前必须满足：

- 有 Feature ID。
- 有 Linear Issue 或等价记录。
- 有目标版本。
- 有模块归属。
- 有清楚的问题或用户价值。
- 有验收标准。
- 无阻塞 Decision。
- 依赖项已识别。
- 测试要求已说明。

不满足时，Codex 必须停止并列出缺口。

## Ready for PR

提交 PR 前必须满足：

- 改动范围与 Feature ID 对应。
- 无明显无关改动。
- 相关测试已运行。
- 新增或修改行为有测试覆盖，或说明为什么暂不覆盖。
- 文档或配置变更已说明。
- 已记录风险和已知限制。

## Ready for Review

PR 进入 Review 前必须包含：

- Feature ID。
- Linear 链接或引用。
- 目标版本。
- 变更摘要。
- 测试结果。
- 截图或录屏，如果是 UI 变更。
- 数据迁移说明，如果涉及数据库。
- 回滚建议，如果风险较高。

## Review Pass

Review 通过表示：

- 代码结构可接受。
- 改动范围可接受。
- 测试结果可接受。
- 没有明显阻塞风险。

Review 通过不表示：

- 业务验收通过。
- 版本可以发布。
- UAT 可以跳过。

## Ready for UAT

进入 UAT 前必须满足：

- 当前版本 Included Feature 已完成或明确移出。
- 阻塞 Bug 已清零。
- 关键测试通过。
- UAT 场景已列出。
- UAT 环境或运行方式已明确。
- 已知限制已写明。

## UAT Pass

UAT Pass 必须由人给出。

UAT Pass 需要：

- 验收人姓名或角色。
- 验收日期。
- 验收版本。
- 验收场景。
- 结论。
- 遗留问题分类。

Codex 不得自行给出 UAT Pass。

## Ready for Release

发布前必须满足：

- UAT Pass。
- GitHub CI 通过，或人工批准带风险发布。
- tag/release notes 准备完成。
- Linear 中版本状态已更新。
- 已知限制被 Owner 接受。

## Blocker 定义

以下情况视为 Blocker：

- 核心流程无法完成。
- 数据错误或丢失风险。
- 权限、安全、隐私明显不符合要求。
- UAT 负责人拒绝通过。
- 目标版本 Feature 无法验收。
- 生产部署无法启动或回滚。

## Codex 汇报质量格式

Codex 每次完成开发或修复后，必须给出：

```text
Feature ID:
Target Version:
Status:
Changes:
Tests:
Risks:
Needs Human Check:
New Decisions:
New Backlog Items:
```

