# AI Project OS v0.5 - START_HERE

这是一套可以直接放进本地项目仓库的 AI 项目操作系统。

目标不是写漂亮文档，而是让本地 Codex 在进入一个旧项目或半成品项目时，按固定规则完成：

1. 先做自我检查，确认项目位置、依赖、账号和权限边界。
2. 如果是成熟或现状不明的项目，先执行 Phase 0.5 Whitebox Discovery。
3. 执行 Phase 0.75 Safety Classification，确认仓库、凭证、Agent 文档和项目记忆边界。
4. 审计项目现状，区分事实、说法、推断、矛盾和未知项。
5. 生成可人工确认的 Baseline。
6. 生成 Linear Import Plan。
7. 经人工确认后再写入 Linear。
8. 按版本开发。
9. 每个正式版本必须停下来做人工 UAT。

## 60 秒启动

1. 从 GitHub Release 下载最新 zip。
2. 解压后把完整的 `project-os/` 放进目标项目根目录。
3. 在该项目目录打开 Codex，把下面这段话发给它：

```text
请读取 project-os/START_HERE.md，并按 AI Project OS 工作。
先检查当前项目状态。
如果这是成熟或混乱项目，先执行 Phase 0.5 Whitebox Discovery 和 Phase 0.75 Safety Classification。
Linear 默认使用 English + Chinese。
只问真正阻塞的问题；其余按安全默认值继续。
先告诉我发现、风险和下一步，然后开始执行。
```

更短的安装说明、目录检查和常用启动口令见 `QUICKSTART.md`。

## 工具分工

- Linear：项目管理、Feature、任务、Bug、Decision、UAT 反馈。
- 本地 Codex：读取本地仓库、分析、开发、测试、生成 PR 准备材料。
- GitHub：代码、PR、测试结果、版本 tag、release 事实来源。
- 云端 Codex / scheduled automation：只允许 Linear intake/follow-up 的 dry-run/advisory 设计；不自动修改本地代码。
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

是否把 `project-os/` 提交到 GitHub，必须先按 `AGENT_DOC_POLICY.md` 和 `REPO_PUBLICATION_POLICY.md` 分类。单人项目可保留 local-only 文档；团队项目应共享稳定规则，但仍不得提交凭证、个人路径或原始聊天记录。

## 在新的本地 Codex 对话里启动 Phase 0/1

在目标项目仓库根目录打开本地 Codex，然后发送：

```text
请读取 project-os/START_HERE.md、project-os/SELF_CHECK.md、project-os/AGENTS.md、project-os/BOOTSTRAP.md、project-os/WHITEBOX_PROTOCOL.md、project-os/SECURITY_BOUNDARY.md 和 project-os/REPO_PUBLICATION_POLICY.md。

请按 AI Project OS v0.5 工作。

先执行 Phase 0 Self-Check。
如果是成熟、混乱或上下文不完整的项目，Phase 0 后先进入 Phase 0.5 Whitebox Discovery。
任何将进入 Git、团队共享或公开发布的项目，在 Phase 1 前执行 Phase 0.75 Safety Classification。

要求：
- 先确认当前目录、Git/GitHub、Linear、Linear Issue 描述语言（默认 English + Chinese）、依赖、环境变量和测试入口。
- 只读项目代码、文档、测试、配置和 Git 历史。
- 禁止修改产品代码。
- 禁止写入 Linear。
- 禁止创建 GitHub PR。
- 允许生成或更新 project-os/audit/*.md，包括 SELF_CHECK_REPORT.md。
- 允许在 Phase 0.5 生成或更新 project-os/discovery/*.md 和 SCAN_EVIDENCE.json。
- 允许在 Phase 0.75 生成或更新 project-os/safety/*.md 和经脱敏的 SAFETY_EVIDENCE.json。
- 先 dry-run 运行 `python3 project-os/tools/whitebox_scan.py --root . --summary`；确认范围后才使用 `--write`。
- 安全报告不得输出 matched value、source line、environment value 或 file content。
- 白盒化产物必须包含 PROJECT_MAP、DEPENDENCY_MAP、DOCUMENT_INVENTORY、SETTINGS_AND_DATA_REGISTER、LOGIC_BOUNDARY_AUDIT 和 WHITEBOX_IMPORT_REPORT。
- 每个重要结论必须写 State、Evidence、Confidence 和 Next Verification。
- 可记录设置名和路径，禁止记录 secret 值。
- 输出 PROJECT_BASELINE_DRAFT、PRODUCT_MAP、FEATURE_INVENTORY、GAPS_AND_DUPLICATES、RISKS_AND_DECISIONS、LINEAR_IMPORT_PLAN。
- 生成 Linear Import Plan 时，Issue 描述必须写清执行动作（Action Steps）和期待结果（Expected Result）。
- 任何业务不确定必须写入 Decision，不要自己猜。
- 完成后停下来，等待人工确认。
```

