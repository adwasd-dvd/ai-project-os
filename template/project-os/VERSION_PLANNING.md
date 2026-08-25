# VERSION_PLANNING

本文定义 AI Project OS v0.6 的版本规划、Development Train 和分阶段交付规则。

核心原则：

```text
一个可交付 Issue 只属于一个目标版本。
旧版本历史不搬家。
下一版本反馈用 carry-over revalidation 承接。
```

## Development Trains / 大批次开发

DEC-009 允许把多个相邻的小能力合并为一个 Development Train，但不能绕过版本纪律。

Train 必须：

- 指定一个正式 release version。
- 在 Linear 建立一个 Project 和明确 Included/Excluded scope。
- 所有 Feature 仍有独立 Feature ID、验收标准和 traceability。
- 合并开发期间遇到新业务方向仍需 Decision。
- 只在整个 Train 完成后做一次统一人工 UAT。
- UAT 前不 merge/tag/release，UAT 后才完成 Linear Project。

Train 不允许：

- 用“批量开发”掩盖 scope creep。
- 把多个 Feature 的证据混成无法追踪的一条说明。
- 因为内部小里程碑完成就声称正式版本已发布。
- 自动跨过 destructive、public、credential 或 business-decision gate。

AI Project OS 当前 train cadence：

```text
Development Train A -> v0.6.0 -> automation + traceability -> one UAT
Development Train B -> v0.8.0 -> release/rollback + self-upgrade -> one UAT
Internal Stable -> v1.0.0 -> end-to-end messy-project rescue -> one UAT
```

## Project Per Version

推荐每个正式版本有一个 Linear Project：

```text
AI Project OS v0.1
AI Project OS v0.3
AI Project OS v0.3
```

Project 表示版本范围，不表示代码事实。代码、PR、tag、release 的事实来源仍是 GitHub。

## Target Version

每个正式开发 Issue 必须有 `Target Version`。

规则：

- `Target Version` 必须出现在 Linear Issue 描述中。
- Issue 所在 Linear Project 应与 `Target Version` 一致。
- 如果 Issue 只是 Backlog 且未排期，可以写 `Target Version: Backlog`。
- 如果是 patch，只能写具体 patch 版本，例如 `v0.2.1`。
- 没有目标版本时，Codex 不得进入正式开发。

## 为什么一个 Issue 不跨多个版本

一个 Issue 跨多个可交付版本会造成：

- UAT 无法判断哪个版本验收通过。
- GitHub tag/release notes 无法对应 Linear 范围。
- 后续评论不知道属于旧版本修复还是下版本需求。
- Codex 容易把未来范围顺手塞进当前版本。

如果一个能力需要分阶段交付，使用 parent/child 或 staged issue。

## Staged Delivery

推荐模式：

| 层级 | 用途 | 是否开发交付 |
|---|---|---|
| Parent Issue 或 Linear Document | 描述大能力、背景和总目标 | No |
| Child Issue v0.2 | 第一阶段可验收范围 | Yes |
| Child Issue v0.3 | 第二阶段可验收范围 | Yes |
| Child Issue Future | 后续计划或 Backlog | Not yet |

示例：

| Issue | Target Version | Acceptance Focus |
|---|---|---|
| AIPOS-011 | v0.2.0 | 自动化边界和 follow-up 设计 |
| AIPOS-016 | v0.2.0 | cron-ready intake runner contract |
| AIPOS-020 | v0.3.0 | 可运行的 scheduled intake command |
| AIPOS-021 | Future | 自动启动代码工作的权限模型 |

## 移入下一版本

可以移动原 Issue 到下一版本的情况：

- Issue 尚未开始开发。
- 原始范围整体被重新排期。
- 没有旧版本 UAT 或 closeout 事实需要保留。
- Owner 明确确认目标版本变化。

不要移动原 Issue 的情况：

- 原 Issue 原始范围已经完成。
- 旧版本已经进入 UAT 或 closeout。
- 新内容来自后续评论或 late feedback。
- 需要保留旧版本历史。

这种情况必须使用 carry-over revalidation。

## Patch、Next、Backlog

| 分类 | 用途 | 处理 |
|---|---|---|
| Current Fix | 阻塞当前版本 UAT | 留在当前版本，立即修 |
| Patch | 发布后必须修的小问题 | 创建 `vX.Y.1` patch Issue |
| Next Version | 新 Feature 或非阻塞改进 | 创建或更新下一版本 Issue |
| Backlog | 只记录，不排期 | 放 Backlog，保留来源 |
| Decision | 范围或规则不清 | 创建 Decision，阻塞相关 Feature |

## Carry-over Revalidation

如果旧版本 Issue 原始范围已完成，但有下版本反馈：

1. 在旧 Issue 留双语 closeout comment。
2. 把旧 Issue 设为 `Done`。
3. 创建或更新下一版本 Issue。
4. 下一版本 Issue 必须写明 source issue、revalidation scenario、expected result、owner acceptance path。
5. 两边都留下链接或明确 ID。

不得直接把旧 Issue 从 `AI Project OS v0.1` 移到 `AI Project OS v0.2`。

## GitHub Tag 与 Linear Scope

GitHub tag/release 表示代码和发行事实，例如：

```text
v0.2.0
```

Linear Project 表示这个版本计划和验收范围。

发布前必须能对齐：

- Linear Project 中哪些 Issue Included。
- GitHub tag 包含哪些代码状态。
- release notes 列出哪些完成项和已知限制。
- UAT 记录确认哪个版本通过。

## 用户口令

规划下一版本：

```text
请读取 Linear、project-os/VERSION_PLANNING.md 和 project-os/RELEASE_POLICY.md。
把候选功能分成 Included、Excluded、Deferred、Decision 和 UAT focus。
先给版本范围建议，不要写代码。
```

拆分大功能：

```text
请把这个大功能拆成 parent/child issue。
每个 child issue 只能属于一个目标版本，并写清 Acceptance Criteria 和 Expected Result。
```

关闭旧版本并承接反馈：

```text
请关闭 <old version> 中已完成但有下版本反馈的 issue。
按 AI Project OS 创建 <next version> carry-over revalidation issue。
不要直接移动旧 issue。
```

硬规则：不要直接把旧 Issue 移入下一版本项目；旧版本历史用 carry-over revalidation 承接。
