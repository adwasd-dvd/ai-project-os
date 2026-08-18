# RELEASE_POLICY

本文定义版本推进规则。

核心原则：

```text
每个正式版本都有明确范围。
每个正式版本必须人工 UAT。
未通过 UAT，不得进入下一正式版本。
```

## 版本命名

推荐使用语义化版本：

```text
v0.1.0
v0.1.1
v0.2.0
v1.0.0
```

### 正式版本

例如：

```text
v0.1.0
v0.2.0
v1.0.0
```

正式版本必须：

- 有明确版本目标。
- 有 Feature 范围。
- 有 UAT 记录。
- 有 GitHub tag。
- 有 release notes。

### Patch 版本

例如：

```text
v0.1.1
v0.1.2
```

Patch 版本只处理：

- 当前正式版本的阻塞 Bug。
- UAT 后必须立即修的问题。
- 不改变核心范围的小修正。

Patch 版本不得塞入新 Feature。

## 版本范围

每个版本必须明确：

- Included：本版本必须完成。
- Excluded：明确不做。
- Deferred：延期到未来版本。
- Decisions：上线前必须解决。
- UAT Owner：谁验收。

## 当前版本变更规则

当前版本开发期间，任何新增内容必须先分类：

| 分类 | 处理方式 |
|---|---|
| 当前版本立即修 | 只限阻塞 UAT 或核心流程的问题 |
| Patch 版本 | 当前版本发布后小修 |
| 下一版本 | 放入下一正式版本规划 |
| Backlog | 只记录，不排期 |
| Decision | 等人工判断 |

Codex 不得因为“顺手”把 Backlog 或下一版本内容加入当前版本。

## Release Planning Checklist

进入版本开发前，必须确认：

- 版本号已定。
- 版本目标已定。
- Included Feature 已列出。
- 每个 Included Feature 都有 Feature ID。
- 每个 Included Feature 都有目标版本。
- 每个 Included Feature 都有验收标准。
- 阻塞 Decision 已清理。
- UAT 负责人已定。
- GitHub 分支策略已定。

## Version Freeze

当版本进入 UAT 前，进入 Version Freeze。

Freeze 后只允许：

- 修复阻塞 Bug。
- 修复 UAT 必须通过的问题。
- 更新文档、release notes、测试说明。

Freeze 后不允许：

- 新增 Feature。
- 扩大验收标准。
- 做无关重构。
- 修改非阻塞交互细节。

## UAT Gate

每个正式版本必须有人工 UAT 结论。

允许发布的结论格式：

```text
UAT 通过，允许发布 vX.Y.Z。
```

不允许发布的结论格式：

```text
UAT 未通过，必须先处理以下问题。
```

Codex 不能代替这个结论。

## 下一版本启动规则

只有满足以下条件，才可以启动下一正式版本：

- 当前正式版本 UAT 已通过，或明确取消。
- 当前版本的阻塞问题已清零或转入 patch。
- GitHub tag/release 已创建，或人工明确决定暂不发布 tag。
- Linear 中当前版本状态已关闭或归档。
- 下一版本范围已人工确认。

## Release Notes 最小格式

```text
# Release vX.Y.Z

## Summary

## Included Features

## Fixed Bugs

## Known Limitations

## UAT Result

## GitHub
- Tag:
- PRs:
- CI:
```

