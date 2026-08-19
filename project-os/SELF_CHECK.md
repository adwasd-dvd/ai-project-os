# SELF_CHECK

本文定义 AI Project OS v0.3 的 Phase 0 Self-Check。

Phase 0 是本地 Codex 第一次接管项目时必须执行的初始化自检。

目标：先确认 Codex 是否站在正确的项目里、是否能读取必要上下文、Linear 中用什么语言描述项目事项、哪些依赖或账号需要用户配合、是否存在 scheduled scan 需求，再进入 Phase 1 Audit。

## 什么时候执行

用户出现以下表达时，Codex 必须先执行本文件：

```text
按照这个懒人包工作。
按 project-os 工作。
初始化这个项目。
接管这个项目。
开始 Phase 1。
```

即使用户直接说“开始审计”，如果项目是第一次接入 AI Project OS，也必须先做 Phase 0。

## Phase 0 总原则

- 能自己检查的，不问用户。
- 必须用户授权、登录、选择或确认的，再问用户。
- 一次只问少量阻塞问题。
- 不为了完美配置阻塞整个 Phase 1。
- 如果项目会进入 Linear，必须询问或确认 Linear Issue 描述语言。
- Linear Issue 描述语言默认建议为 `English + Chinese`，除非用户明确指定其他语言。
- Codex-authored Linear comments、status updates 和 run summaries 默认也应遵守同一双语用户可读规则。
- Phase 0 不修改产品代码。
- Phase 0 不写入 Linear。
- Phase 0 不创建 GitHub PR。
- Phase 0 可以生成或更新 `project-os/audit/SELF_CHECK_REPORT.md`。

## Codex 第一响应

当用户说“按照这个懒人包工作”时，Codex 应先说明：

```text
我会先做 Phase 0 Self-Check：确认当前仓库、project-os 文件、Git/GitHub、Linear、Linear Issue 描述语言（默认建议 English + Chinese）、依赖、环境变量、测试入口和是否需要 scheduled Linear scan。不会修改产品代码，也不会写入 Linear。完成后我会告诉你缺什么，再进入 Phase 1 Audit。
```

然后直接开始检查。

## Self-Check Checklist

### 1. Project Location

Codex 必须确认：

- 当前目录是否是项目根目录。
- 是否存在 `.git`。
- 是否存在 `project-os/`。
- 是否存在关键文件：
  - `project-os/START_HERE.md`
  - `project-os/SELF_CHECK.md`
  - `project-os/AGENTS.md`
  - `project-os/BOOTSTRAP.md`
  - `project-os/audit/`

如果 `project-os/audit/` 不存在，Codex 可以创建。

如果 `project-os/` 不在项目根目录，Codex 必须提示用户确认正确位置。

### 2. Repository Facts

Codex 必须收集：

- 仓库名称。
- 当前分支。
- 当前 commit。
- 是否有未提交改动。
- Git remote。
- GitHub repo URL，如果存在。
- 最近 tag。
- 最近提交摘要。

如果不是 Git 仓库，Codex 可以继续 Phase 1 读取文件，但必须标记风险。

### 3. Project Shape

Codex 必须识别：

- 主要语言。
- 框架。
- 包管理器。
- 应用入口。
- 测试入口。
- 构建入口。
- lint 或类型检查入口。
- 数据库或迁移目录。
- 文档目录。
- CI/CD 配置。

这一步只做识别，不做深度审计。

### 4. Local Dependency Readiness

Codex 必须判断：

- 依赖是否已安装。
- 是否存在 lockfile。
- 是否能安全运行安装命令。
- 是否存在 `.env.example`、`.env.template` 或配置说明。
- 是否缺少本地运行所需环境变量。

Codex 不应擅自安装依赖，除非用户已经授权，或用户明确要求它继续完成本地准备。

如果安装依赖是 Phase 1 必需项，Codex 必须先说明原因并请求确认。

### 5. GitHub Readiness

Codex 必须判断：

- 是否有 GitHub remote。
- 是否能读取本地 Git 历史。
- 是否有创建 PR 所需连接或登录状态。

Phase 1 不要求 GitHub 登录。

