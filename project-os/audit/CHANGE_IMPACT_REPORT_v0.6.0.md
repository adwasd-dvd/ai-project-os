# Change Impact Report / 变更影响报告

Feature ID: `AIPOS-044`
Target Version: `v0.6.0`
Development Gate: `READY`

## Gate Findings / 门禁发现

- No structural blocker found. / 未发现结构性阻塞。

## Impact Matrix / 影响矩阵

| Area | Level | Confidence | Claim | Evidence | Next Verification |
|---|---|---|---|---|---|
| modules | high | high | Train A changes core Linear intake, automation, workflow, quality, and release-governance modules. | DEC-009 and DVD-219 through DVD-225 explicitly define the combined Train A scope. | Review the final diff and traceability matrix before UAT handoff. |
| dependencies | medium | high | The executable tools add no third-party runtime dependency but the live runner depends on Linear GraphQL availability and schema compatibility. | Both tools import only Python standard-library modules; the Linear endpoint and error contract are documented by Linear. | Run py_compile, offline tests, and one authorized live dry scan before human UAT. |
| data_security | high | high | Live scans process issue descriptions/comments and require a Linear token, so config, reports, and receipts must preserve the secret and project-memory boundary. | The token is environment-only; runtime files are ignored; the ledger omits body and token values; write operations use allowlists and runtime authorization. | Run focused ledger tests and staged/private safety scan; inspect generated runtime files locally only. |
| documentation | high | high | The new tools affect startup, daily Linear operation, development readiness, PR review, UAT, and version cadence documentation. | Core rules now link AUTOMATION_RUNBOOK, CHANGE_IMPACT, and TRACEABILITY into START_HERE, AGENTS, WORKFLOW, QUALITY_GATE, and UAT_TEMPLATE. | Run strict validator and complete the non-engineering Owner walkthrough in UAT. |
| tests | high | high | Automation safety and evidence-state claims require deterministic tests, not documentation-only assertions. | Focused tests cover routing, bilingual output, credentials, write gates, idempotency, partial failure, trace states, evidence paths, and impact blockers. | Run the full source suite and the extracted candidate-package suite. |
| uat | high | high | Only a human can confirm that the report, setup, queue routing, write boundary, and traceability matrix are understandable and useful. | DEC-009 requires one consolidated Train A human UAT and release policy forbids Codex self-acceptance. | Owner completes project-os/audit/UAT_v0.6.0.md and explicitly passes or fails. |
| rollout_rollback | medium | high | Train A ships as a versioned GitHub Release asset; rollback restores v0.5.0 while preserving runtime state and project-specific audit memory. | Version planning and release policy keep generated zip assets out of source and require human UAT before tag/release. | Verify candidate zip, digest, extracted validation, Draft PR, and documented v0.5.0 rollback path. |

## Test Impact / 测试影响

- Run py_compile for both new tools.
- Run all Python unit tests, including intake and traceability suites.
- Run the deterministic offline fixture twice and compare outputs.
- Run strict source/template validation.
- Run private staged safety gate and inspect public tracked advisory.
- Build the v0.6.0 candidate zip, extract it, validate it, and run its tests.

## Human UAT Impact / 人工 UAT 影响

- Owner runs or reviews the fixture queues and bilingual summary.
- Owner confirms the live dry-run credential/setup path is understandable.
- Owner confirms scheduled scans cannot modify local product code.
- Owner reviews the triple write gate and sanitized ledger boundary.
- Owner uses the impact and traceability reports to explain what is ready, pending, and not yet released.

## Delivery / 交付

- Rollout: After explicit v0.6.0 UAT Pass, merge the Draft PR, tag the merge commit, publish the verified zip and digest, then close Linear issues/project.
- Rollback: Before release, discard the candidate branch. After release, reinstall the v0.5.0 package from its GitHub Release while preserving LOCAL_OVERRIDES, audit history, runtime config/ledger, and project-specific safety decisions.

Tests and UAT are intentionally separate. / 测试与人工 UAT 明确分开。
