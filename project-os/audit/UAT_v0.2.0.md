# UAT v0.2.0

This record must be completed by a human Owner or delegated UAT reviewer.

本记录必须由人类 Owner 或被授权的 UAT reviewer 完成。

## UAT Header

```text
Version: v0.2.0
Date: 2026-08-19
Environment: local repo + Linear DvdTeacher
Build / Commit: 30b1abc + working tree v0.2.0 package state
Tester: Owner
Owner: Owner
Result: Pass
```

## Version Goal

Make AI Project OS usable as a practical day-to-day Linear-driven workflow after initial import.

让 AI Project OS 在首次导入后，能作为日常 Linear 驱动的项目管理和 Codex 协作流程使用。

## Scope

### Included

```text
- AIPOS-009 Automated policy validator
- AIPOS-010 Worked first-project example
- AIPOS-011 Codex Linear follow-up automation design
- AIPOS-012 Requirement and issue management workflow
- AIPOS-013 Version planning and staged delivery workflow
- AIPOS-014 Linear-driven Codex handoff prompt library
- AIPOS-015 Linear intake scan and inconsistency guardrails
- AIPOS-016 Cron-ready Linear intake runner design
- AIPOS-017 Bilingual Linear output policy
- AIPOS-018 Version closeout and carry-over revalidation workflow
```

### Excluded

```text
- Actual unattended local code execution from cron/scheduled automation
- Cloud Codex execution policy beyond documented future decision boundary
- GitHub release/tag creation until human UAT passes
```

## Codex Verification Already Run

```text
python3 project-os/tools/validate_project_os.py --root .
python3 template/project-os/tools/validate_project_os.py --root .
python3 -m py_compile project-os/tools/validate_project_os.py template/project-os/tools/validate_project_os.py
unzip -t releases/ai-project-os-v0.2.0.zip
```

Result:

```text
Passed
```

## Human UAT Scenarios

| Scenario ID | Feature ID | Scenario | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|
| UAT-001 | AIPOS-012 | Give Codex a messy product idea and ask it to classify without coding | Codex separates Idea/Requirement/Feature/Decision/Backlog and does not start development |  |  |  |
| UAT-002 | AIPOS-013 | Ask Codex to split a broad feature across v0.2/v0.3/Backlog | Each deliverable issue has one target version and staged acceptance criteria |  |  |  |
| UAT-003 | AIPOS-014 | Use a broad `检查 Linear` prompt | Codex reports scan scope, scanned, created, updated, skipped, blockers, and next action before work |  |  |  |
| UAT-004 | AIPOS-015 | Verify older-version feedback is not missed while reviewing v0.2 | Old-version active/recent feedback is detected or explicitly skipped with reason |  |  |  |
| UAT-005 | AIPOS-016 | Simulate two scheduled dry-runs | No duplicate comments/issues and no automatic code execution |  |  |  |
| UAT-006 | AIPOS-017 | Inspect one issue comment and one project status update | Both include Chinese user-facing summary |  |  |  |
| UAT-007 | AIPOS-018 | Reproduce DVD-7/DVD-8 style carry-over closeout | Old issue is not moved; new/updated next-version issue keeps source link and expected result |  |  |  |
| UAT-008 | AIPOS-009 | Run validator | Output is understandable and reports pass/fail with paths and hints |  |  |  |
| UAT-009 | AIPOS-010 | Follow `examples/FIRST_PROJECT.md` | User can understand what to type, what to check, and when to stop |  |  |  |
| UAT-010 | AIPOS-009/AIPOS-010 | Inspect `releases/ai-project-os-v0.2.0.zip` | Zip contains top-level `project-os/` with v0.2 docs, example, and validator |  |  |  |
| UAT-011 | AIPOS-012/AIPOS-014 | Discuss whether Linear labels or assignee should express Human/Codex ownership | v0.2 can ship; assignee-driven handoff is classified as next-version work for v0.3 | Owner confirmed v0.3 direction | Pass | Owner asked to proceed with the recommended version plan |

## Issues Found

| ID | Description | Severity | Category | Target Version | Linear Issue | Owner |
|---|---|---|---|---|---|---|
|  |  |  | Current Fix / Patch / Next / Backlog / Decision |  |  |  |

## Final UAT Decision

Choose one:

```text
UAT 通过，允许发布 v0.2.0。
```

Owner approval recorded from conversation on 2026-08-19:

```text
可以按照你的建议往前做吧。
```

This approval is interpreted as permission to close v0.2.0 and start v0.3 under the recommended plan.

本批准被解释为允许关闭 v0.2.0，并按建议路线启动 v0.3。

```text
UAT 未通过，必须先处理以下问题：
-
```

```text
有条件通过，允许发布 v0.2.0，但以下问题必须进入 Patch：
-
```

## Sign-off

```text
Accepted By:
Accepted By: Owner
Date: 2026-08-19
Notes: v0.2.0 accepted as the Linear-driven day-to-day workflow baseline. Assignee-driven Human/Codex handoff is accepted as v0.3 scope rather than a v0.2 blocker.
```
