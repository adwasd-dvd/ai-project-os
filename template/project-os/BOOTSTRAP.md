# BOOTSTRAP

本文定义 AI Project OS v0.4 的启动流程。

任何本地 Codex 第一次进入项目时，必须先执行本文件，不允许直接开发。

## 总目标

把一个现有项目整理成可管理、可开发、可验收、可发布的状态。

启动流程分为七个主要阶段，并在 Self-Check 与 Audit 之间加入 Phase 0.5：

0. Phase 0 Self-Check：接管前自我检查。
0.5. Phase 0.5 Whitebox Discovery：对成熟/不明项目收集证据并建立白盒地图。
1. Phase 1 Audit：只读审计。
2. Phase 2 Baseline Confirmation：人工确认现状。
3. Phase 3 Linear Setup/Import：确认后导入 Linear。
4. Phase 4 Release Planning：确定版本范围。
5. Phase 5 Development：按 Feature 开发。
6. Phase 6 Human Acceptance：人工 UAT 验收。

## Phase 0 Self-Check

### 目标

确认 Codex 是否处在正确的项目里，是否能读取必要上下文，Linear Issue 用什么语言描述，哪些依赖、账号、链接或权限需要用户配合。

### 必须先读取

- `START_HERE.md`
- `SELF_CHECK.md`
- `AGENTS.md`
- `BOOTSTRAP.md`

### 允许做

- 检查当前目录和 Git 状态。
- 检查 `project-os/` 是否完整。
- 检查 GitHub remote 是否存在。
- 检查 Linear MCP 或连接是否可用。
- 询问或确认 Linear Issue 描述语言，默认建议 `English + Chinese`。
- 识别包管理器、测试命令、构建命令、环境变量模板。
- 创建或更新 `project-os/audit/SELF_CHECK_REPORT.md`。

### 禁止做

- 禁止修改产品代码。
- 禁止写入 Linear。
- 禁止创建 GitHub PR。
- 禁止擅自安装依赖。
- 禁止连接生产数据库。

### Phase 0 完成条件

Codex 必须输出：

- 是否确认当前目录是项目根目录。
- 是否需要 Phase 0.5，以及是否可以进入 Phase 0.5/1。
- 阻塞项。
- 非阻塞缺口。
- Linear Issue 描述语言偏好。
- 接下来建议用户确认什么。

如无阻塞项，成熟/不明项目进入 Phase 0.5；有证据标记为 `Not Applicable` 的全新项目可进入 Phase 1。

## Phase 0.5 Whitebox Discovery

### 何时必须执行

以下任一情况必须执行 Phase 0.5：

- 仓库已经存在一段时间。
- 原团队、原对话或设计上下文不完整。
- 代码、文档、配置或 Linear 之间可能不一致。
- 项目被用户描述为黑盒、灰盒、混乱、糟或无法管理。
- Codex 无法用高置信度说明主要组件、依赖、数据或边界。

全新空项目可将 Phase 0.5 标记为 `Not Applicable`，但必须写明证据，不得默认跳过。

### 必须先读取

- `WHITEBOX_PROTOCOL.md`
- `discovery/README.md`
- `SELF_CHECK_REPORT.md` 中的范围与权限结论

### 机械证据扫描

先 dry run：

```bash
python3 project-os/tools/whitebox_scan.py --root . --summary
```

检查输出范围后，才写入：

```bash
python3 project-os/tools/whitebox_scan.py --root . --write
```

默认只能写入：

```text
project-os/discovery/SCAN_EVIDENCE.json
```

### 必须输出

- `discovery/PROJECT_MAP.md`
- `discovery/DEPENDENCY_MAP.md`
- `discovery/DOCUMENT_INVENTORY.md`
- `discovery/SETTINGS_AND_DATA_REGISTER.md`
- `discovery/LOGIC_BOUNDARY_AUDIT.md`
- `discovery/WHITEBOX_IMPORT_REPORT.md`

每个重要结论必须有：

```text
State
Evidence
Confidence
Unknowns / Contradictions
Next Verification
```

### 禁止做

- 禁止修改产品代码、依赖或运行时数据。
- 禁止记录 secret 值；只可记录设置名和路径。
- 禁止执行未知脚本或连接生产系统。
- 禁止把 Claimed 或 Inferred 写成 Observed。
- 禁止写入 Linear 或自动开始修复发现。

