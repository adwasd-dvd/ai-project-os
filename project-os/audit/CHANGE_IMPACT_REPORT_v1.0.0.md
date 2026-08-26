# Change Impact Report / 变更影响报告

Feature ID: `AIPOS-059`
Target Version: `v1.0.0`
Development Gate: `READY`

## Gate Findings / 门禁发现

- No structural blocker found. / 未发现结构性阻塞。

## Impact Matrix / 影响矩阵

| Area | Level | Confidence | Claim | Evidence | Next Verification |
|---|---|---|---|---|---|
| modules | high | high | v1.0 adds an end-to-end rescue orchestrator that composes whitebox, safety, diagnosis, recovery planning, Linear import preparation, proactive PM routing, and release evidence. | The approved v1.0 success standard requires a messy mature project to become understandable and manageable end to end. | Review the final AIPOS-052 through AIPOS-059 feature-to-code and feature-to-evidence matrix. |
| dependencies | medium | high | The rescue workflow remains Python standard-library only and composes existing local scanners without installing project dependencies or accessing production. | Existing whitebox, safety, traceability, release, and upgrade tools use standard-library implementations with offline fixtures. | Compile every source/template tool and run rescue fixtures in an isolated temporary repository. |
| data_security | high | high | Rescue evidence may identify credentials, private project memory, settings, data boundaries, and contradictions, so outputs must stay sanitized, path-confined, and free of raw values or source lines. | SECURITY_BOUNDARY and the existing scanners prohibit matched values, source lines, environment values, and file contents in evidence. | Test secret-bearing fixtures, output traversal, OS-self exclusion, forbidden input fields, and deterministic sanitized receipts. |
| documentation | high | high | Startup, rescue protocol, workflow, quality gates, Linear handoff, examples, and operator prompts must present one coherent rescue path in English and Chinese. | START_HERE currently requires users to manually sequence several phases and tools. | Run strict validator and review the installed-package 60-second rescue path. |
| tests | high | high | The v1.0 success standard requires deterministic end-to-end tests for messy project evidence, routing, safety blocking, idempotent reruns, output freshness, and one-Project Linear drafts. | Train A and Train B established focused unit tests, deterministic packages, extracted-package tests, and real workflow dogfood as release gates. | Run focused rescue tests, the full source suite, deterministic package comparison, and the full extracted-package suite. |
| uat | high | high | Only the Owner can judge whether the generated diagnosis, risks, roadmap, ownership queues, and next action make a previously messy project controllable. | The v1.0 success standard is an end-to-end human outcome and AI Project OS forbids self-acceptance. | Prepare one bilingual v1.0 UAT with explicit actions and expected results, then stop for Owner approval. |
| rollout_rollback | high | high | Rescue planning must be read-only for product code and external systems by default; generated OS evidence must be branch-reviewable and removable without altering project behavior. | Existing policies require inspect-plan-approve boundaries, branch-based changes, protected memory, and human-controlled external writes and releases. | Dogfood in isolated and real repositories, verify reruns are harmless, and confirm abandoning the branch removes only generated OS evidence. |

## Test Impact / 测试影响

- Compile all source and template Python tools.
- Test dry-run inspection, authorized local plan writes, deterministic reruns, and stale-output verification.
- Test OS-owned path exclusion so product evidence is not dominated by the installed OS package.
- Test safety blocks, contradictions, missing target version, missing dependencies/tests/docs/CI, and human gate routing.
- Test bilingual one-Project Linear draft records with Action Steps, Expected Result, Milestone, duplicate keys, and no remote mutation.
- Run the full source suite, strict validator, staged/private safety gate, deterministic package build, and extracted-package suite.

## Human UAT Impact / 人工 UAT 影响

- Owner runs one rescue command in a representative messy mature project.
- Owner verifies that diagnosis separates evidence, confidence, impact, contradictions, unknowns, and next verification.
- Owner verifies that the recovery roadmap says what humans and Codex do next and what proves completion.
- Owner verifies that the Linear package targets one Project and one Milestone and remains dry-run before approval.
- Owner verifies that no secret value, source line, production action, external write, business Decision, UAT approval, or release happens automatically.
- Owner gives an explicit pass or fail conclusion for v1.0.0.

## Delivery / 交付

- Rollout: Implement on codex/v1.0-internal-stable, keep rescue product/external operations read-only, dogfood and package through a Draft PR, then stop for explicit v1.0.0 Owner UAT before merge, tag, or Release.
- Rollback: Before release, abandon the v1.0 branch or remove generated rescue evidence. After release, reinstall immutable v0.8.0 on a dedicated branch while preserving local overrides, audit/Linear history, safety dispositions, discovery evidence, and private runtime context.

Tests and UAT are intentionally separate. / 测试与人工 UAT 明确分开。
