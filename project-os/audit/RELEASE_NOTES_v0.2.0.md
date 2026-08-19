# Release v0.2.0

Release notes for AI Project OS v0.2.0.

Human UAT passed on 2026-08-19. This is the local OS package closeout record.

人类 UAT 已于 2026-08-19 通过。本文件是本地 OS 包的关账记录。

## Summary

AI Project OS v0.2.0 turns the initial audit/import lazy pack into a day-to-day Linear-driven operating loop.

AI Project OS v0.2.0 把最初的 audit/import 懒人包升级为可以日常使用的 Linear 驱动协作流程。

## Included Features

| Feature ID | Linear | Summary |
|---|---|---|
| AIPOS-009 | DVD-16 | Lightweight validator for required files, key policy gates, template drift, and release zip shape |
| AIPOS-010 | DVD-17 | Worked first-project walkthrough from Phase 0 through Linear import, UAT, and carry-over |
| AIPOS-011 | DVD-19 | Linear follow-up automation design with manual/scheduled boundaries and no automatic code execution |
| AIPOS-012 | DVD-20 | Requirement and issue management workflow for idea/requirement/feature/bug/decision/backlog classification |
| AIPOS-013 | DVD-21 | Version planning and staged delivery workflow, including patch and next-version handling |
| AIPOS-014 | DVD-22 | Linear-driven Codex handoff prompt library for checking Linear, starting work, UAT, rework, and release prep |
| AIPOS-015 | DVD-24 | Linear intake scan and inconsistency guardrails across active issues and versions |
| AIPOS-016 | DVD-25 | Cron-ready intake runner contract with dry-run defaults, safe modes, and idempotency |
| AIPOS-017 | DVD-26 | Bilingual Linear output policy for comments, status updates, UAT notes, decisions, and run summaries |
| AIPOS-018 | DVD-27 | Version closeout and carry-over revalidation workflow for old-version feedback |

## Fixed Bugs

No product-code bugs. v0.2 addresses process misses found during v0.1/v0.2 Linear grooming:

- Broad Linear scans must include active/recent older-version feedback.
- Codex-authored Linear output must be bilingual by default.
- Old-version completed issues with next-version feedback must use carry-over revalidation instead of direct movement.

## Known Limitations

- v0.2 defines cron/scheduled Linear intake behavior, but does not implement unattended local code execution.
- Generated zip artifacts are local release assets and are ignored by Git unless published separately.
- GitHub tag/release creation was deferred for this local closeout; publish separately if needed.

## UAT Result

```text
Pass.
通过。
```

Owner approval recorded from conversation on 2026-08-19:

```text
可以按照你的建议往前做吧。
```

## Verification

Codex ran:

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

## GitHub

```text
Tag: Deferred for local closeout
PRs: Pending / not created in this local closeout
CI: Not applicable for Markdown-only package; validator passed locally
Release asset: releases/ai-project-os-v0.2.0.zip
```
