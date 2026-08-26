# DOGFOOD REPORT v1.0.0

This report records v1.0 mature-project rescue certification against both a representative messy fixture and the AI Project OS source repository.

本报告记录 v1.0 成熟项目救援在代表性混乱 fixture 和 AI Project OS 源码仓库上的认证结果。

## Scope / 范围

```text
Features: AIPOS-052 through AIPOS-058
Branch: codex/v1.0-internal-stable
Tool: project-os/tools/rescue_project.py
Input: project-os/audit/RESCUE_INPUT_v1.0.0.json
Real-repository output: ignored project-os/runtime/v100_rescue_dogfood_run3 and run4
Product writes performed: 0
External writes performed: 0
Human UAT claimed: No
```

## Representative Messy Fixture / 代表性混乱 Fixture

Focused certification test:

`test_representative_messy_project_certification_is_deterministic`

The fixture combines these conditions in one repository:

该 fixture 在同一个仓库中组合：

- documented and implemented startup paths contradict each other / 文档与实现的启动路径冲突；
- dependency manifest exists but lock evidence is missing / 存在依赖清单但缺少 lock 证据；
- automated tests are missing / 缺少自动化测试；
- CI is missing / 缺少 CI；
- a credential-like local file is present / 存在疑似凭证的本地文件；
- Git contains uncommitted product changes / Git 中存在未提交产品改动；
- the installed `project-os/` directory must not count as product evidence / 已安装 `project-os/` 不得计入产品证据。

Result:

```text
Gate: SAFETY_BLOCKED
Contradiction routed: DOC-RUN-001 -> Human Decision
Dependency finding: DEP-LOCK-001
Test finding: TEST-001
CI finding: CI-001
Safety finding: present and blocking
Linear proposal: dry-run, one Project, one Milestone, writes 0
Two complete runs: byte-identical
Credential-like value in any artifact: No
```

## Safety Resolution Boundary / 安全解决边界

The focused suite also proves:

Focused suite 还证明：

- a normal automatic finding can be closed with bilingual resolution text, resolver identity, and repository-relative evidence;
- a current safety finding cannot be signed away while the scanner still emits it;
- forbidden raw/sensitive input fields and output traversal fail closed.

- 普通自动发现可通过双语解决说明、解决人和仓库相对证据关闭；
- 当前安全扫描仍在输出的发现不能靠文字签掉；
- 禁止的原始/敏感输入字段和输出路径逃逸会 fail closed。

## Real Repository Dogfood / 真实仓库 Dogfood

The AI Project OS source repository was inspected with `project-os/` excluded from product evidence. In this source layout, `template/project-os/` remains product source and is included.

AI Project OS 源码仓库在产品证据中排除了 `project-os/`。在该源码布局中，`template/project-os/` 仍是产品源码，因此保留在范围内。

```text
Product files: 100
Product bytes: 719259
Excluded prefixes: project-os
Safety profile: private
Safety gate: Go
Safety Block: 0
Safety Review: 0
Total findings: 4
Resolved findings: DEP-001, ENTRY-001
Open findings: GIT-001, CI-001
Blocking findings: 0
Gate: READY_FOR_DEVELOPMENT
Human Queue: GIT-001
Backlog: CI-001
Linear mode: dry-run
Target Project: AI Project OS
Target Milestone: v1.0.0
Linear writes performed: 0
Product writes performed: 0
External writes performed: 0
```

`DEP-001` was resolved because AI Project OS tools intentionally use the Python standard library. `ENTRY-001` was resolved because the product is entered through `START_HERE.md` and explicit tools rather than one runtime server. Both resolutions cite repository paths.

`DEP-001` 已解决，因为 AI Project OS 工具有意只使用 Python 标准库。`ENTRY-001` 已解决，因为产品通过 `START_HERE.md` 和显式工具进入，而不是一个运行服务器。两项解决均引用仓库路径。

`GIT-001` correctly remains visible because development is active on the branch. `CI-001` is routed to Backlog and does not silently enter v1.0 scope.

`GIT-001` 正确保留可见，因为该分支正在开发。`CI-001` 被路由到 Backlog，不会静默进入 v1.0 范围。

## Determinism And Freshness / 确定性与新鲜度

Two independent output directories were generated from the same source/input. Recursive comparison found no difference, and `verify` returned PASS.

相同源码和输入在两个独立目录生成，递归比较没有差异，`verify` 返回 PASS。

| Artifact | SHA-256 |
|---|---|
| `RESCUE_DIAGNOSIS.md` | `021fec1079dd9b32b7700df11b521faae147f8dfa8f194f54c94d06d9258cc73` |
| `LINEAR_RESCUE_IMPORT.json` | `35d8f16e558b920f97f6a8faee5d332edeb3536872a897b54bf02190e64351a9` |
| `RESCUE_EVIDENCE.json` | `7683c7e3466d236c3d5714851b402619ac8bb6bc49daaec3c957669559493c46` |
| `RESCUE_RECEIPT.json` | `d7fc900ca220a473518c0572299d3df51fc59d0ce25d6b56fa6193aab9818f38` |
| `PM_NEXT_ACTION.md` | `df3e69ce9c13aa70f4608b853d19d01d831bed74605d063a5fc90b322f863f98` |
| `RECOVERY_ROADMAP.md` | `ee51d3ae437b304cef757699ddb00f572f6807d417acc543b96f33cc9434b92e` |

## Current Conclusion / 当前结论

The v1.0 rescue engine has automated evidence for orchestration, sanitization, contradiction/safety routing, resolutions, recovery planning, one-Project Linear drafts, proactive PM queues, deterministic reruns, and real-repository operation. Package and extracted-package certification plus consolidated Owner UAT remain pending under AIPOS-059.

v1.0 救援引擎已经拥有编排、脱敏、矛盾/安全路由、解决记录、恢复计划、单 Project Linear 草案、积极型 PM 队列、确定性重跑和真实仓库运行的自动证据。AIPOS-059 的安装包/解压包认证和统一 Owner UAT 仍待完成。
