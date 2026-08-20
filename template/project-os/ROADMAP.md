# ROADMAP

This roadmap captures the intended path from AI Project OS v0.4 to the internal v1.0 stable release, plus post-1.0 open-source readiness.

本路线图记录 AI Project OS 从 v0.4 到公司内部 v1.0 稳定版的计划，以及 1.0 之后的开源准备方向。

## Product Positioning

AI Project OS is an active AI project manager for software projects.

AI Project OS 是积极型 AI 项目经理。

Its job is not only to help Codex write code. Its job is to make AI-assisted software projects controllable:

它不只是帮 Codex 写代码，而是让 AI 辅助的软件项目变得可控：

- recover messy existing projects;
- turn black-box or gray-box projects into white-box projects;
- keep Linear, local docs, GitHub, UAT, and release state aligned;
- help non-engineering owners use mature software-development discipline;
- support multiple AI coding tools through shared project rules.

- 救活混乱的成熟项目；
- 把黑盒或灰盒项目变成白盒项目；
- 让 Linear、本地文档、GitHub、UAT 和 release 状态保持一致；
- 帮软件工程经验不多的 Owner 使用成熟开发方法管理项目；
- 通过共享项目规则支持不同 AI 编码工具。

## v0.3 - Human/Codex Handoff

Status: Released / 已发布

Goal:

```text
Assigned = human queue
Unassigned = Codex queue
Status = lifecycle
Labels = classification only, optional for advanced workflows
```

目标：

```text
有 assignee = 人类队列
无 assignee = Codex 队列
Status = 生命周期
Labels = 只做分类，高级流程可选
```

Deliverables:

- Assignee-driven Human/Codex handoff policy.
- Linear intake routing by status + assignee.
- Prompt and UAT playbook for pass, failed UAT, clarification, and handoff back to Codex.
- Validator checks that `next:*` labels stay optional in the basic workflow.
- Roadmap through v1.0.

## v0.4 - Project Whitebox / Existing Project Intelligence

Status: Released / 已发布

Goal:

Take an existing black-box or gray-box project and make it understandable, inspectable, and manageable.

目标：

接管一个黑盒/灰盒现有项目，把它变成可理解、可检查、可管理的白盒项目。

Deliverables:

- `WHITEBOX_PROTOCOL.md`
- `tools/whitebox_scan.py`
- deterministic `discovery/SCAN_EVIDENCE.json` generation
- `discovery/PROJECT_MAP.md`
- `discovery/DEPENDENCY_MAP.md`
- `discovery/DOCUMENT_INVENTORY.md`
- `discovery/SETTINGS_AND_DATA_REGISTER.md`
- `discovery/LOGIC_BOUNDARY_AUDIT.md`
- `discovery/WHITEBOX_IMPORT_REPORT.md`
- Linear project description summary with links to whitebox docs.
- Evidence and confidence levels for every important conclusion.
- Worked example, scanner tests, validator guardrails, and human UAT.

## v0.5 - Repo Safety & Project Memory Boundary

Status: Next development / 下一开发版本

Goal:

Define what can be written, committed, published, shared, or kept local.

目标：

定义哪些内容可以写入、提交、发布、共享，哪些必须留在本地。

Deliverables:

- `SECURITY_BOUNDARY.md`
- `REPO_PUBLICATION_POLICY.md`
- `AGENT_DOC_POLICY.md`
- `PROJECT_MEMORY_AUDIT.md`
- `DOC_GAP_REGISTER.md`
- `SECRET_SCAN_REPORT.md`
- Git and secret-scan gates before release or publication.
- Policy for local-only, team-shared, private-repo, and public-safe OS documents.

## v0.6 - Linear Intake / Cron MVP

Goal:

Let Codex safely check Linear on demand or on a schedule, summarize attention items, and prepare the next action without surprise code execution.

目标：

让 Codex 能安全地手动或定时检查 Linear，总结注意事项，并准备下一步，但不突然自动改代码。

Deliverables:

- Scheduled scan configuration.
- Dry-run first setup.
- Idempotent comments and status recommendations.
- Human queue, Codex queue, review queue, blockers, skipped items, and next action in every run summary.
- Permission gates for any automatic write.

## v0.7 - Change Impact & Traceability

Goal:

Before Codex changes a project, it should know what the change touches and how it traces back to requirements, versions, risks, tests, and UAT.

目标：

Codex 修改项目前，必须知道变更会影响什么，并能追溯到需求、版本、风险、测试和 UAT。

Deliverables:

- Requirement-to-issue-to-code traceability.
- Change impact checklist.
- Risk and test impact summary before development.
- Evidence links for important implementation claims.
- Decision and scope-change tracking.

## v0.8 - UAT / Release / Rollback Loop

Goal:

Make "done" mean accepted, releasable, and recoverable.

目标：

让“完成”真正意味着已验收、可发布、可回滚。

Deliverables:

- Version-level UAT checklist generation.
- Feature-level UAT evidence.
- Release notes generation.
- Rollback and hotfix playbook.
- Post-release checks.
- Clear separation between code complete, review complete, UAT pass, release, and post-release done.

## v0.9 - OS Self-Upgrade & Dogfood Hardening

Goal:

AI Project OS should manage its own upgrades without overwriting project memory.

目标：

AI Project OS 应该能管理自己的升级，同时不覆盖项目自己的记忆。

Deliverables:

- Detect installed OS version.
- Check upstream GitHub version when configured.
- Generate upgrade plan and conflict report.
- Preserve `LOCAL_OVERRIDES.md`, audit history, Linear mappings, and private project context.
- Apply migrations through a branch and validator.
- Use AI Project OS to dogfood its own v0.9 release.

## v1.0 - Internal Stable Release

Success standard:

```text
Drop AI Project OS into a messy mature project. It can whitebox the project, expose risks and contradictions, build a Linear-managed roadmap, and guide humans and AI through stable releases.
```

成功标准：

```text
把 AI Project OS 丢进一个已经糊掉的成熟项目里。它能白盒化项目，暴露风险和矛盾，建立 Linear 管理的路线图，并带着人类和 AI 稳定发版。
```

v1.0 should be stable for company-internal use. It does not need to be public open source yet.

v1.0 应该先成为公司内部稳定版，不要求立刻公开开源。

## v1.1-v1.3 - Open-source Readiness

Goal:

Prepare the OS core for public use after the internal system is proven.

目标：

在内部系统被验证后，再准备公开使用的 OS core。

Deliverables:

- Remove company-private assumptions.
- Add public installation guide.
- Add migration guide.
- Add examples that contain no private project data.
- Add contribution guide.
- Separate open-source core rules from private project memory.
- Support Codex, Claude, Cursor, and other AI coding tools through shared local project files.
