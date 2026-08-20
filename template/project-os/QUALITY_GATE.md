# QUALITY_GATE

本文定义每个阶段的质量门禁。

质量门禁的目的不是增加流程，而是防止 AI 和人把“做了一点”误认为“可以交付”。

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
