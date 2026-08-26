# QUALITY_GATE

本文定义每个阶段的质量门禁。

质量门禁的目的不是增加流程，而是防止 AI 和人把“做了一点”误认为“可以交付”。

## Ready for Mature-Project Rescue

v1.0 救援开始前必须满足：

- 项目根目录和允许读取范围已确认；
- 已读取 `RESCUE_PROTOCOL.md`；
- 先运行 `tools/rescue_project.py inspect`，默认不写证据；
- 产品证据默认排除已安装的 `project-os/`；
- publication profile 已选择，或明确标记为待确认；
- 不需要生产凭证、生产数据、未知脚本执行或依赖安装；
- 任何声明发现都使用 English + Chinese，并包含 Evidence、State、Impact、Confidence、Action Steps、Expected Result 和 Next Verification。

## Rescue Evidence Complete

救援证据只有在以下条件满足时才能交给 Baseline review 或 Linear planning：

- `RESCUE_EVIDENCE.json`、`RESCUE_DIAGNOSIS.md`、`RECOVERY_ROADMAP.md`、`LINEAR_RESCUE_IMPORT.json`、`PM_NEXT_ACTION.md` 和 `RESCUE_RECEIPT.json` 齐全；
- `verify` 对当前仓库状态通过；
- 证据不含 matched value、source line、environment value、file content、raw conversation、credential 或 private payload；
- 当前 gate、Human Queue、Codex Queue、Review Queue、blockers 和 next action 都已明确；
- high/critical Contradicted 或 Unknown 已进入人工 Decision/验证，不会静默猜测；
- Linear 包明确为 dry-run、one Project、one Milestone、writes performed 0；
- 工具没有执行产品代码、依赖安装、生产访问、产品写入或外部写入。

## Ready for Development

Feature 进入开发前必须满足：

- 有 Feature ID。
- 有 Linear Issue 或等价记录。
- 有目标版本。
- 有模块归属。
- 有清楚的问题或用户价值。
- 有验收标准。
- 无阻塞 Decision。
- 依赖项已识别。
- 测试要求已说明。
- `CHANGE_IMPACT.md` 七个区域已检查。
- 高影响低置信度结论已有 Next Verification 或已经阻塞开发。
- Traceability manifest 已建立 `planned` 状态。

不满足时，Codex 必须停止并列出缺口。

## Ready for Linear Intake

宽泛 Linear 检查可以开始前必须明确：

- Linear team 或 workspace 可读取。
- 用户点名的 Issue、Project 或版本已经记录。
- 如果用户未点名，Codex 已说明默认 scan scope。
- 将扫描 active statuses 和 lookback window。
- 将按 `LINEAR_INTAKE.md` 输出 bilingual run summary。
- 将按 status + assignee 分出 Codex Queue、Human Queue、Review Queue 和 Inconsistent。
- Codex-ready 的基础定义是 `Todo + unassigned`，但仍必须满足 Feature ID、目标版本、验收标准和无阻塞 Decision。

如果 scan scope 过大或权限不足，Codex 必须先汇报限制。

## Ready for Whitebox Discovery

Phase 0.5 开始前必须明确：

- 项目根目录已确认。
- 可读范围、排除范围和不可用系统已记录。
- 已读取 `WHITEBOX_PROTOCOL.md`。
- scanner dry-run 默认不写入。
- 如需写入，目标只能在仓库内的 `project-os/discovery/`。
- 不需要生产凭证或生产数据。
- secret 值不会被复制到报告。

## Whitebox Complete

白盒发现只有在以下条件满足时才能进入 Baseline Confirmation：

- `PROJECT_MAP.md`、`DEPENDENCY_MAP.md`、`DOCUMENT_INVENTORY.md`、`SETTINGS_AND_DATA_REGISTER.md`、`LOGIC_BOUNDARY_AUDIT.md` 和 `WHITEBOX_IMPORT_REPORT.md` 均已填写。
- 空表不被当作完成证据。
- 每个重要结论都有 State、Evidence、Confidence 和 Next Verification。
- 重要 Unknown 和 Contradicted 发现可见。
- 高影响、低置信度项已转入验证或 Decision。
- discovery 产物不含 secret 值。
- `WHITEBOX_IMPORT_REPORT.md` 可支持人工 review 和 Linear 草案，但未绕过首次写入授权。

## Ready for Safety Classification

Phase 0.75 开始前必须明确：

