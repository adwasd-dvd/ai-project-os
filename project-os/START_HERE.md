# AI Project OS v0.3 - START_HERE

这是一套可以直接放进本地项目仓库的 AI 项目操作系统。

目标不是写漂亮文档，而是让本地 Codex 在进入一个旧项目或半成品项目时，按固定规则完成：

1. 先做自我检查，确认项目位置、依赖、账号和权限边界。
2. 再审计项目现状。
3. 生成可人工确认的 Baseline。
4. 生成 Linear Import Plan。
5. 经人工确认后再写入 Linear。
6. 按版本开发。
7. 每个正式版本必须停下来做人工 UAT。

## 工具分工

- Linear：项目管理、Feature、任务、Bug、Decision、UAT 反馈。
- 本地 Codex：读取本地仓库、分析、开发、测试、生成 PR 准备材料。
- GitHub：代码、PR、测试结果、版本 tag、release 事实来源。
- 云端 Codex / scheduled automation：v0.3 只允许 Linear intake/follow-up 的 dry-run/advisory 设计；不自动修改本地代码。
- Linear MCP：允许使用，但首次批量写入 Linear 必须人工确认。

## 怎么放到现有仓库

把整个 `project-os/` 目录放到目标项目仓库根目录：

```text
your-existing-repo/
├── project-os/
├── src/
├── tests/
├── package.json
└── ...
```

建议把 `project-os/` 一起提交到 GitHub，让所有 Operator、顾问和项目经理看到同一套规则。

## 在新的本地 Codex 对话里启动 Phase 0/1

在目标项目仓库根目录打开本地 Codex，然后发送：

```text
请读取 project-os/START_HERE.md、project-os/SELF_CHECK.md、project-os/AGENTS.md、project-os/BOOTSTRAP.md。

请按 AI Project OS v0.3 工作。

先执行 Phase 0 Self-Check。
如果 Phase 0 没有阻塞项，再进入 Phase 1 Audit。

要求：
- 先确认当前目录、Git/GitHub、Linear、Linear Issue 描述语言（默认 English + Chinese）、依赖、环境变量和测试入口。
- 只读项目代码、文档、测试、配置和 Git 历史。
- 禁止修改产品代码。
- 禁止写入 Linear。
- 禁止创建 GitHub PR。
- 允许生成或更新 project-os/audit/*.md，包括 SELF_CHECK_REPORT.md。
- 输出 PROJECT_BASELINE_DRAFT、PRODUCT_MAP、FEATURE_INVENTORY、GAPS_AND_DUPLICATES、RISKS_AND_DECISIONS、LINEAR_IMPORT_PLAN。
- 生成 Linear Import Plan 时，Issue 描述必须写清执行动作（Action Steps）和期待结果（Expected Result）。
- 任何业务不确定必须写入 Decision，不要自己猜。
- 完成后停下来，等待人工确认。
```

## 人工确认 Baseline 后推进 Phase 3

当你、项目经理、顾问确认 `project-os/audit/*.md` 基本靠谱以后，再发送：

```text
Baseline 已人工确认。

请进入 Phase 3 Linear Setup/Import。

要求：
- 先读取 project-os/LINEAR_POLICY.md 和 project-os/audit/LINEAR_IMPORT_PLAN.md。
- 如果可用，使用 Linear MCP 读取现有 Linear 项目和 Issue，检查疑似重复。
- 确认 Linear Issue 描述语言；默认使用 English + Chinese。
- 最终写入清单必须展示每类 Issue 的执行动作和期待结果。
- 先输出最终写入清单，不要立刻创建。
- 首次批量写入 Linear 必须等待我明确回复“批准写入 Linear”。
- 不要删除或覆盖 Linear 既有内容。
- 遇到疑似重复、字段冲突或业务不确定，停下来问我。
```

首次写入前，必须收到明确授权：

```text
批准写入 Linear。按 LINEAR_IMPORT_PLAN 分批创建，每批完成后汇报。
```

## 后续日常开发启动语

```text
请读取 project-os/AGENTS.md、project-os/WORKFLOW.md、project-os/RELEASE_POLICY.md、project-os/QUALITY_GATE.md、project-os/LINEAR_INTAKE.md。

我要处理 Feature ID: <填写 Feature ID>，目标版本: <填写版本号>。

请先从 Linear/GitHub/本地代码确认上下文，然后给出开发计划。
如果 Feature ID 或目标版本缺失，请不要开始正式开发。
```

