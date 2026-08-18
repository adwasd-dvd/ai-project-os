# GITHUB_POLICY

本文定义 GitHub 使用规则。

GitHub 是代码、PR、测试和版本事实来源。

## 分支规则

推荐分支名：

```text
feature/<feature-id>-short-title
bugfix/<feature-id-or-bug-id>-short-title
chore/<short-title>
release/vX.Y.Z
```

示例：

```text
feature/crm-001-customer-search
bugfix/uat-014-login-timeout
release/v0.1.0
```

## Commit 规则

Commit 应该清楚引用 Feature ID 或 Bug ID。

推荐格式：

```text
<type>(<feature-id>): <summary>
```

示例：

```text
feat(CRM-001): add customer search and pagination
fix(UAT-014): handle login timeout
```

## PR 规则

每个 PR 应尽量对应一个 Feature、Bug 或 Chore。

PR 标题推荐：

```text
[FEATURE_ID] 简短标题
```

PR 描述必须包含：

```text
## Summary

## Linear

## Target Version

## Changes

## Tests

## Screenshots / Evidence

## Risks

## UAT Notes
```

## 测试规则

Codex 完成开发后必须运行相关测试。

如果不能运行测试，必须说明：

- 为什么不能运行。
- 影响范围。
- 建议由谁补测。
- 是否阻塞 PR 或 UAT。

## Review 规则

Review 必须关注：

- 是否满足 Feature。
- 是否超出 Scope。
- 是否破坏现有流程。
- 是否有测试。
- 是否需要数据迁移。
- 是否有安全、权限、隐私风险。

Review 不替代 UAT。

## CI 规则

CI 结果是版本质量的重要事实。

CI 失败时：

- 不得忽略。
- 必须定位原因。
- 如果决定带失败发布，必须由人明确批准并记录风险。

## Tag 规则

正式版本发布时创建 Git tag：

```text
vX.Y.Z
```

Tag 必须对应：

- 已通过 UAT 的代码。
- 明确的 release notes。
- Linear 中对应版本范围。

## Release Notes

GitHub Release 应包含：

- 版本目标。
- 完成 Feature。
- 修复 Bug。
- 已知限制。
- UAT 结论。
- 主要 PR。
- 部署或回滚说明。

## Codex 与 GitHub

Codex 可以：

- 准备 PR 描述。
- 读取 PR 和 CI。
- 根据失败测试修复代码。
- 生成 release notes 草稿。

Codex 不可以：

- 把 Review 通过当 UAT 通过。
- 在没有人工确认时发布正式版本。
- 删除他人分支或 tag。
- 强行覆盖远端历史。

