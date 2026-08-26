# QUICKSTART - 60-Second Start / 60 秒启动

Install AI Project OS and start a guided Codex takeover in about one minute.

大约一分钟安装 AI Project OS，并让 Codex 开始引导式接管项目。

## 1. Download / 下载

Download the latest `ai-project-os-v*.zip` from:

从这里下载最新的 `ai-project-os-v*.zip`：

<https://github.com/adwasd-dvd/ai-project-os/releases/latest>

## 2. Put It In Your Project / 放进项目

Extract the zip into the target project root. The result must look like:

把 zip 解压到目标项目根目录。结果应该是：

```text
your-project/
├── project-os/
│   ├── QUICKSTART.md
│   ├── START_HERE.md
│   └── ...
├── your existing code
└── ...
```

Do not create `your-project/project-os/project-os/`.

不要多套一层 `project-os/project-os/`。

## 3. Open Codex And Say This / 打开 Codex 并发送

Open the target project in Codex, start a conversation, and send:

在 Codex 中打开目标项目，新建对话，然后发送：

```text
请读取 project-os/START_HERE.md，并按 AI Project OS 工作。
先检查当前项目状态。
如果这是成熟或混乱项目，读取 project-os/RESCUE_PROTOCOL.md，先运行 rescue inspect，再生成本地 rescue plan。
Linear 默认使用 English + Chinese。
只问真正阻塞的问题；其余按安全默认值继续。
先告诉我发现、风险和下一步，然后开始执行。
```

That is the normal start. Codex should inspect the repository, identify missing context, explain risk, and continue through the OS workflow.

这就是标准启动方式。Codex 会检查仓库、识别缺失上下文、说明风险，并按 OS 流程继续。

## Short Prompts / 简短口令

New project / 新项目：

```text
读取 project-os/START_HERE.md。按 AI Project OS 初始化这个新项目，并使用安全默认值继续。
```

Messy existing project / 混乱旧项目：

```text
读取 project-os/START_HERE.md 和 project-os/RESCUE_PROTOCOL.md。运行 v1.0 rescue inspect；按安全默认值准备输入并生成本地 rescue plan。告诉我当前门禁、人类队列、Codex 队列、阻塞和下一步，然后继续所有不需要人工决定的安全工作。
```

Direct read-only command / 直接只读命令：

```bash
python3 project-os/tools/rescue_project.py --root . inspect --summary
```

The rescue workflow excludes the installed `project-os/` from product evidence and generates only local evidence until a separate human approval authorizes any external write.

救援流程会从产品证据中排除已安装的 `project-os/`，并且在另行人工批准外部写入前只生成本地证据。

Continue from Linear / 从 Linear 继续：

```text
读取 project-os/START_HERE.md 和 Linear。检查 Codex Queue，选择最高优先级且 Ready 的事项开始工作。
```

## Quick Validation / 快速验证

Optional but recommended after installation:

安装后建议运行：

```bash
python3 project-os/tools/validate_project_os.py --root . --strict
```

## Check For An OS Upgrade / 检查 OS 升级

Ask Codex:

```text
请读取 project-os/UPGRADE_POLICY.md。
先检查已安装版本和配置的上游版本，只生成只读报告。
如果有新版本，再生成 installed/base/target 三方升级计划。
不要 apply，等我审查计划。
```

The default upgrade flow is inspect -> plan -> human review. It never silently overwrites the installed `project-os/`.

默认升级流程是 inspect -> plan -> 人工 review，绝不会静默覆盖已安装的 `project-os/`。

For a mature or unclear project, Codex will guide the whitebox and safety scans. These scans are read-only unless an explicit write option is used.

成熟或不清晰项目由 Codex 引导白盒和安全扫描。除非明确使用 write 参数，否则扫描保持只读。

## Optional: Check Linear Automatically / 可选：自动检查 Linear

After the normal takeover is working, read `AUTOMATION_RUNBOOK.md`. Start with the included offline fixture, then configure a local live dry-run. Scheduled scans never modify local product code.

正常接管跑通后，读取 `AUTOMATION_RUNBOOK.md`。先运行内置离线 fixture，再配置本地 live dry-run。定时扫描绝不修改本地产品代码。

## Upgrade Rule / 升级规则

Install from a tagged GitHub Release. Before replacing an existing installation, read `UPGRADE_POLICY.md` and preserve `LOCAL_OVERRIDES.md`, audit history, and project-specific safety decisions.

使用带 tag 的 GitHub Release 安装。替换已有版本前，读取 `UPGRADE_POLICY.md`，并保留 `LOCAL_OVERRIDES.md`、audit 历史和项目自己的安全决定。
