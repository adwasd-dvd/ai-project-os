# UAT v0.3.0

This record must be completed by a human Owner or delegated UAT reviewer.

本记录必须由人类 Owner 或被授权的 UAT reviewer 完成。

## UAT Header

```text
Version: v0.3.0
Date: 2026-08-19
Environment: local repo + Linear DvdTeacher
Build / Commit: local release package `releases/ai-project-os-v0.3.0.zip`; GitHub publication deferred
Tester: Owner / dvdTeacher
Owner: dvdTeacher
Result: Pass
```

## Version Goal

Make Human/Codex handoff clear and low-friction in Linear by using assignee as the basic next-actor signal.

通过 assignee 作为基础下一动作信号，让 Linear 里的 Human/Codex 交接清楚、低摩擦。

## Scope

### Included

```text
- DEC-006 Confirm assignee-driven Human/Codex handoff model
- AIPOS-019 Assignee-driven Human/Codex handoff policy
- AIPOS-020 Update Linear intake routing for status + assignee
- AIPOS-021 Handoff prompt library and UAT playbook
- AIPOS-022 Validator guardrails for v0.3 handoff rules
- AIPOS-023 Codify roadmap through v1.0 and post-1.0 open-source readiness
```

### Excluded

```text
- v0.4 Project Whitebox / Existing Project Intelligence implementation
- v0.5 Repo Safety & Project Memory Boundary implementation
- v0.6 scheduled/cron runner implementation
- Automatic local code execution from scheduled automation
- GitHub tag/release creation until human UAT passes or Owner explicitly requests it
```

## Codex Verification To Run

```text
python3 project-os/tools/validate_project_os.py --root .
python3 template/project-os/tools/validate_project_os.py --root .
python3 -m py_compile project-os/tools/validate_project_os.py template/project-os/tools/validate_project_os.py
unzip -t releases/ai-project-os-v0.3.0.zip
```

Result:

```text
Passed
```

## Human UAT Scenarios

| Scenario ID | Feature ID | Scenario | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|
| UAT-001 | AIPOS-019 | Read `LINEAR_POLICY.md` handoff section | Rule is understandable: assigned = human queue, unassigned = Codex queue | Owner accepted the assignee-driven rule | Pass | Approved in Codex task |
| UAT-002 | AIPOS-020 | Inspect a `Todo + unassigned` issue | Codex classifies it as Codex Queue only after Ready checks | Owner accepted the queue model | Pass | Approved in Codex task |
| UAT-003 | AIPOS-020 | Inspect a `Todo + assigned` issue | Codex classifies it as Human Queue and does not start work | Owner accepted the queue model | Pass | Approved in Codex task |
| UAT-004 | AIPOS-020 | Inspect an `In Review + assigned` issue | Codex classifies it as Review/UAT Queue and waits for human pass/fail | Owner accepted the review handoff | Pass | Approved in Codex task |
| UAT-005 | AIPOS-021 | Simulate failed UAT | Human comment + unassign + `Todo` hands the issue back to Codex | Owner accepted the failed-UAT loop | Pass | Approved in Codex task |
| UAT-006 | AIPOS-021 | Simulate UAT pass | Human moves issue to `Done`; Codex does not self-approve | Owner explicitly approved v0.3.0 | Pass | Approved in Codex task |
| UAT-007 | AIPOS-022 | Run validator | Validator passes and checks v0.3 handoff guardrails | Validator passed | Pass | Codex verification evidence |
| UAT-008 | AIPOS-023 | Read `ROADMAP.md` | v0.4-v1.0 direction and 1.0 success standard match Owner intent | Owner approved continuing with the roadmap | Pass | Approved in Codex task |
| UAT-009 | AIPOS-021 | Follow `examples/FIRST_PROJECT.md` handoff loop | User can operate without maintaining `next:*` labels | Owner accepted the operating model | Pass | Approved in Codex task |
| UAT-010 | AIPOS-022 | Inspect `releases/ai-project-os-v0.3.0.zip` | Zip contains top-level `project-os/` with v0.3 docs, roadmap, example, and validator | Archive test passed | Pass | Codex verification evidence |

## Issues Found

| ID | Description | Severity | Category | Target Version | Linear Issue | Owner |
|---|---|---|---|---|---|---|
|  |  |  | Current Fix / Patch / Next / Backlog / Decision |  |  |  |

## Final UAT Decision

```text
UAT 通过，允许发布 v0.3.0。
```

## Sign-off

```text
Accepted By: dvdTeacher / Owner
Date: 2026-08-19
Notes: User stated `UAT 通过，允许发布 v0.3.0。开始 v0.4。`
```
