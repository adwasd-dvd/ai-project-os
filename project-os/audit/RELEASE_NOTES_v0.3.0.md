# Release v0.3.0

Release notes for AI Project OS v0.3.0.

Human UAT passed on 2026-08-19 and the local release package is approved.

人类 UAT 已于 2026-08-19 通过，本地发布包已获批准。

## Summary

AI Project OS v0.3.0 makes the Human/Codex loop easier to operate in Linear.

AI Project OS v0.3.0 让 Linear 里的 Human/Codex 协作循环更容易使用。

The key rule is:

```text
Assigned = human queue
Unassigned = Codex queue
Status = lifecycle
Labels = classification only, optional for advanced workflows
```

中文规则：

```text
有 assignee = 人类队列
无 assignee = Codex 队列
Status = 生命周期
Labels = 只做分类，高级流程可选
```

## Included Features

| Feature ID | Linear | Summary |
|---|---|---|
| DEC-006 | DVD-51 | Confirm assignee-driven Human/Codex handoff model |
| AIPOS-019 | DVD-52 | Assignee-driven Human/Codex handoff policy |
| AIPOS-020 | DVD-53 | Linear intake routing by status + assignee |
| AIPOS-021 | DVD-54 | Handoff prompt library and UAT playbook |
| AIPOS-022 | DVD-55 | Validator guardrails for v0.3 handoff rules |
| AIPOS-023 | DVD-56 | Roadmap through v1.0 and post-1.0 open-source readiness |

## Fixed Workflow Friction

- Basic handoff no longer requires humans to maintain `next:*` labels.
- `Todo + unassigned` is Codex Queue after Ready checks.
- `Todo + assigned` is Human Queue.
- `In Review + assigned` is Review/UAT Queue.
- Failed UAT handoff is now: comment feedback + unassign + `Todo`.

## Known Limitations

- Scheduled automation still cannot modify local code automatically.
- v0.4 Project Whitebox and v0.5 Repo Safety are planned but not implemented in v0.3.
- GitHub tag/release publication was approved as part of the v0.3.0 closeout.

## UAT Result

```text
Pass - approved by Owner on 2026-08-19.
通过 - Owner 于 2026-08-19 批准。
```

## Verification

Codex should run:

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

## GitHub

```text
Tag: v0.3.0
Release: https://github.com/adwasd-dvd/ai-project-os/releases/tag/v0.3.0
PRs: Release PR created from `codex/release-v0.3.0`
CI: Not applicable for Markdown-only package; validator passed locally
Release asset: releases/ai-project-os-v0.3.0.zip
```