### Phase 0.5 完成条件

- 六份报告均已填写，不是空表。
- 覆盖范围和未读区域已记录。
- 高影响、低置信度发现已转入验证队列或 Decision。
- 重要矛盾和未知项保持可见。
- discovery 产物不含 secret 值。
- Codex 可以说明哪些是事实、说法、推断或未知。

## Phase 1 Audit

### 目标

让 Codex 看懂项目现状，但不改变项目事实。

### 允许做

- 读取代码、文档、配置、测试、脚本、CI、部署配置。
- 读取 Git 历史、分支、tag、最近提交信息。
- 读取已有 TODO、注释、Issue 引用、PR 引用。
- 生成或更新 `project-os/audit/*.md`。
- 引用并对账 `project-os/discovery/*.md` 和 `SCAN_EVIDENCE.json`。
- 标注不确定、冲突、缺口、重复项和风险。

### 禁止做

- 禁止修改产品代码。
- 禁止修改测试代码。
- 禁止修改依赖锁文件。
- 禁止创建、删除、修改 Linear 内容。
- 禁止创建 GitHub PR。
- 禁止自行决定业务规则。
- 禁止把猜测当事实。

### 必须输出

- `audit/PROJECT_BASELINE_DRAFT.md`
- `audit/PRODUCT_MAP.md`
- `audit/FEATURE_INVENTORY.md`
- `audit/GAPS_AND_DUPLICATES.md`
- `audit/RISKS_AND_DECISIONS.md`
- `audit/LINEAR_IMPORT_PLAN.md`
- 已完成的 Phase 0.5 discovery 报告，或有证据的 `Not Applicable` 结论

### Phase 1 完成条件

Codex 必须在最终回复中说明：

- 已读取哪些项目区域。
- 哪些区域没有读取到，原因是什么。
- 哪些判断证据充分。
- 哪些判断需要人工确认。
- 是否存在阻塞 Phase 2 的问题。

完成后必须停止，等待人工确认。

## Phase 2 Baseline Confirmation

### 目标

由人确认 AI 对项目现状的理解是否可作为管理和开发基线。

### 人工确认者

至少需要以下角色中的一人确认：

- 项目 Owner
- 项目经理
- 业务负责人
- 顾问或技术负责人

### 人工需要检查

- 模块划分是否符合业务理解。
- Feature 列表是否遗漏关键能力。
- Feature 当前状态是否判断合理。
- 重复项是否真的重复。
- 建议目标版本是否符合业务优先级。
- Decision 是否覆盖所有不确定点。
- Whitebox 覆盖范围是否诚实、主要组件和边界是否符合理解。
- 高影响、低置信度发现和重要矛盾是否已解决或正确路由。

### Codex 允许做

- 根据人工反馈修订 `audit/*.md`。
- 对争议项增加证据和置信度。
- 把不确定项移动到 Decision。

### Codex 禁止做

- 禁止因为“看起来合理”就进入 Linear 写入。
- 禁止把未确认的 Baseline 当作项目事实。

### Phase 2 完成条件

人工明确回复类似：

```text
Baseline 已确认，可以进入 Phase 3。
```

没有这句话或等价明确授权，不得进入 Phase 3。

## Phase 3 Linear Setup/Import

### 目标

把确认后的项目结构导入 Linear，让 Linear 成为项目管理控制台。

### 前置条件

- Phase 2 已人工确认。
- `audit/LINEAR_IMPORT_PLAN.md` 已更新到最终版本。
- 如适用，`discovery/WHITEBOX_IMPORT_REPORT.md` 已被人工确认，其发现已对账到 Import Plan。
- Linear workspace、team、status、label、project 规则已明确。
- Linear Issue 描述语言已确认，默认建议为 `English + Chinese`。
- Linear Issue 描述模板已写清执行动作和期待结果。

### Linear MCP 使用规则

如果 Linear MCP 可用，Codex 可以：

- 读取现有 Linear team、project、issue、label。
- 检查疑似重复。
- 根据已确认的 Import Plan 创建内容。

首次批量创建前，必须先输出最终写入清单，并等待明确授权：