GitHub 写操作或 PR 操作只在后续阶段需要。缺少 GitHub 登录不应阻塞 Phase 1，但必须记录。

### 6. Linear Readiness

Codex 必须判断：

- 是否能使用 Linear MCP 或等价连接。
- 是否知道 Linear workspace。
- 是否知道 Linear team。
- 是否已有相关 Linear project。
- 是否已有 Issue 命名或状态规范。
- Linear Issue 描述语言应该是什么。
- 如果用户没有指定，是否采用默认 `English + Chinese`。
- Linear Issue 是否需要写清执行动作和期待结果。
- Codex-authored Linear comments、status updates 和 run summaries 是否采用同样的双语规则。
- 是否需要 future scheduled/cron Linear intake scan；如果需要，默认 dry-run/read-only。

Phase 1 不要求 Linear 登录。

Linear 连接缺失不应阻塞 Phase 1，但会阻塞 Phase 3 写入。

首次批量写入 Linear 前仍必须人工确认。

### 7. Permission Boundaries

Codex 必须向用户明确当前阶段权限：

```text
Phase 0/1 我只会读取项目并写 project-os/audit 文档。
我不会改产品代码。
我不会写入 Linear。
我不会创建 GitHub PR。
```

如果需要超出这些权限，必须单独请求用户确认。

### 8. Human Questions

Codex 只能问真正阻塞的问题。

推荐一次最多问 1 到 3 个问题。

优先级：

1. 当前目录是否正确。
2. Linear workspace/team 应该选哪个。
3. Linear Issue 描述语言是否采用默认 `English + Chinese`。
4. 是否未来需要 scheduled/cron Linear intake scan；默认 `dry-run/read-only`。
5. 是否允许安装依赖或运行测试。
6. 缺失的环境变量从哪里获得。
7. 谁是 UAT Owner。

不要一开始就问长问卷。

## Self-Assigned Goal

Phase 0 开始时，Codex 应给出当前目标：

```text
Current Goal: 完成 AI Project OS Phase 0 Self-Check，并判断是否可以进入 Phase 1 Audit。
```

如果运行环境支持显式目标跟踪，并且用户要求使用目标功能，Codex 可以创建对应目标。

否则，只需在对话中清楚声明当前目标。

## Dependency Handling

当缺少依赖、账号或链接时，Codex 应这样处理：

| 缺失项 | 是否阻塞 Phase 1 | Codex 行为 |
|---|---|---|
| Linear 登录 | No | 记录，Phase 3 前再处理 |
| GitHub 登录 | No | 记录，PR 前再处理 |
| scheduled scan 需求 | No | 记录，v0.3 默认 dry-run/read-only |
| package install | Maybe | 说明用途，请求确认 |
| `.env` | Maybe | 先静态审计，运行时再询问 |
| 数据库连接 | Maybe | 不连接生产库，先记录 |
| UAT Owner | No | Phase 4 前必须确认 |
| 项目根目录不确定 | Yes | 立即询问 |

## Phase 0 Output

Codex 必须生成或更新：

```text
project-os/audit/SELF_CHECK_REPORT.md
```

报告必须包含：

- 当前目录确认。
- Git/GitHub 状态。
- Linear 状态。
- Linear Issue 描述语言偏好。
- Linear comments/status/run summaries 语言偏好。
- scheduled scan 偏好和安全默认值。
- 依赖状态。
- 环境变量状态。
- 可运行命令。
- 阻塞项。
- 非阻塞缺口。
- 是否建议进入 Phase 1。

## Phase 0 Completion

完成后，Codex 必须给出结论：

```text
Phase 0 Self-Check complete.

Can start Phase 1 Audit: Yes / No

Blocking items:
-

Non-blocking missing items:
-

Recommended next step:
-
```

如果可以进入 Phase 1，Codex 应询问用户：

```text
是否现在开始 Phase 1 Audit？我会只读项目并生成 audit 文档，不改产品代码、不写 Linear。
```

如果用户一开始已经明确要求“初始化并开始 Phase 1”，且 Phase 0 没有阻塞项，Codex 可以直接进入 Phase 1，但必须先在回复中说明。
