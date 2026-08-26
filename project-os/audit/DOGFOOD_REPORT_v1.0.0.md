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

## Initial Candidate Package / 初始候选安装包

The implementation and dogfood evidence were committed at `c6317fa`, then two delayed deterministic packages were built from that commit.

实现和 dogfood 证据提交于 `c6317fa`，随后从该提交构建两个有时间间隔的确定性安装包。

```text
Candidate A: releases/ai-project-os-v1.0.0-candidate-a.zip
Candidate B: releases/ai-project-os-v1.0.0-candidate-b.zip
SHA-256: e8926363aec753dc613a7bde2df2f5906106e778c4b769432c84419328f8094e
Size: 274979 bytes
Byte comparison: identical
Archive integrity: pass
Extracted strict validator: 0 failures, 0 warnings
Extracted automated tests: 72/72 pass
Extracted representative messy-project certification: included in full suite
```

After the UAT evidence and Draft PR metadata were committed, the package was rebuilt from branch commit `2fa9d6f`. It was byte-identical to Candidate A, kept the same SHA-256 and size, passed archive integrity, and passed the extracted strict validator plus all 72 tests again.

UAT 证据和 Draft PR 元数据提交后，又从分支提交 `2fa9d6f` 重建安装包。它与 Candidate A 逐字节相同，SHA-256 和大小不变，并再次通过归档完整性、解压后严格验证和全部 72 个测试。

## Real Mature Project UAT / 真实成熟项目 UAT

The initial candidate was installed on a dedicated branch of **展会宝 TradeShow Copilot**, a working trade-show PWA repository. Three pre-existing vendor SVG deletions were preserved. Product commands, dependency installation, production, Linear, and GitHub writes remained disabled.

初始候选被安装到真实展会 PWA 仓库 **展会宝 TradeShow Copilot** 的专用分支。3 个既有 vendor SVG 删除被原样保留。产品命令、依赖安装、生产访问、Linear 和 GitHub 写入始终禁用。

```text
Product files: 35
Documents: 4
Entrypoints: 2
Discovered automated tests: 0
Lockfiles: 0
Initial gate: SAFETY_BLOCKED
Initial safety Block: 1
Initial open findings: 11
Product writes performed: 0
External writes performed: 0
Linear writes performed: 0
```

The real repository exposed two AI Project OS candidate defects. A Worker-context environment lookup was conservatively misclassified as an embedded credential, and custom rescue output produced documentation references that pointed at the default output directory. Both were fixed in `544cd32` with focused regression tests and source/template parity.

真实仓库暴露了两个 AI Project OS 候选缺陷：Worker context 环境变量读取被保守地误判为嵌入凭证；自定义救援输出生成的文档引用仍指向默认目录。两项均在 `544cd32` 修复，并增加专项回归测试及源码/模板同步验证。

The corrected candidate was installed over the OS package without changing product files. Two full rescue outputs were byte-identical, `verify` passed, provider-credential patterns were absent, and output references stayed portable.

修正候选覆盖 OS 包时没有修改产品文件。两次完整救援输出逐字节一致，`verify` 通过，不含 provider 凭证模式，输出引用保持可移植。

```text
Corrected gate: NEEDS_HUMAN_DECISION
Corrected safety Block: 0
Corrected safety Review: 0
Open findings: 9
Resolved OS finding: TSC-SAF-001
Human Queue: target version, Git state, API access, external-data policy, local-device policy
Codex Queue: dependency reproducibility, automated tests, service-worker path bug
Backlog: CI decision
Product writes performed: 0
External writes performed: 0
Linear writes performed: 0
```

The resulting project diagnosis surfaced a real built-path contradiction in feedback offline registration plus security, privacy, device-retention, test, dependency, Git, and CI gaps. Business answers were not invented; high-impact unknowns remained in the Human Queue.

最终项目诊断发现反馈离线注册存在真实构建路径冲突，并暴露安全、隐私、设备保留、测试、依赖、Git 和 CI 缺口。系统没有虚构业务答案，高影响未知项继续留在人类队列。

## Corrected Candidate Package / 修正候选安装包

Two packages were built from `544cd32` after real-project fixes.

真实项目修复完成后，从 `544cd32` 构建两个安装包。

```text
Candidate A: releases/ai-project-os-v1.0.0-real-uat-a.zip
Candidate B: releases/ai-project-os-v1.0.0-real-uat-b.zip
SHA-256: e86be5ebaa9670d4a41717132b2754e5d49302fac319cc2094d8b772e21f2f2e
Size: 275338 bytes
Byte comparison: identical
Archive integrity: pass
Extracted strict validator: 0 failures, 0 warnings
Extracted automated tests: 73/73 pass
```

The candidate zip remains a local/GitHub Release artifact and is not added to Git source history.

候选 zip 继续作为本地/GitHub Release 产物，不加入 Git 源码历史。

## Accepted Release-Metadata Package / 已验收发布元数据安装包

After Owner UAT Pass, two packages were independently built from committed release metadata at `817cae8`.

Owner 通过 UAT 后，从已提交的发布元数据 `817cae8` 独立构建两个安装包。

```text
Candidate A: releases/ai-project-os-v1.0.0-final-a.zip
Candidate B: releases/ai-project-os-v1.0.0-final-b.zip
SHA-256: 6dcec2eae38af467ec68062a5e18be1171152af558578b03323f7a5be1cfdd99
Size: 275400 bytes
Byte comparison: identical
Archive integrity: pass
Extracted strict validator: 0 failures, 0 warnings
Extracted automated tests: 73/73 pass
```

The review surface was PR [#9](https://github.com/adwasd-dvd/ai-project-os/pull/9). Owner UAT passed and v1.0.0 was released on 2026-08-26. The uploaded asset was re-downloaded and verified byte-identical with SHA-256 `6dcec2eae38af467ec68062a5e18be1171152af558578b03323f7a5be1cfdd99`.

审查入口为 PR [#9](https://github.com/adwasd-dvd/ai-project-os/pull/9)。Owner 已于 2026-08-26 通过 UAT，v1.0.0 随后发布；上传资产已重新下载并验证为逐字节一致。

## Current Conclusion / 当前结论

The v1.0 rescue engine has automated and real-mature-project evidence for orchestration, sanitization, contradiction/safety routing, resolutions, recovery planning, one-Project Linear drafts, proactive PM queues, deterministic reruns, and extracted-package certification. Real UAT found and closed two OS defects without changing the target product. Consolidated Owner UAT, release, remote verification, Linear closeout, and post-release verification passed under AIPOS-059.

v1.0 救援引擎拥有编排、脱敏、矛盾/安全路由、解决记录、恢复计划、单 Project Linear 草案、积极型 PM 队列、确定性重跑和解压包认证的自动及真实成熟项目证据。真实 UAT 在不修改目标产品的情况下发现并关闭两个 OS 缺陷；AIPOS-059 的统一 Owner UAT、发布、远端核验、Linear 关账与发布后验证均已通过。