```text
批准写入 Linear。
```

### 禁止做

- 禁止首次未确认批量写入。
- 禁止删除 Linear 既有内容。
- 禁止覆盖现有 Issue 描述、状态、负责人或版本。
- 禁止自动关闭疑似重复 Issue。
- 禁止把 Phase 1 的状态判断直接写成 Linear 最终状态，除非人确认。

### 批量写入方式

建议每批不超过 20 个 Issue。

每批完成后 Codex 必须汇报：

- 创建了哪些 Project / Issue。
- 哪些项目跳过了，原因是什么。
- 哪些项目疑似重复，需要人工确认。
- 下一批准备写什么。

### Phase 3 完成条件

- Linear 中已出现确认后的项目结构。
- `audit/LINEAR_IMPORT_PLAN.md` 已记录实际写入结果。
- 所有疑似重复和冲突项都有处理状态。

## Phase 4 Release Planning

### 目标

确定当前正式版本要做什么，不做什么。

### 必须确定

- 当前目标版本，例如 `v0.1.0`。
- 版本目标。
- Included Feature。
- Excluded Feature。
- 风险和 Decision。
- UAT 验收人。
- 预计验收方式。

### 硬规则

- 无目标版本，不允许正式开发。
- 无 Feature ID，不允许正式开发。
- 新需求只记录，不自动加入当前版本。
- Scope 变化必须写入 Linear，并由人确认。

### Phase 4 完成条件

Linear 或 `project-os` 中存在明确的版本范围，且人工确认。

### v0.3 版本规划补充

Phase 4 必须使用 `VERSION_PLANNING.md` 判断：

- 哪些 Issue 属于当前版本。
- 哪些属于 patch。
- 哪些属于下一正式版本。
- 哪些只是 Backlog。
- 哪些需要 Decision。
- 旧版本反馈是否需要 carry-over revalidation。

一个可交付 Issue 只能属于一个目标版本。旧版本已完成 Issue 的下版本反馈不得直接移动旧 issue，必须创建或更新下一版本承接 Issue。

## Phase 5 Development

### 目标

本地 Codex 按 Feature ID 和目标版本执行开发。

### 开发前必须检查

- Feature ID 是否存在。
- 目标版本是否存在。
- Feature 是否 Ready。
- 是否存在未解决 Decision。
- 是否有验收标准。
- 是否有测试要求。
- 是否与当前分支和 PR 对应。

### Codex 工作步骤

1. 读取 Feature、Linear、GitHub、代码上下文。
2. 给出实现计划。
3. 修改代码。
4. 运行相关测试。
5. 更新必要文档。
6. 汇报变更、测试结果、风险。
7. 准备 PR 描述或提交建议。

如果用户用宽泛口令要求 Codex 检查 Linear 并继续工作，Codex 必须先执行 `LINEAR_INTAKE.md` 的 scan contract，并汇报 scan scope、scanned、created、updated、skipped、blockers 和 next action。

### 禁止做

- 禁止顺手做无关 Feature。
- 禁止把验收反馈当新开发直接做掉。
- 禁止跳过测试说明。
- 禁止自我声明 UAT 通过。
- 禁止在 v0.3 因为 scheduled scan 自动修改本地代码。

## Phase 6 Human Acceptance

### 目标

让每个正式版本在进入下一版本前接受人工 UAT。

### 必须做

- 使用 `UAT_TEMPLATE.md`。
- 人工执行关键流程。
- 把问题分类为：
  - 当前版本立即修
  - Patch 版本
  - 下一版本
  - Backlog
  - Decision
- 更新 Linear 状态。
- 确认是否允许进入下一正式版本。
- 对已完成但有下版本反馈的旧 Issue 执行 carry-over revalidation。

### 硬规则

- 一个 Codex 不能自我验收。
- 版本未人工 UAT，不得进入下一正式版本。
- UAT 中发现的新需求不能自动进入当前版本。
- 旧版本 Issue 原范围完成时，应关闭旧 Issue 并创建下一版本承接 Issue，不要直接移动旧 issue。

### Phase 6 完成条件

人工明确给出版本结论：

```text
UAT 通过，允许发布 <version>。
```

或：

```text
UAT 未通过，必须先处理以下问题。
```
