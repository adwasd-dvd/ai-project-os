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
如果这是成熟或混乱项目，先执行 Phase 0.5 Whitebox Discovery 和 Phase 0.75 Safety Classification。
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
读取 project-os/START_HERE.md。先对白盒、安全边界和项目记忆做完整接管检查，再给我 baseline 草案。
```

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

For a mature or unclear project, Codex will guide the whitebox and safety scans. These scans are read-only unless an explicit write option is used.

成熟或不清晰项目由 Codex 引导白盒和安全扫描。除非明确使用 write 参数，否则扫描保持只读。

## Upgrade Rule / 升级规则

Install from a tagged GitHub Release. Before replacing an existing installation, read `UPGRADE_POLICY.md` and preserve `LOCAL_OVERRIDES.md`, audit history, and project-specific safety decisions.

使用带 tag 的 GitHub Release 安装。替换已有版本前，读取 `UPGRADE_POLICY.md`，并保留 `LOCAL_OVERRIDES.md`、audit 历史和项目自己的安全决定。
