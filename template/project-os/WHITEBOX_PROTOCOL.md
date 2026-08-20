# WHITEBOX_PROTOCOL

This protocol defines how AI Project OS turns an existing black-box or gray-box repository into an evidence-backed project model.

本协议定义 AI Project OS 如何把现有黑盒/灰盒仓库变成基于证据的项目模型。

Whitebox discovery happens after Phase 0 Self-Check and before the Phase 1 baseline is presented for human confirmation.

白盒发现位于 Phase 0 Self-Check 之后、Phase 1 baseline 提交人工确认之前。

## Goal / 目标

Whitebox discovery must make the project:

白盒发现必须让项目变得：

- understandable: a human can explain what the system does;
- inspectable: important claims point to evidence;
- manageable: findings can become decisions, features, bugs, or backlog;
- honest: unknowns and contradictions stay visible;
- repeatable: another Codex run can reproduce the evidence collection.

- 可理解：人类可以解释系统在做什么；
- 可检查：重要结论指向证据；
- 可管理：发现可转成 Decision、Feature、Bug 或 Backlog；
- 诚实：未知项和矛盾保持可见；
- 可重复：另一次 Codex 可复现证据收集。

Whitebox discovery is not a promise that every behavior is understood. It is a controlled way to show what is known, how it is known, and what still needs verification.

白盒发现不保证所有行为都已被理解。它用可控方式展示已知什么、如何得知、还需要验证什么。

## Safety Contract / 安全契约

The discovery path is read-only by default.

Discovery 路径默认只读。

Allowed:

- read repository files, Git metadata, tests, and configuration names;
- run `tools/whitebox_scan.py` without `--write`;
- write only under `project-os/discovery/` when the user requested discovery output or the current phase allows audit-document writes;
- record environment-variable names from example/template files;
- record paths of secret-like files without reading or reproducing their values.

允许：

- 读取仓库文件、Git 元数据、测试和配置名称；
- 在不使用 `--write` 时运行 `tools/whitebox_scan.py`；
- 仅在用户要求 discovery 产物或当前阶段允许写 audit 文档时，写入 `project-os/discovery/`；
- 从 example/template 文件记录环境变量名称；
- 记录 secret-like 文件路径，不读取、不复制其值。

Forbidden:

- modify product code, dependencies, lockfiles, or runtime data during discovery;
- connect to production services or databases;
- print or persist passwords, tokens, private keys, cookies, connection strings, or environment-variable values;
- execute unknown project scripts merely to learn what they do;
- describe an inferred security property as verified;
- automatically create or update Linear from unconfirmed whitebox findings.

禁止：

- discovery 期间修改产品代码、依赖、lockfile 或运行时数据；
- 连接生产服务或数据库；
- 输出或保存密码、token、私钥、cookie、连接字符串或环境变量值；
- 为了了解未知脚本而直接执行它；
- 把推断的安全属性描述为已验证；
- 把未确认的白盒发现自动写入 Linear。

After whitebox discovery, v0.5 runs Phase 0.75 Safety Classification. Use `SECURITY_BOUNDARY.md`, `REPO_PUBLICATION_POLICY.md`, and `tools/safety_scan.py` before Git, team sharing, or public publication. Whitebox evidence may record names and paths; secret values may never be recorded.

白盒发现完成后，v0.5 进入 Phase 0.75 Safety Classification。进入 Git、团队共享或公开发布前，使用 `SECURITY_BOUNDARY.md`、`REPO_PUBLICATION_POLICY.md` 和 `tools/safety_scan.py`。白盒证据可记录名称和路径，但绝不能记录 secret 值。

## Evidence Vocabulary / 证据语汇

Every important finding must use one of these states:

每个重要发现必须使用以下状态之一：

| State | Meaning | 含义 |
|---|---|---|
| Observed | Directly visible in code, config, test output, runtime output, or Git evidence | 直接观察于代码、配置、测试、运行输出或 Git 证据 |
| Derived | Mechanically calculated from observed evidence | 由已观察证据机械计算得出 |
| Claimed | Stated by documentation, comments, issues, or conversation | 由文档、注释、Issue 或对话声称 |
| Inferred | Reasoned from indirect evidence and not yet directly verified | 根据间接证据推断，未直接验证 |
| Contradicted | Two or more relevant sources disagree | 两个或以上相关来源相互冲突 |
| Unknown | Evidence is missing or insufficient | 证据缺失或不足 |