## Linear 日常控制口令

只检查，不开工：

```text
请检查 Linear，然后按 AI Project OS 规则给我一个双语 run summary。
先不要写代码。
请说明 scan scope、scanned、created、updated、skipped、blockers 和 next action。
```

检查并继续下一个安全事项：

```text
请检查 Linear，然后处理下一个 Codex-ready issue。
Codex-ready 的基础定义是：Todo + unassigned + Feature ID + 目标版本 + 验收标准 + 无阻塞 Decision。
开始前先汇报 scan scope、Codex Queue、Human Queue、Review Queue 和将处理的 issue。
如果发现下版本需求、旧版本反馈或状态不一致，请按 LINEAR_INTAKE 分类，不要直接写代码。
```

把人类验收失败的 issue 交回 Codex：

```text
我已经在 Linear 留了验收失败反馈。
请读取 <Issue ID> 的最新评论。
如果它是 Todo + unassigned，请按 AI Project OS 继续修改。
如果缺 Feature ID、目标版本、验收标准或阻塞 Decision，请先停下来说明缺口。
```

v0.3 基础交接规则：

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

把模糊需求整理成 Linear 草案：

```text
请读取 project-os/REQUIREMENT_MANAGEMENT.md。
把下面这个想法分类并整理成 Linear issue 草案。
不要写代码，不要改变状态；如果缺 Feature ID、目标版本或验收标准，请列出缺口。
```

版本规划：

```text
请读取 project-os/VERSION_PLANNING.md 和 project-os/RELEASE_POLICY.md。
把候选功能分成当前版本、patch、下一版本、Backlog 或 Decision。
先给建议，不要直接移动旧 issue。
```

旧版本关账并承接反馈：

```text
请关闭 <old version> 中已完成但有下版本反馈的 issue，并按 AI Project OS 创建 <next version> carry-over revalidation issue。
不要直接移动旧 issue。
```

## 硬规则摘要

- 第一次接管项目，必须先做 Phase 0 Self-Check。
- 无 Feature ID，不正式开发。
- 无目标版本，不顺手做。
- AI 发现新需求，只记录，不自动实现。
- 业务不确定，必须提出 Decision。
- 一个 Codex 不能自我验收。
- 版本未人工 UAT，不得进入下一正式版本。
- Phase 1 的 Linear 状态变化必须由人确认。
- 首次批量写入 Linear 必须人工确认。
- 宽泛 Linear 检查必须执行 `LINEAR_INTAKE.md` 的扫描规则。
- Codex 写入 Linear 的用户可读评论、状态更新和 run summary 默认必须双语。
- Human/Codex 基础交接由 assignee 决定：有 assignee 等人类，无 assignee 等 Codex。
- `next:*` label 是高级可选项，不是基础流程必需项。
- 旧版本已完成 Issue 的下版本反馈必须 carry-over，不得直接移动旧 issue。
- v0.3 automation 只允许 Linear intake/follow-up，不允许自动修改本地代码。

## 推荐阅读顺序

1. `SELF_CHECK.md`：第一次接管项目前怎么自检。
2. `OS_VERSION.md`：当前安装的 OS 版本。
3. `LOCAL_OVERRIDES.md`：本项目自己的规则，升级时不得覆盖。
4. `AGENTS.md`：所有 AI 和 Operator 必须遵守的总规则。
5. `BOOTSTRAP.md`：Phase 0 到 Phase 6 的完整启动流程。
6. `LINEAR_POLICY.md`：Linear 怎么建、怎么写、什么时候必须停。
7. `REQUIREMENT_MANAGEMENT.md`：需求、评论和 issue 如何分类。
8. `VERSION_PLANNING.md`：版本、patch、分阶段交付和 carry-over。
9. `LINEAR_INTAKE.md`：宽泛 Linear 检查和 cron-ready scan 规则。
10. `AUTOMATION_POLICY.md`：自动跟进、dry-run、幂等和禁止动作。
11. `ROADMAP.md`：v0.3 到 v1.0 以及 1.0 后开源准备路线。
12. `RELEASE_POLICY.md`：版本怎么推进，什么时候必须 UAT。
13. `QUALITY_GATE.md`：什么叫 Ready、Done、Accepted。
14. `UPGRADE_POLICY.md`：以后怎么升级 AI Project OS。
15. `examples/FIRST_PROJECT.md`：从 Phase 0 到 Linear 和 UAT 的示例。
