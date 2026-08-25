# Change Impact Report / 变更影响报告

Feature ID: `DEMO-001`
Target Version: `v0.1.0`
Development Gate: `READY`

## Gate Findings / 门禁发现

- No structural blocker found. / 未发现结构性阻塞。

## Impact Matrix / 影响矩阵

| Area | Level | Confidence | Claim | Evidence | Next Verification |
|---|---|---|---|---|---|
| modules | low | high | The example changes only project operating documentation. | Feature scope names the documentation module. | Review the final diff before development completes. |
| dependencies | low | high | No runtime dependency is added. | The planned output is Markdown and JSON. | Run the dependency inventory after implementation. |
| data_security | low | high | No production data or secret value is required. | Examples use placeholders only. | Run the target publication safety gate. |
| documentation | medium | high | Operator instructions must be updated with the feature workflow. | The feature changes an operator-facing process. | Review QUICKSTART and START_HERE for discoverability. |
| tests | medium | high | Validation needs deterministic fixture coverage. | The expected output is machine-verifiable. | Run the focused automated tests. |
| uat | medium | high | A human must confirm the workflow is understandable. | Automated tests cannot establish human usability. | Record explicit Owner pass or fail. |
| rollout_rollback | low | high | Delivery uses a versioned package and can revert to the prior tag. | Release policy pins installable packages to tags. | Verify the candidate zip and rollback note. |

## Test Impact / 测试影响

- Run the strict project validator.
- Run focused deterministic tests.

## Human UAT Impact / 人工 UAT 影响

- Owner follows the feature workflow and records pass or fail.

## Delivery / 交付

- Rollout: Ship through a human-approved tagged release.
- Rollback: Restore the prior tagged package and preserve local project memory.

Tests and UAT are intentionally separate. / 测试与人工 UAT 明确分开。