- 项目根目录和预期 publication profile 已确认，或已明确标记为待人工确认。
- 已读取 `SECURITY_BOUNDARY.md`、`REPO_PUBLICATION_POLICY.md` 和 `AGENT_DOC_POLICY.md`。
- scanner 先 dry run，默认不写文件。
- 写入目标只能位于仓库内，且报告不得包含 matched value、source line、environment value 或 file content。
- 任何删除、凭证轮换、Git 历史改写或远端发布都需要人工授权。

## Safety Classification Complete

Phase 0.75 只有在以下条件满足时才能完成：

- 重要资产已归入 `Local Only`、`Team Shared`、`Private Repo` 或 `Public Safe`。
- publication profile 和目标 destination 已记录。
- Block findings 已处理或明确阻止发布。
- Review findings 已有 disposition、owner 或 Next Verification。
- Agent 文档共享模式已确认。
- 项目记忆和文档缺口已记录，聊天说法未被当作事实。
- 生成的证据不包含命中值、源文件内容或环境变量值。

## Ready for Scheduled Scan

scheduled/cron scan 启用前必须满足：

- `AUTOMATION_POLICY.md` 中的 schedule config 已明确。
- `dry_run: true` 是首次设置默认值。
- mode 已明确为 `read-only`、`advisory` 或 `semi-automatic`。
- idempotency 规则已明确。
- 禁止 automatic code execution。
- 自动写入范围已经由人确认。
- runtime config、reports 和 ledger 位于忽略的 `project-os/runtime/`。
- live token 只来自安全环境变量，不进入 config。
- `scan` 与 `apply` 是不同命令。

## Ready for Automated Linear Write

执行任何自动 Linear write 前必须满足：

- dry-run JSON 的 `planned_actions` 已人工或按既定策略审阅。
- 本地 config 的 `write_policy.enabled` 为 `true`。
- operation 和 update fields 均在最小白名单中。
- apply 命令包含 `--authorize-writes`。
- runtime authorization environment 等于明确授权值。
- 每个 action 有稳定 idempotency key。
- ledger 不记录 API key、评论正文或原始 payload。
- 不包含 code、Decision approval、scope approval、UAT、merge、tag 或 release 动作。

任一条件缺失时必须 fail closed。

## Ready for Change Impact

正式开发前必须：

- 读取 `CHANGE_IMPACT.md`。
- 记录 modules、dependencies、data_security、documentation、tests、uat 和 rollout_rollback。
- 每个重要结论有 level、confidence、evidence 和 next verification。
- `scope_change` 明确为 true/false。
- unresolved Decisions 明确列出。
- automated test plan 与 human UAT plan 分开。

以下情况会阻塞开发：

- 未批准 scope expansion。
- 未解决 Decision。
- high impact + low/unknown confidence。
- 必填区域、test/UAT plan、rollout 或 rollback 缺失。
- evidence path 不存在。

## Traceability Complete for Declared State

`tools/trace_project.py` 必须验证：

- Feature ID 唯一且目标版本一致。
- requirement、Linear、change-impact、code/evidence、tests、UAT 和 release 链接与声明状态相符。
- `verified` 需要 passing automated tests。
- `uat_pending` 明确等待人类。
- `accepted` 必须有人工 UAT Pass 与证据路径。
- `released` 必须有 tag 和 GitHub Release URL。
- schema v2 的 Linear equivalent record 必须包含真实 type、ID、Linear URL 和使用原因，禁止虚构 Issue ID。
- schema v2 的 Feature/版本 UAT Pass 必须包含 actor、date、scenarios、evidence 和 limitations disposition。
- post-release verification 独立于 `accepted` 和 `released`。

## Ready for Release Plan / 发布计划就绪

运行 `tools/release_project.py plan` 前必须准备：

- Included/Excluded/Deferred 范围；
- schema v2 traceability manifest；
- READY change-impact report；
- publication profile、destination、Safety Go、Block 0 与 Review disposition；
- 测试和证据路径；
- 确定性 zip、SHA-256 与 extracted validation；
- rollback target、plan、authority 与 verification；
- GitHub branch 和 PR。

缺人工版本 UAT Pass、Feature acceptance、safety Go、package digest、rollback 或 PR 时必须 `BLOCKED`。

## Ready for OS Upgrade Plan / OS 升级计划就绪

- installed、base 和 target 来源已明确；
- 版本与 source evidence 可验证；
- downgrade 未发生，或有明确人工授权；
- protected paths 覆盖 LOCAL_OVERRIDES、audit、Linear mappings、安全处置、discovery 产物和 runtime/private context；
- 报告只包含 path、hash、classification、risk、decision、validation 和 rollback，不包含文件正文或 secret 值；
- both-modified 或无可信 base 的歧义文件进入 conflict 并阻塞 apply。