Do not use `Observed` for a statement found only in README or a conversation. That is `Claimed` until code, tests, runtime evidence, or another authoritative source confirms it.

如果说法只出现在 README 或对话中，不得标为 `Observed`。在代码、测试、运行证据或其他权威来源确认前，它属于 `Claimed`。

## Confidence / 置信度

Confidence describes evidence strength, not business impact.

置信度描述证据强度，不是业务影响。

| Confidence | Minimum interpretation | 最低解释 |
|---|---|---|
| High | Direct evidence is current and corroborated, or a deterministic result is reproducible | 当前直接证据有交叉验证，或确定性结果可复现 |
| Medium | One direct source or several aligned indirect sources exist, but an important verification is missing | 存在一个直接来源或多个一致间接来源，但缺少重要验证 |
| Low | Mostly inference, stale claims, partial coverage, or unresolved contradiction | 主要依赖推断、过期说法、不完整覆盖或未解矛盾 |
| Unknown | Confidence cannot yet be assigned | 尚无法分配置信度 |

A high-impact finding can have low confidence. Keep `Impact` and `Confidence` in separate fields.

高影响发现可以只有低置信度。`Impact` 和 `Confidence` 必须分开记录。

## Evidence Precedence / 证据优先级

When sources disagree, prefer the most current source that directly demonstrates behavior. Use this default order, then document exceptions:

来源冲突时，优先使用能直接证明行为的最新来源。默认顺序如下，如有例外必须记录：

1. Reproducible runtime or test evidence / 可复现运行或测试证据.
2. Executed code and active configuration / 实际执行代码和当前配置.
3. Schema, migration, API contract, or lockfile / schema、migration、API 契约或 lockfile.
4. Git history and reviewed change records / Git 历史和已 review 变更记录.
5. Current maintained documentation / 当前受维护文档.
6. Issue, comment, or conversation claim / Issue、评论或对话说法.
7. Inference / 推断.

Passing tests prove only the behavior they actually cover. They do not automatically prove the whole product rule.

测试通过只能证明其实际覆盖的行为，不能自动证明整个产品规则。

## Minimum Finding Record / 最小发现记录

Every important conclusion, risk, contradiction, or unknown must include:

每个重要结论、风险、矛盾或未知项必须包含：

```text
Finding ID:
Claim:
State: Observed / Derived / Claimed / Inferred / Contradicted / Unknown
Evidence:
Evidence Freshness:
Confidence: High / Medium / Low / Unknown
Impact: Critical / High / Medium / Low / Unknown
Unknowns:
Contradictions:
Next Verification:
Recommended Disposition: Confirm / Decision / Bug / Feature / Backlog / Accept Risk
Owner:
```

Evidence should use a stable locator when possible:

证据应尽量使用稳定定位：

```text
path/to/file.ext:line
test command + result
commit SHA
Linear issue ID
GitHub PR or release URL
runtime observation + environment + date
```

## Discovery Sequence / 发现顺序

### Phase 0.5A - Scope and Safety / 范围与安全

1. Confirm repository root and allowed read scope.
2. Identify excluded directories, submodules, generated content, large files, and unavailable systems.
3. Confirm that production access is not required.
4. Record coverage limits before making conclusions.

1. 确认仓库根目录和允许读取范围。
2. 识别排除目录、submodule、生成内容、大文件和不可用系统。
3. 确认不需要生产访问。
4. 在得出结论前记录覆盖限制。

### Phase 0.5B - Mechanical Evidence / 机械证据

Run:

```bash
python3 project-os/tools/whitebox_scan.py --root .
```

This is a dry run and writes nothing. After reviewing the path-only output, write deterministic evidence with:

这是 dry run，不写入。检查只包含路径的输出后，可写入确定性证据：

```bash
python3 project-os/tools/whitebox_scan.py --root . --write
```

Expected output:

```text
project-os/discovery/SCAN_EVIDENCE.json
```

The scanner supplies evidence candidates. It does not explain business purpose or prove runtime behavior.

Scanner 只提供证据候选，不解释业务用途，也不证明运行时行为。

### Phase 0.5C - Interpret the System / 解释系统

Complete these reports in order:

按顺序完成：

1. `discovery/PROJECT_MAP.md`
2. `discovery/DEPENDENCY_MAP.md`
3. `discovery/DOCUMENT_INVENTORY.md`
4. `discovery/SETTINGS_AND_DATA_REGISTER.md`
5. `discovery/LOGIC_BOUNDARY_AUDIT.md`
6. `discovery/WHITEBOX_IMPORT_REPORT.md`

Every report must record scan coverage and unanswered questions. Empty tables do not count as completed discovery.

每份报告必须记录扫描覆盖和未回答问题。空表格不算完成 discovery。

### Phase 0.5D - Reconcile / 对账

Cross-check:

- documentation against code and configuration;
- declared dependencies against lockfiles and observed imports;
- stated runtime commands against scripts and CI;
- data claims against schemas and migrations;
- authorization claims against code paths and tests;
- Linear/GitHub status claims against repository evidence.

交叉检查：

- 文档与代码/配置；
- 声明依赖与 lockfile/实际 import；
- 声称的运行命令与 script/CI；
- 数据说法与 schema/migration；
- 授权说法与代码路径/测试；
- Linear/GitHub 状态说法与仓库证据。

Do not silently choose a winner when relevant sources disagree. Create a contradiction record and define the next verification.

相关来源冲突时，不得静默选择其中一个。必须创建矛盾记录并定义下一步验证。

### Phase 0.5E - Management Handoff / 管理交接

Use `WHITEBOX_IMPORT_REPORT.md` to prepare:

- the human baseline review;
- a compact bilingual Linear project summary;
- proposed Features, Bugs, Decisions, and Backlog;
- verification work for low-confidence, high-impact findings.

使用 `WHITEBOX_IMPORT_REPORT.md` 准备：

- 人工 baseline review；
- 紧凑双语 Linear 项目摘要；
- 建议的 Feature、Bug、Decision 和 Backlog；
- 低置信度、高影响发现的验证工作。

The first Linear bulk-write approval gate still applies.

首次 Linear 批量写入授权门禁仍然适用。

## Stop Conditions / 停止条件

Stop and ask the human when:

- repository scope is ambiguous;
- access would require production credentials or private data;
- a high-impact behavior has contradictory evidence and determines architecture or business scope;
- generated or vendor content dominates the scan and exclusion policy is unclear;
- submodules or linked repositories are required but unavailable;
- the next step would modify product code, dependencies, runtime state, Linear, or GitHub without authorization.

以下情况必须停下并询问人类：

- 仓库范围不明；
- 需要生产凭证或私密数据；
- 决定架构或业务范围的高影响行为存在矛盾证据；
- 生成/vendor 内容占据主体，且排除规则不明；
- 必需的 submodule 或关联仓库不可用；
- 下一步将在未授权时修改产品代码、依赖、运行时状态、Linear 或 GitHub。

## Whitebox Complete / 白盒完成条件

Whitebox discovery is ready for baseline confirmation only when:

只有满足以下条件，才可将白盒发现交给 baseline 确认：

- all six reports exist and name their coverage limits;
- every important conclusion has state, evidence, confidence, and next verification;
- important unknowns and contradictions are visible;
- no secret values appear in discovery outputs;
- high-impact low-confidence findings are routed to verification or Decision;
- `WHITEBOX_IMPORT_REPORT.md` links the detailed evidence;
- Codex stops for human confirmation before Linear import.

- 六份报告齐全并说明覆盖限制；
- 每个重要结论都有状态、证据、置信度和下一步验证；
- 重要未知项和矛盾可见；
- discovery 产物不含 secret 值；
- 高影响、低置信度发现已路由到验证或 Decision；
- `WHITEBOX_IMPORT_REPORT.md` 链接详细证据；
- Codex 在 Linear import 前停下等待人工确认。
