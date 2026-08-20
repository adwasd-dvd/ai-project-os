# UAT v0.5.0

This record must be completed by a human Owner or delegated UAT reviewer.

本记录必须由人类 Owner 或被授权的 UAT reviewer 完成。

## UAT Header

```text
Version: v0.5.0
Date: 2026-08-20
Environment: local repo + Linear DvdTeacher + GitHub Draft PR
Build / Commit: branch codex/v0.5-repo-safety; Draft PR pending
Tester: Owner / dvdTeacher
Owner: dvdTeacher
Result: Pending
```

Candidate package:

```text
Path: releases/ai-project-os-v0.5.0.zip
SHA-256: 75eee07ddc40075399ae237044676dfb419f257c7e55461c04205d1fdda44120
Git policy: ignored locally; publish only as a GitHub Release asset after UAT
```

## Version Goal

Make repository publication, Agent documents, and incomplete project memory controllable without exposing the content a safety check is meant to protect.

让仓库发布、Agent 文档和断档项目记忆变得可控，同时不在安全检查证据中泄露被保护内容。

## Codex Verification

```text
python3 project-os/tools/validate_project_os.py --root . --strict
python3 -m unittest discover -s project-os/tools -p 'test_*.py'
python3 project-os/tools/safety_scan.py --root . --profile local --scope worktree --summary
python3 project-os/tools/safety_scan.py --root . --profile private --scope staged --fail-on-block --summary
python3 project-os/tools/safety_scan.py --root . --profile public --scope tracked --fail-on-block --summary
unzip -t releases/ai-project-os-v0.5.0.zip
python3 <extracted>/project-os/tools/validate_project_os.py --root <extracted> --strict
python3 -m unittest discover -s <extracted>/project-os/tools -p 'test_*.py'
git diff --check
```

Current automated evidence:

```text
Strict validator: 0 failures, 0 warnings
Automated tests: 10 passed
Local/worktree safety scan: Block 0, Review 0, Gate Go
Archive integrity: Passed
Extracted standalone validator: 0 failures, 0 warnings
Extracted standalone tests: 10 passed
Staged/private safety gate: Block 0, Review 0, Gate Go
Public/tracked advisory: Block 0, Review 32, Gate Review
Review disposition: 30 Private Repo memory records and 2 Team Shared Agent docs are compatible with the current PRIVATE GitHub destination; not pre-approved for future public visibility
```

## Human UAT Scenarios

| Scenario ID | Feature ID | Action Steps / 执行动作 | Expected Result / 期待结果 | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|
| SAF-001 | AIPOS-031 | Read `SECURITY_BOUNDARY.md` and classify one credential, team runbook, private audit, and public template / 阅读政策并分类四类资产 | Each maps clearly to Local Only, Team Shared, Private Repo, or Public Safe / 四级分类清楚且私有仓库不是 secret store | Pending Owner | Pending |  |
| SAF-002 | AIPOS-032 | Read `REPO_PUBLICATION_POLICY.md` and this manifest / 阅读发布政策和本 manifest | PR, private/team share, and public Release have distinct scan and human gates / 不同发布目标有不同检查且最终由人决定 | Pending Owner | Pending |  |
| SAF-003 | AIPOS-033 | Choose the appropriate Agent-doc mode for a single-user and team project / 为单人和团队项目选择 Agent 文档模式 | Personal memory stays local; stable shared rules can use a canonical reviewed file / 个人记忆留本地，稳定规则经 review 后共享 | Pending Owner | Pending |  |
| SAF-004 | AIPOS-034 | Review the memory audit and doc-gap templates / 检查项目记忆与文档缺口模板 | Chat-only claims, contradictions, stale decisions, and missing evidence stay visible / 断档、冲突和缺证据事项不会被当作事实 | Pending Owner | Pending |  |
| SAF-005 | AIPOS-035 | Run scanner tests or inspect provided results / 运行 scanner 测试或检查证据 | Scanner is read-only by default, deterministic, confined, and emits no matched content / 默认只读、稳定、限制写入且不输出命中内容 | Codex: 5 scanner tests passed | Pending Owner | Automated evidence ready |
| SAF-006 | AIPOS-036 | Open the release zip and run strict validation / 解压候选包并严格验证 | One top-level `project-os/`; standalone validator and 10 tests pass / 只有一个顶层目录且独立验证与测试通过 | Codex: Passed | Pending Owner | Automated evidence ready |
| SAF-007 | AIPOS-037 | Follow only the README 60-Second Start and `QUICKSTART.md` / 只按 GitHub 快速启动说明操作 | User can download, place `project-os/`, open Codex, paste one prompt, and understand the first response / 用户可下载、放入、发送一句话并理解 Codex 首次反馈 | Pending Owner | Pending | Primary user-facing check |
| SAF-008 | AIPOS-035 | Use a test file containing a secret-like value / 用测试夹具模拟疑似 secret | Finding contains rule/path/classification/disposition/remediation but not value or source line / finding 有处置信息但不泄露值或源行 | Codex: Passed | Pending Owner | Covered by unit tests |
| SAF-009 | AIPOS-032 | Review a private-repo publication decision / 检查私有仓库发布判断 | Credentials/private keys still Block; repository visibility does not waive classification / 凭证仍阻塞，私有可见性不代表安全分类 | Codex: Policy + tests pass | Pending Owner |  |
| SAF-010 | AIPOS-036 | Compare source and `template/project-os/` / 比较源码与分发模板 | Generic files match; project-specific audit data does not leak into template package / 通用文件一致且 dogfood 审计不泄露到分发模板 | Codex: strict drift check passed | Pending Owner |  |
| SAF-011 | AIPOS-032 | Compare private release and future public visibility / 比较当前私有发布与未来公开仓库 | Current private-compatible Review items remain visible and must be reclassified before any visibility change / 当前可进入私有仓库的内容在未来公开前仍需重新分类 | Codex: 32 Review items grouped and dispositioned | Pending Owner |  |

## Minimal Owner Check

The Owner only needs to confirm these three user-facing judgments:

Owner 只需重点确认这三项：

1. `README.md` 和 `QUICKSTART.md` 是否真的足够简单。
2. 四级分类与 private-repo 边界是否符合你的直觉。
3. Agent 文档和聊天断档的处理方式是否符合你希望的项目管理方式。

## Issues Found

| ID | Description | Severity | Category | Target Version | Linear Issue | Owner |
|---|---|---|---|---|---|---|
| Pending | Human UAT not yet completed / 尚未完成人工验收 | Gate | UAT | v0.5.0 | DVD-83 through DVD-89 | Owner |

## Final UAT Decision

Pass:

```text
UAT 通过，允许发布 v0.5.0。
```

Fail:

```text
UAT 未通过，必须先处理以下问题：
-
```

## Sign-off

```text
Accepted By: Pending
Date: Pending
Notes: Pending human review
```
