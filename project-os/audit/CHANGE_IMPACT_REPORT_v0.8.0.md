# Change Impact Report / 变更影响报告

Feature ID: `AIPOS-051`
Target Version: `v0.8.0`
Development Gate: `READY`

## Gate Findings / 门禁发现

- No structural blocker found. / 未发现结构性阻塞。

## Impact Matrix / 影响矩阵

| Area | Level | Confidence | Claim | Evidence | Next Verification |
|---|---|---|---|---|---|
| modules | high | high | Train B changes release governance, UAT evidence, recovery, upgrade discovery, upgrade planning, guarded apply, validation, packaging, and traceability. | DEC-009 and the approved roadmap explicitly combine former v0.8 and v0.9 into one v0.8.0 train. | Review the final Train B diff and feature-to-evidence matrix before UAT handoff. |
| dependencies | medium | high | New tools remain Python standard-library only; optional upstream discovery depends on local packages or configured GitHub release metadata, while offline fixtures cover the same contract. | The existing package and automation tools use standard-library-only implementations and fail closed around unavailable external systems. | Run compile checks, dependency inspection, offline fixtures, and an optional read-only GitHub metadata check. |
| data_security | high | high | Upgrade planning compares project-specific files and may encounter private audit, runtime, or Agent context, so reports must contain hashes/classifications rather than raw private content and apply must be path-confined. | Existing safety policies classify local, team, private, and public artifacts and prohibit output of matched values or source content. | Test protected paths, traversal refusal, sanitized reports/receipts, and run private staged plus public tracked safety scans. |
| documentation | high | high | Release, rollback, upgrade, startup, quality gates, UAT, examples, and operator prompts must describe the new inspect-plan-approve-apply-verify lifecycle consistently. | The current roadmap and UPGRADE_POLICY define the intended behavior but do not yet provide executable Train B controls. | Run strict validator and an Owner walkthrough of release and upgrade quick paths. |
| tests | high | high | Release-state and file-migration safety claims require deterministic offline tests for evidence gates, conflicts, freshness, authorization, path confinement, idempotency, preservation, package extraction, and failure recovery. | Train A established focused unit tests, strict validation, deterministic packaging, and extracted-package verification as release evidence. | Run focused release/upgrade suites, the complete source suite, delayed package comparison, and the complete extracted-package suite. |
| uat | high | high | Only the Owner can confirm that lifecycle wording, release readiness, recovery guidance, conflict explanations, preservation behavior, and upgrade controls are understandable and trustworthy. | DEC-009 requires one consolidated Train B UAT and RELEASE_POLICY forbids Codex self-acceptance. | Prepare a bilingual v0.8.0 UAT with explicit actions and expected results, then stop for the Owner conclusion. |
| rollout_rollback | high | high | Train B changes the mechanism that plans OS upgrades and release recovery, so rollout must be branch-based and rollback must preserve the last accepted package plus project-specific memory without destructive automation. | The existing release policy uses immutable GitHub tags/assets and UPGRADE_POLICY lists files that must never be overwritten automatically. | Dogfood an isolated older-to-candidate upgrade, simulate verification failure, verify protected hashes, and inspect rollback guidance before UAT. |

## Test Impact / 测试影响

- Compile all source and template Python tools.
- Run focused lifecycle/release readiness tests and focused upgrade planner/apply tests.
- Test missing UAT/safety/package/rollback evidence and contradictory release states.
- Test version comparison, identical/upstream/local/both-modified files, protected paths, traversal, stale plans, authorization, idempotency, and verification failure.
- Dogfood an older packaged OS to the v0.8.0 candidate in an isolated temporary repository.
- Run strict source/template validation and private/public safety gates.
- Build two delayed deterministic packages, extract one, and run the full extracted-package suite.

## Human UAT Impact / 人工 UAT 影响

- Owner distinguishes code complete, review complete, UAT Pass, released, and post-release done from generated evidence.
- Owner reviews a READY release plan and at least one BLOCKED plan with a clear next action.
- Owner follows rollback/hotfix/post-release guidance and confirms no destructive action is automatic.
- Owner reviews installed/upstream version discovery and an upgrade conflict report.
- Owner verifies LOCAL_OVERRIDES, audit/Linear records, safety dispositions, and private/runtime context survive the dogfood upgrade.
- Owner gives an explicit pass or fail conclusion for v0.8.0.

## Delivery / 交付

- Rollout: Implement on codex/v0.8-train-b, keep all remote/destructive operations manual, prepare a Draft PR and deterministic candidate package, then stop for explicit v0.8.0 human UAT before merge, tag, or Release.
- Rollback: Before release, abandon the Train B branch. After release, reinstall the immutable v0.6.0 package or the latest accepted package on a new branch while preserving LOCAL_OVERRIDES, audit history, Linear mappings, safety dispositions, runtime/private context, and human UAT records.

Tests and UAT are intentionally separate. / 测试与人工 UAT 明确分开。
