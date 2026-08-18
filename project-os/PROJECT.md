# PROJECT

本文定义项目治理、角色、工具边界和事实来源。

## 项目目标

本项目使用 AI Project OS v0.1，把本地代码仓库整理成可以持续推进的工程系统。

系统目标：

- 让本地 Codex 先完成接管前自检。
- 让旧项目先被审计，再被接管。
- 让 Linear 成为项目管理控制台。
- 让 GitHub 成为代码和版本事实来源。
- 让本地 Codex 成为开发执行助手。
- 让每个正式版本经过人工 UAT。

## v0.1 工具边界

### Linear

Linear 负责：

- Feature 管理。
- Bug 管理。
- Decision 管理。
- 版本范围。
- 状态流转。
- UAT 反馈归档。

Linear 不负责：

- 保存代码事实。
- 替代 GitHub PR。
- 替代人工 UAT。

### 本地 Codex

本地 Codex 负责：

- 读取本地仓库。
- 读取项目规则。
- 审计代码和文档。
- 生成项目 Baseline。
- 按 Feature ID 开发。
- 运行本地测试。
- 准备 PR 内容。
- 在获得授权后通过 Linear MCP 写入 Linear。

本地 Codex 不负责：

- 自行批准版本。
- 自行验收版本。
- 自行决定业务优先级。
- 自行首次批量写入 Linear。

### GitHub

GitHub 负责：

- 代码事实。
- 分支。
- Pull Request。
- Review。
- CI 测试结果。
- tag。
- release notes。

### 云端 Codex

AI Project OS v0.1 暂不上云端 Codex。

如未来启用云端 Codex，必须先更新本文和 `AGENTS.md`，明确云端 Codex 的权限、触发方式、写入边界和验收责任。

## 事实来源

| 事实类型 | 事实来源 |
|---|---|
| Feature 状态 | Linear |
| 代码状态 | GitHub + 本地仓库 |
| 测试结果 | GitHub CI + 本地测试输出 |
| 版本发布 | GitHub tag/release |
| 当前版本范围 | Linear + RELEASE_POLICY |
| 业务决策 | Linear Decision Issue + RISKS_AND_DECISIONS |
| UAT 结论 | UAT_TEMPLATE 记录 + Linear 状态 |

## 项目角色

| 角色 | 责任 |
|---|---|
| Owner | 目标、优先级、最终 UAT 结论 |
| Project Manager | Linear、版本、范围、状态 |
| Operator A/B | 使用本地 Codex 开发已 Ready 的 Feature |
| Consultant | Review、高风险 Feature、架构建议 |
| Codex | 审计、执行、测试、整理、辅助写入 |

## 项目文件地图

| 文件 | 用途 |
|---|---|
| `START_HERE.md` | 用户启动说明 |
| `SELF_CHECK.md` | 第一次接管项目时的自我检查 |
| `BOOTSTRAP.md` | Phase 0 到 Phase 6 总流程 |
| `AGENTS.md` | 所有 AI 和人员的硬规则 |
| `WORKFLOW.md` | Idea 到 Release 的工作流 |
| `RELEASE_POLICY.md` | 版本推进规则 |
| `QUALITY_GATE.md` | Ready/Review/UAT/Release 门禁 |
| `LINEAR_POLICY.md` | Linear 结构和写入规则 |
| `GITHUB_POLICY.md` | GitHub 分支、PR、tag 规则 |
| `FEATURE_TEMPLATE.md` | Feature 标准模板 |
| `UAT_TEMPLATE.md` | 人工验收模板 |
| `DAILY_MEETING.md` | 每日同步模板 |
| `audit/*.md` | Phase 1 产物和 Phase 3 导入计划 |

## 项目节奏

推荐默认节奏：

- 每日一次 15 分钟同步。
- 每个 Feature 独立进入开发。
- 每个 PR 对应一个 Feature 或一个清楚的 Bug。
- 每个正式版本必须 UAT。
- UAT 未通过，只能修当前版本阻塞项或规划 patch，不得直接进入下一正式版本。

## Scope 管理

任何 Scope 变化必须进入 Linear。

Scope 变化包括：

- 新增 Feature。
- 改变验收标准。
- 改变目标版本。
- 把 Bug 升级为 Feature。
- 把 Backlog 提前到当前版本。
- 合并或拆分 Feature。

Codex 发现 Scope 变化时，只能记录和建议，不得自动执行。
