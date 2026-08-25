# Release v0.6.0

Release notes for AI Project OS v0.6.0 Development Train A.

AI Project OS v0.6.0 Development Train A 发布说明。

## Summary / 摘要

v0.6 turns the documented Linear intake loop into an executable, dry-run-first runner and adds a durable requirement-to-release evidence chain. It can scan current and adjacent projects, route work by status + assignee, preserve old-version feedback, prepare safe advisory actions, and execute only explicitly authorized idempotent Linear writes. It also blocks development when change impact is incomplete and prevents automated tests from being mistaken for human UAT.

v0.6 把文档化的 Linear intake 变成可执行、默认 dry-run 的 runner，并增加持久的需求到 release 证据链。它能扫描当前与相邻版本 Project，按 status + assignee 路由，保留旧版本反馈，准备安全 advisory 动作，并且只执行明确授权的幂等 Linear 写入。它还会在 change impact 不完整时阻塞开发，并防止把自动测试误当成人工 UAT。

## Included Features / 包含功能

| Feature ID | Linear | Summary |
|---|---|---|
| DEC-009 | DVD-218 | Three large development trains with one formal UAT each |
| AIPOS-038 | DVD-219 | Manual/scheduled Linear intake config and standard-library runner |
| AIPOS-039 | DVD-220 | Queue routing, Ready checks, feedback classification, and cross-version scope |
| AIPOS-040 | DVD-221 | Triple write gate, idempotency, freshness, retry, partial failure, and sanitized ledger |
| AIPOS-041 | DVD-222 | Manual, cron-compatible, and Codex recurring operations runbook |
| AIPOS-042 | DVD-223 | Requirement-to-release traceability manifest and validator |
| AIPOS-043 | DVD-224 | Seven-area change-impact gate and evidence report |
| AIPOS-044 | DVD-225 | Validator, tests, worked example, package, Draft PR, and consolidated UAT |

## What Users Get / 用户得到什么

- A deterministic offline fixture and live Linear GraphQL read path.
- Current/adjacent project resolution plus explicit issue inclusion.
- Codex Queue, Human Queue, Review Queue, inconsistent, blocked, and Closed Watch routing.
- Feature ID, target version, acceptance criteria, blocking relation, and Decision checks.
- Bilingual JSON/Markdown reports with scan scope, scanned, created, updated, skipped, blockers, and next action.
- Separate scan and apply commands.
- Config allowlist + CLI authorization + runtime authorization.
- Stable local/remote idempotency markers, plan freshness, incomplete-scan blocking, bounded retry, and sanitized receipts.
- Manual, cron-compatible, and Codex recurring setup.
- Change-impact and traceability tools with deterministic reports.

## Known Limitations / 已知限制

- A personal API key or OAuth token is required for the standalone live runner. This development environment did not contain `LINEAR_API_KEY`; human UAT owns the live credential test.
- The default planner emits advisory comments only. Issue updates and issue creation require an explicitly reviewed plan and narrow allowlist.
- Polling is project-scoped and bounded. Incomplete scope or a reached issue cap blocks apply. Higher scale should use Linear webhooks.
- The runner does not modify local product code, approve Decisions/scope/UAT, merge PRs, tag, or release.
- Traceability verifies declared evidence structure; it does not prove the business truth of a human claim.

## Verification / 验证

```text
Change-impact gate: READY
Traceability state: released; structural validation passed
Automated tests: 38/38 passed in source and extracted deterministic package
Strict validator: 0 failures, 0 warnings in source and extracted package
Final tracked private safety: Block 0, Review 0
Final tracked public advisory: Block 0; 40 expected audit/Agent publication-classification review items
Deterministic zip/extracted package: two delayed builds byte-identical; archive, validation, and tests passed
Remote release asset: downloaded and byte-identical to the local artifact
Human UAT: Pass - Owner approved 2026-08-25
```

## GitHub

```text
Release commit: a3076d69793ee62ff0c758018984f1b201cc32bb
Implementation PR: https://github.com/adwasd-dvd/ai-project-os/pull/4
Deterministic packaging PR: https://github.com/adwasd-dvd/ai-project-os/pull/5
Tag: v0.6.0
Release: https://github.com/adwasd-dvd/ai-project-os/releases/tag/v0.6.0
Release asset: ai-project-os-v0.6.0.zip
Release SHA-256: 565e81b722ddba1b02514c2a8485e2f831332125428f2ae7284f55be3c45639b
```
