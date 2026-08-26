# Rescue Example / 救援示例

This example shows how v1.0 turns a messy mature repository into a controlled recovery plan without modifying product code or external systems.

本示例展示 v1.0 如何在不修改产品代码或外部系统的前提下，把混乱成熟仓库变成受控恢复计划。

## Starting Condition / 初始状态

```text
README says one startup command.
Implemented entry point suggests a different command.
Dependency manifest exists but lock evidence is missing.
No automated test path is visible.
A credential-like local file exists.
No target version or Linear Milestone is confirmed.
```

```text
README 声称一条启动命令。
实际入口暗示另一条命令。
存在依赖清单，但缺少锁定证据。
看不到自动化测试路径。
存在疑似凭证的本地文件。
尚未确认目标版本或 Linear Milestone。
```

## Inspect / 检查

```bash
python3 project-os/tools/rescue_project.py --root . inspect --summary
```

Expected first conclusion / 预期首次结论：

```text
Gate: SAFETY_BLOCKED or NEEDS_HUMAN_DECISION
Evidence written: No
Product or external writes: No
```

## Declared Contradiction / 声明矛盾

Codex adds the following shape to `RESCUE_INPUT.json` after locating both evidence paths. No file contents are copied.

Codex 找到两条证据路径后，把以下结构加入 `RESCUE_INPUT.json`，不复制文件正文。

```json
{
  "finding_id": "DOC-RUN-001",
  "title_en": "Documented and implemented startup paths disagree",
  "title_zh": "文档与实现的启动路径冲突",
  "state": "contradicted",
  "impact": "high",
  "confidence": "high",
  "evidence": ["README.md", "src/main.py"],
  "action_steps_en": "Reproduce both startup paths in an isolated environment.",
  "action_steps_zh": "在隔离环境复现两条启动路径。",
  "expected_result_en": "One canonical startup path is proven and documented.",
  "expected_result_zh": "证明并记录一条权威启动路径。",
  "next_verification_en": "Run both commands and record exit status.",
  "next_verification_zh": "运行两条命令并记录退出状态。",
  "recommended_disposition": "decision",
  "owner": "Owner",
  "blocks": ["baseline", "development"],
  "resolved": false
}
```

## Plan / 计划

```bash
python3 project-os/tools/rescue_project.py --root . plan \
  --input project-os/rescue/RESCUE_INPUT.json \
  --profile private --write --summary
```

The generated package makes the handoff explicit:

生成包会明确交接：

```text
RESCUE_DIAGNOSIS.md: contradiction, impact, confidence, evidence, next verification
RECOVERY_ROADMAP.md: safety -> Decisions -> stabilization -> baseline -> Linear -> release
LINEAR_RESCUE_IMPORT.json: dry-run, one Project, one Milestone, writes 0
PM_NEXT_ACTION.md: Human Queue contains DOC-RUN-001
RESCUE_RECEIPT.json: deterministic artifact digests
```

## Human Resolution / 人工解决

The Owner chooses or confirms the canonical startup rule. Codex records `resolved: true` plus repository-relative resolution evidence, regenerates the plan, and asks for Baseline confirmation only after other blocking findings are closed or routed.

Owner 选择或确认权威启动规则。Codex 写入 `resolved: true` 和仓库相对 resolution evidence，重新生成计划；只有其他阻塞发现都关闭或完成路由后，才请求 Baseline 确认。

## Linear Boundary / Linear 边界

Even if `write_approved` appears in the input, `rescue_project.py` performs zero Linear writes. Actual Linear import remains a separate operation under `LINEAR_POLICY.md`, using one Project, one Milestone, duplicate checks, and explicit authorization.

即使输入中出现 `write_approved`，`rescue_project.py` 仍执行零次 Linear 写入。真实 Linear 导入仍是 `LINEAR_POLICY.md` 下的独立操作，使用一个 Project、一个 Milestone、重复检查和明确授权。