## Ready for OS Upgrade Apply / OS 升级执行就绪

- plan 为新鲜、完整、无 conflict 的 `READY`；
- source digest 与 installed hashes 未变化；
- 当前分支符合 upgrade branch prefix；
- 无无关 tracked worktree 改动；
- CLI 包含 `--authorize-upgrade`；
- runtime authorization environment 等于 `APPROVED`；
- 写入只在 installed `project-os/` 内；
- protected files 保持逐字节一致；
- receipt 只写入 ignored `project-os/runtime/`。

apply 后必须进行 hash verify、strict validator、完整测试、目标 safety gate 和项目人工 UAT。工具不得自动 merge、改写历史或批准升级。

## Ready for PR

提交 PR 前必须满足：

- 改动范围与 Feature ID 对应。
- 无明显无关改动。
- 相关测试已运行。
- 新增或修改行为有测试覆盖，或说明为什么暂不覆盖。
- 文档或配置变更已说明。
- 已记录风险和已知限制。
- 已按目标 destination 执行 staged/private safety scan，且 Block findings 为零：

```bash
python3 project-os/tools/safety_scan.py --root . --profile private --scope staged --fail-on-block --summary
```

## Ready for Review

PR 进入 Review 前必须包含：

- Feature ID。
- Linear 链接或引用。
- 目标版本。
- 变更摘要。
- 测试结果。
- 截图或录屏，如果是 UI 变更。
- 数据迁移说明，如果涉及数据库。
- 回滚建议，如果风险较高。
- change-impact report。
- traceability report，声明状态至少为 `verified`。

## Review Pass

Review 通过表示：

- 代码结构可接受。
- 改动范围可接受。
- 测试结果可接受。
- 没有明显阻塞风险。

Review 通过不表示：

- 业务验收通过。
- 版本可以发布。
- UAT 可以跳过。

## Ready for UAT

进入 UAT 前必须满足：

- 当前版本 Included Feature 已完成或明确移出。
- 阻塞 Bug 已清零。
- 关键测试通过。
- UAT 场景已列出。
- UAT 环境或运行方式已明确。
- 已知限制已写明。

v0.2 还必须包含：

- 至少一个 Linear comment 或 project status update 的双语检查。
- 至少一个跨版本 Linear intake/carry-over 检查。
- 如果启用 scheduled scan，必须验证 dry-run 不重复写入。

v0.3 还必须包含：

- `Todo + unassigned` 被识别为 Codex Queue。
- `Todo + assigned` 被识别为 Human Queue。
- `In Review + assigned` 被识别为 Review/UAT Queue。
- 人类验收失败后，留言 + unassign + `Todo` 能让 Codex 下次扫描处理。
- `next:*` label 不作为基础交接必需项。

v0.4 还必须包含：

- scanner dry-run 不创建文件。
- scanner `--write` 仅写入指定 discovery 目录。
- 两次扫描对同一仓库生成确定性结果。
- ignored/generated 路径不进入证据。
- 环境变量和 secret 只记录名称/路径，不记录值。
- 完整示例至少包含一个 Unknown 和一个 Contradicted 发现。
- 人类确认白盒产物“有用且可信”，Codex 不能自我确认。

v0.5 还必须包含：

- `Local Only`、`Team Shared`、`Private Repo` 和 `Public Safe` 四级分类可实际使用。
- scanner 默认只读，且不输出 matched value、source line、environment value 或 file content。
- `worktree`、`staged`、`tracked` scopes 与 `local`、`private`、`team`、`public` profiles 有确定性结果。
- private repository 不被当作 secret store。
- Agent 文档可以选择 local-only、team-shared、organization-shared 或 public-safe 模式。
- 项目记忆审计能保留聊天断档、未证实需求和文档冲突。
- GitHub README 和 `QUICKSTART.md` 能让新用户完成“下载、放入项目、告诉 Codex 开始”流程。

v0.6 还必须包含：

