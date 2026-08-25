# Linear Intake Automation

This directory contains portable, non-secret inputs for `tools/linear_intake.py`.

本目录保存 `tools/linear_intake.py` 的可移植、非秘密输入。

## Files

- `linear_intake.example.json`: safe default configuration; writes disabled.
- `fixtures/train_a_snapshot.json`: deterministic offline routing fixture.
- Runtime config, reports, and ledger belong in `project-os/runtime/` and stay out of Git.

## Commands

Dry-run fixture:

```bash
python3 project-os/tools/linear_intake.py --root . scan \
  --config project-os/automation/linear_intake.example.json \
  --snapshot project-os/automation/fixtures/train_a_snapshot.json \
  --as-of 2026-08-24T18:00:00Z
```

Live dry-run and guarded apply are documented in `AUTOMATION_RUNBOOK.md`.

实时 dry-run 与受控 apply 见 `AUTOMATION_RUNBOOK.md`。

## Snapshot Contract

An offline snapshot is a JSON object containing `schema_version`, `team`, and `issues`. Each issue may include:

```text
id
identifier
title
description
status
assignee
project
labels
updated_at
completed_at
blocked_by
comments[]
```

Offline snapshots must not contain secret values. Comments are used for local classification but are never copied into the run ledger.

离线快照不得包含 secret 值。评论可用于本地分类，但不会复制到运行账本。

## Planned Action Contract

Supported operation names:

```text
comment_create
issue_update
issue_create
```

Support does not equal permission. Each operation must also be allowlisted in local config, executed through the apply command, and authorized at runtime.

“支持”不等于“允许”。操作还必须进入本地配置白名单，通过 apply 命令执行，并有运行时授权。