## 只做成熟项目白盒化

如果你想先看清项目，不进 Linear、不改代码，可以说：

```text
请读取 project-os/WHITEBOX_PROTOCOL.md 和 project-os/discovery/README.md。

对当前仓库执行 Phase 0.5 Whitebox Discovery。

要求：
- 默认只读，不改产品代码、不安装依赖、不连生产。
- 先运行 scanner dry-run 并汇报覆盖范围。
- 只在 project-os/discovery/ 写入白盒产物。
- 区分 Observed、Derived、Claimed、Inferred、Contradicted 和 Unknown。
- 重要结论必须有证据、置信度和下一步验证。
- 不记录任何 secret 值。
- 完成后停下，等我确认 Baseline。
```

## 只做安全检查

如果你只想知道“现在能不能提交、共享或公开”，可以说：

```text
请读取 project-os/SECURITY_BOUNDARY.md、project-os/REPO_PUBLICATION_POLICY.md、project-os/AGENT_DOC_POLICY.md 和 project-os/safety/README.md。

对当前仓库执行 Phase 0.75 Safety Classification。
先用 local/worktree profile 做只读 dry run，再告诉我目标发布 profile 需要补什么。
报告只能记录规则 ID、路径、分类、处置和修复建议；不得输出命中值、源代码行、环境变量值或文件正文。
不要自动删除文件、轮换凭证、改写 Git 历史或发布内容。
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

基础交接规则：

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
- 成熟或现状不明项目在 Baseline 前必须完成 Phase 0.5 Whitebox Discovery。
- 任何进入 Git、团队共享或公开发布的项目必须完成 Phase 0.75 Safety Classification。
- 白盒重要结论必须有 State、Evidence、Confidence 和 Next Verification。
- discovery 产物不得记录 secret 值。
- 私有仓库不是 secret store；安全证据不得输出命中值或源文件内容。
- automation 只允许 Linear intake/follow-up，不允许自动修改本地代码。

## 推荐阅读顺序

1. `QUICKSTART.md`：下载后如何在 60 秒内让 Codex 开始工作。
2. `SELF_CHECK.md`：第一次接管项目前怎么自检。
3. `OS_VERSION.md`：当前安装的 OS 版本。
4. `LOCAL_OVERRIDES.md`：本项目自己的规则，升级时不得覆盖。
5. `AGENTS.md`：所有 AI 和 Operator 必须遵守的总规则。
6. `WHITEBOX_PROTOCOL.md`：成熟项目证据、置信度、矛盾和停止规则。
7. `SECURITY_BOUNDARY.md`：四级资产分类和安全停止条件。
8. `REPO_PUBLICATION_POLICY.md`：进入 private/public GitHub 前的门禁。
9. `AGENT_DOC_POLICY.md`：AI 指令和团队规则何时共享。
10. `BOOTSTRAP.md`：Phase 0 到 Phase 6 的完整启动流程。
11. `LINEAR_POLICY.md`：Linear 怎么建、怎么写、什么时候必须停。
12. `REQUIREMENT_MANAGEMENT.md`：需求、评论和 issue 如何分类。
13. `VERSION_PLANNING.md`：版本、patch、分阶段交付和 carry-over。
14. `LINEAR_INTAKE.md`：宽泛 Linear 检查和 cron-ready scan 规则。
15. `AUTOMATION_POLICY.md`：自动跟进、dry-run、幂等和禁止动作。
16. `ROADMAP.md`：v0.3 到 v1.0 以及 1.0 后开源准备路线。
17. `RELEASE_POLICY.md`：版本怎么推进，什么时候必须 UAT。
18. `QUALITY_GATE.md`：什么叫 Ready、Done、Accepted。
19. `UPGRADE_POLICY.md`：以后怎么升级 AI Project OS。
20. `examples/FIRST_PROJECT.md`：从 Phase 0 到 Linear 和 UAT 的示例。
21. `examples/WHITEBOX_EXAMPLE.md`：带 Unknown、Contradicted、证据和 Linear 交接的完整白盒示例。
22. `examples/SAFETY_EXAMPLE.md`：四级分类、脱敏 finding 和发布判定示例。
