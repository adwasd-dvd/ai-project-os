# RESCUE_PROTOCOL

This protocol is the v1.0 end-to-end takeover path for a mature, messy, black-box, gray-box, or abandoned software project.

本协议是 v1.0 针对成熟、混乱、黑盒、灰盒或近乎失控软件项目的端到端接管路径。

## Success Standard / 成功标准

```text
Drop AI Project OS into a messy mature project.
It whiteboxes the project, exposes risks and contradictions,
builds one Linear-managed recovery roadmap,
and guides humans and Codex through stable releases.
```

```text
把 AI Project OS 放进一个混乱成熟项目。
它能白盒化项目、暴露风险和矛盾、
建立一个由 Linear 管理的恢复路线图，
并带着人类和 Codex 稳定发版。
```

## One Guided Entry / 单一引导入口

Start read-only:

先只读检查：

```bash
python3 project-os/tools/rescue_project.py --root . inspect --summary
```

Codex then prepares `project-os/rescue/RESCUE_INPUT.json` from the example, using repository-relative evidence paths and no raw private values. Generate the local evidence package with:

Codex 随后根据模板准备 `project-os/rescue/RESCUE_INPUT.json`，只使用仓库相对证据路径，不写入原始私密值。生成本地证据包：

```bash
python3 project-os/tools/rescue_project.py --root . plan \
  --input project-os/rescue/RESCUE_INPUT.json \
  --profile private \
  --write --summary
```

Verify freshness after the repository changes:

仓库变化后检查证据是否仍然新鲜：

```bash
python3 project-os/tools/rescue_project.py --root . verify \
  --input project-os/rescue/RESCUE_INPUT.json \
  --profile private
```

## Outputs / 输出

The plan command writes only these files under the selected repository-internal rescue evidence directory:

plan 命令只在所选仓库内部救援证据目录写入以下文件：

- `RESCUE_EVIDENCE.json`: sanitized whitebox, safety, Git, finding, gate, and queue facts / 脱敏白盒、安全、Git、发现、门禁和队列事实。
- `RESCUE_DIAGNOSIS.md`: evidence-backed diagnosis / 基于证据的诊断。
- `RECOVERY_ROADMAP.md`: dependency-aware recovery phases and completion evidence / 考虑依赖关系的恢复阶段和完成证据。
- `LINEAR_RESCUE_IMPORT.json`: bilingual one-Project/one-Milestone dry-run proposal / 双语单 Project/单 Milestone dry-run 建议。
- `PM_NEXT_ACTION.md`: Human, Codex, Review, Backlog, blockers, and next action / 人类、Codex、Review、Backlog、阻塞和下一步。
- `RESCUE_RECEIPT.json`: deterministic artifact digests and no-write facts / 确定性产物摘要和零写入事实。

## Evidence Model / 证据模型

Every declared important finding must include:

每个重要声明发现必须包含：

```text
Finding ID
English + Chinese title
State: observed / derived / claimed / inferred / contradicted / unknown
Impact
Confidence
Repository-relative evidence paths
Action Steps in English + Chinese
Expected Result in English + Chinese
Next Verification in English + Chinese
Recommended Disposition
Owner
Blocking gates
Resolved state and resolution evidence when applicable
```

Automatic findings may be closed only through the input `resolutions` array with English + Chinese resolution text, a resolver, and repository-relative resolution evidence. A safety finding cannot be resolved while the current safety scan still emits it; fix or contain the underlying condition and rescan.

自动发现只能通过输入中的 `resolutions` 数组关闭，并提供中英文解决说明、解决人和仓库相对解决证据。当前安全扫描仍在输出某项时，不能用 resolution 关闭该安全发现；必须先修复或控制实际条件，再重新扫描。

The tool adds conservative automatic findings for missing target version, product scope, dependency evidence, lock evidence, tests, documentation, entry points, CI, repository safety, and overlapping Git work.

工具会对缺失目标版本、产品范围、依赖证据、锁定证据、测试、文档、入口、CI、仓库安全和重叠 Git 工作生成保守的自动发现。

Automatic findings are triage evidence, not business truth. Codex must add evidence-backed contradictions and logic/boundary findings discovered during interpretation.

自动发现是分类证据，不是业务真相。Codex 必须补充解释过程中发现的、具有证据支持的矛盾和逻辑/边界问题。

## Rescue Gates / 救援门禁

```text
SAFETY_BLOCKED
-> NEEDS_HUMAN_DECISION
-> READY_FOR_BASELINE_REVIEW
-> NEEDS_LINEAR_CONFIGURATION
-> READY_FOR_LINEAR_APPROVAL
-> READY_FOR_DEVELOPMENT
```

- `SAFETY_BLOCKED`: publication or repository boundary must be contained first / 必须先控制发布或仓库边界。
- `NEEDS_HUMAN_DECISION`: a blocking contradiction, unknown, scope, version, or business Decision needs a human / 阻塞矛盾、未知项、范围、版本或业务 Decision 需要人类。
- `READY_FOR_BASELINE_REVIEW`: evidence is reviewable but the Owner has not confirmed the baseline / 证据可审查，但 Owner 尚未确认 Baseline。
- `NEEDS_LINEAR_CONFIGURATION`: one Project and one target Milestone are not yet configured / 尚未配置唯一 Project 和目标 Milestone。
- `READY_FOR_LINEAR_APPROVAL`: the import proposal is ready but no Linear write is authorized / 导入建议已准备好，但没有 Linear 写入授权。
- `READY_FOR_DEVELOPMENT`: baseline and Linear gates are satisfied; only individually Ready work may start / Baseline 和 Linear 门禁已满足，只能开始逐项 Ready 工作。

## Proactive PM Rule / 积极型 PM 规则

The system must not merely list problems. It must name:

系统不能只列问题，还必须说明：

- the current gate;
- the Human Queue;
- the Codex Queue;
- the Review Queue;
- blockers and stale evidence;
- the highest-value safe next action;
- evidence required to complete the current phase.

- 当前门禁；
- 人类队列；
- Codex 队列；
- Review 队列；
- 阻塞和过期证据；
- 价值最高的安全下一步；
- 完成当前阶段所需的证据。

## Hard Safety Boundary / 硬安全边界

The rescue tool:

救援工具：

- excludes the installed `project-os/` package from product evidence by default;
- does not run product code or install dependencies;
- does not access production;
- emits no matched value, source line, environment value, file content, raw conversation, credential, or private payload;
- writes only generated rescue evidence when `plan --write` is explicit;
- never writes Linear, GitHub, tags, Releases, product code, dependencies, or runtime data;
- never resolves a business Decision, approves UAT, merges, releases, rotates credentials, rewrites Git history, or rolls production back.

- 默认从产品证据中排除已安装的 `project-os/`；
- 不运行产品代码，也不安装依赖；
- 不访问生产；
- 不输出命中值、源代码行、环境变量值、文件正文、原始对话、凭证或私密 payload；
- 只有明确使用 `plan --write` 时才写入生成的救援证据；
- 绝不写 Linear、GitHub、tag、Release、产品代码、依赖或运行时数据；
- 绝不替人解决业务 Decision、批准 UAT、合并、发布、轮换凭证、改写 Git 历史或回滚生产。

## Human Handoffs / 人工交接

Codex stops for the Owner when a blocking Decision, ambiguous scope, production access, secret remediation, baseline confirmation, first Linear write, UAT, release, destructive action, or rollback authority is required.

遇到阻塞 Decision、范围歧义、生产访问、凭证处置、Baseline 确认、首次 Linear 写入、UAT、发布、破坏性动作或回滚权限时，Codex 必须停下来交给 Owner。
