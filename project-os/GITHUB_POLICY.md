# GITHUB_POLICY

本文定义 GitHub 使用规则。

GitHub 是代码、PR、测试和版本事实来源。

Private repository is not a secret store。密码、token、private key、真实生产连接信息、个人绝对路径和未分类的聊天导出不得因为仓库私有就进入 Git。

## Publication Profile

任何 GitHub 写入前都必须按 `REPO_PUBLICATION_POLICY.md` 记录目标 profile：

- `private`：有限成员可见，但仍禁止 secret。
- `team`：团队共享的稳定规则、代码和经审查文档。
- `public`：任何人均可读取、fork 和长期引用的内容。

Agent 文档必须另外按 `AGENT_DOC_POLICY.md` 确认 local-only、team-shared、organization-shared 或 public-safe 模式。

## 分支规则

推荐分支名：

```text
feature/<feature-id>-short-title
bugfix/<feature-id-or-bug-id>-short-title
chore/<short-title>
release/vX.Y.Z
codex/upgrade-vX.Y.Z
```

示例：

```text
feature/crm-001-customer-search
bugfix/uat-014-login-timeout
release/v0.1.0
codex/upgrade-v0.8.0
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

## Safety Evidence
- Publication profile:
- Scan scope:
- Block findings:
- Review dispositions:

## UAT Notes
```

创建或更新 PR 前，对 staged 内容运行：

```bash
python3 project-os/tools/safety_scan.py --root . --profile private --scope staged --fail-on-block --summary
```

如果目标是 public，合并或发布前还要检查最终 tracked 集合：

```bash
python3 project-os/tools/safety_scan.py --root . --profile public --scope tracked --fail-on-block --summary
```

scanner 输出不得包含 matched value、source line、environment value 或 file content。

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

需要长期引用的证据链接应指向 tag 或保留分支上的 commit，不应只指向即将删除的临时开发分支。

## Release Notes

GitHub Release 应包含：

- 版本目标。
- 完成 Feature。
- 修复 Bug。
- 已知限制。
- UAT 结论。
- 主要 PR。
- 部署或回滚说明。
- publication profile 和 manifest disposition。
- Release asset SHA-256。

Release zip 放在 GitHub Releases，不作为源码长期提交。上传后必须核对 digest 与 closeout 记录一致。

## Secret Incident

发现疑似有效凭证时：

1. 停止 commit、push、PR、merge 和 release。
2. 只记录规则 ID、路径、严重度和修复建议，不复制命中值。
3. 由人工判断并轮换或撤销凭证。
4. 如果内容已进入 Git 历史，由人工批准历史清理方案。
5. 重新扫描目标发布集合，Block 为零后才能继续。

Codex 不得自行轮换凭证、删除文件或改写远端历史。

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
- 把 private repository 当作凭证库。