- fixture 与 live dry-run 使用相同 routing/Ready contract。
- 缺少 live credential 时 fail closed。
- `Todo + unassigned`、assigned Todo、assigned In Review、unassigned In Review、Done + recent comment 和 missing Ready fields 全部被正确分类。
- config、CLI 或 runtime 任一 write authorization 缺失时 fail closed。
- 连续 apply 同一 plan 不重复写入。
- 部分失败只重试失败 action。
- ledger 不含 token、comment body 或 raw payload。
- cron-compatible 和 Codex recurring setup 不触发本地代码修改。
- change-impact gate 能阻止未解决 Decision、scope expansion 和 high-impact low-confidence claim。
- traceability validator 不把 automated tests 当作 human UAT。
- requirement -> Linear -> code/evidence -> test -> UAT -> release 证据可追踪。

v0.8 还必须包含：

- code complete、review complete、UAT Pass、released 和 post-release done 可清楚区分；
- 自动测试、Linear Done 或 PR 不能生成 UAT Pass；
- release plan 在缺 UAT、安全 Go、包摘要、回滚或 PR 时 fail closed；
- feedback 能区分 current fix、hotfix、patch、carry-over、next version、Backlog 和 Decision；
- post-release receipt 验证 tag、Release URL、远端/本地 digest 和声明检查；
- installed/upstream version discovery 对缺失网络、错误版本和未授权 downgrade fail closed；
- 三方计划覆盖 identical、add、safe update、migrate、preserve、conflict 和 remove-candidate；
- LOCAL_OVERRIDES、audit/Linear history、安全处置、discovery 和 runtime/private context 不被覆盖；
- apply 需要新鲜 READY 计划、upgrade branch、CLI/runtime 双重授权与路径限制；
- 重跑 apply 幂等，verification failure 只给回滚指引，不自动改写历史；
- 隔离 dogfood 从旧包升级到候选包并通过 source/extracted package 全套测试。

v1.0 还必须包含：

- 一条 rescue inspect/plan/verify 路径可以编排白盒、安全、诊断、恢复路线图、Linear dry-run 和 PM 下一步；
- 安装的 `project-os/` 不进入产品证据，排除范围可见且路径逃逸会 fail closed；
- 同一混乱项目重复运行得到确定性产物和收据；
- 安全 Block、阻塞矛盾、目标版本缺失、Baseline 待确认、Linear 配置/批准和 Ready for Development 具有不同门禁；
- 每个 Linear 草案含 Feature ID、目标版本、Milestone、Action Steps、Expected Result、证据、queue 和稳定去重键；
- 工具绝不实际写 Linear，也不把 input 中的 write approval 当作执行授权；
- credential fixture 会被阻塞，但任何输出都不含命中值；
- 代表性成熟混乱项目包含文档/实现冲突、依赖风险、测试缺口、安全边界和未解决 Decision；
- Owner 能根据诊断、路线图、队列和下一步判断项目是否已经从“糊掉”变成可控；
- source、deterministic package、extracted package、真实仓库 dogfood 和统一 UAT 全部有证据。

## UAT Pass

UAT Pass 必须由人给出。

UAT Pass 需要：

- 验收人姓名或角色。
- 验收日期。
- 验收版本。
- 验收场景。
- 结论。
- 遗留问题分类。

Codex 不得自行给出 UAT Pass。

## Ready for Release

发布前必须满足：

- UAT Pass。
- GitHub CI 通过，或人工批准带风险发布。
- tag/release notes 准备完成。
- Linear 中版本状态已更新。
- 已知限制被 Owner 接受。
- 已完成旧 Issue 的下版本反馈已经 carry-over 或明确不处理。
- `safety/PUBLICATION_MANIFEST.md` 已给出目标 profile、destination 和人工 `Go` 判定。
- 对目标发布集合运行 safety scan 后 Block findings 为零，Review findings 已有明确 disposition。
- GitHub Release asset 已生成 SHA-256，并记录在 release notes 或 closeout 证据中。

## Carry-over Ready

创建下一版本 carry-over revalidation Issue 前必须满足：

- 来源 Issue 已识别。
- 来源评论或反馈已识别。
- 原 Issue 原始范围是否完成已经说明。
- 下一版本目标已确认。
- Revalidation scenario 和 Expected Result 已写清。
- 旧 Issue 将留下 bilingual closeout comment。

## Blocker 定义

以下情况视为 Blocker：

- 核心流程无法完成。
- 数据错误或丢失风险。
- 权限、安全、隐私明显不符合要求。
- UAT 负责人拒绝通过。
- 目标版本 Feature 无法验收。
- 生产部署无法启动或回滚。

## Codex 汇报质量格式

Codex 每次完成开发或修复后，必须给出：

```text
Feature ID:
Target Version:
Status:
Changes:
Tests:
Risks:
Needs Human Check:
New Decisions:
New Backlog Items:
```
