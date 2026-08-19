# WHITEBOX_EXAMPLE

This fictional example shows how to whitebox a mature project without turning guesses into facts.

本虚构示例展示如何白盒化成熟项目，同时不把猜测写成事实。

## Scenario / 场景

`Acme Orders` is a five-year-old order service. The original team left. README says it is a single Node.js API, but the repository also contains a worker, Python scripts, PostgreSQL migrations, and an undocumented payment webhook.

`Acme Orders` 是一个五年的订单服务。原团队已离开。README 声称它是单一 Node.js API，但仓库里还有 worker、Python 脚本、PostgreSQL migration 和未记录的支付 webhook。

The goal is not to fix the service yet. The goal is to make its shape, evidence, contradictions, and next questions visible.

当前目标不是修复服务，而是让它的形态、证据、矛盾和下一步问题可见。

## 1. Mechanical Scan / 机械扫描

Command:

```bash
python3 project-os/tools/whitebox_scan.py --root . --write
```

Selected safe output:

```text
Languages: TypeScript 84, SQL 17, Python 6
Manifests: package.json, tools/requirements.txt
Lockfiles: pnpm-lock.yaml
Likely entrypoints: src/server.ts, src/worker.ts
Data candidates: db/migrations/*, fixtures/*
Environment key names: DATABASE_URL, PAYMENT_WEBHOOK_KEY, QUEUE_NAME
Secret values emitted: No
```

This output proves that the paths and declarations exist. It does not prove what they do.

该输出只证明路径和声明存在，不证明它们的实际用途。

## 2. Project Map Findings / 项目地图发现

| Finding ID | Claim | State | Evidence | Confidence | Unknowns | Next Verification |
|---|---|---|---|---|---|---|
| PM-001 | The repository contains an HTTP API and a background worker | Observed | `src/server.ts`, `src/worker.ts`, `package.json` scripts | High | Whether both deploy in production | Inspect deployment definitions and ask current operator |
| PM-002 | Python scripts are part of the production order flow | Inferred | `tools/reconcile.py`; no CI or deploy reference found | Low | Whether scripts are manual, obsolete, or scheduled | Check Git history and operations runbook |
| PM-003 | README describes the complete runtime shape | Contradicted | README says "single API"; worker entrypoint and queue config exist | Medium | Whether README is stale or worker is unused | Inspect deployment and runtime process list in a non-production environment |

Notice that PM-003 keeps both sources. It does not silently decide that README or code is correct.

注意 PM-003 保留了两个来源，没有静默决定 README 或代码哪个正确。

## 3. Dependency Map Findings / 依赖地图发现

| Dependency | Scope | Purpose | Evidence | State | Confidence | Next Verification |
|---|---|---|---|---|---|---|
| `fastify` | Runtime | HTTP API framework | `package.json`, imports in `src/server.ts` | Observed | High | Run existing API tests |
| `bullmq` | Runtime | Queue worker | `package.json`, `src/worker.ts` | Observed | High | Confirm Redis deployment and failure behavior |
| `stripe` | Runtime | Payment integration | `package.json`, `src/payments/webhook.ts` | Observed | High | Confirm webhook contract and idempotency tests |
| `pandas` | Tooling or unknown | Reconciliation script | `tools/requirements.txt`, `tools/reconcile.py` | Observed declaration, inferred purpose | Medium | Ask whether script is operationally required |

## 4. Document Inventory Findings / 文档清单发现

| Document | Purpose | Authority | Claims Checked Against | State | Confidence | Gap or Contradiction |
|---|---|---|---|---|---|---|
| `README.md` | Setup and architecture | Supporting | package scripts, entrypoints, deployment files | Contradicted | Medium | Omits worker and payment webhook |
| `docs/api.md` | Public API | Unknown | route registration | Claimed | Low | Last relevant commit is two years old |
| `docs/runbook.md` | Operations | Supporting | CI and scripts | Claimed | Medium | No rollback instructions |

Chat-only claim:

| Claim | Source | Persisted | State | Confidence | Next Action |
|---|---|---|---|---|---|
| "The reconciliation script runs every night" | Former operator chat | No | Claimed | Low | Find scheduler evidence or create a Decision asking whether it is still required |

## 5. Settings and Data Findings / 设置与数据发现

| Setting Name | Purpose | Source | Sensitive Claim | State | Confidence | Unknowns |
|---|---|---|---|---|---|---|
| `DATABASE_URL` | PostgreSQL connection | `.env.example`, database client initialization | Secret | Observed name only | High | Ownership and rotation process |
| `PAYMENT_WEBHOOK_KEY` | Webhook verification | `.env.example`, webhook handler | Secret | Observed name only | High | Rotation and environment ownership |
| `QUEUE_NAME` | Worker queue selection | `.env.example`, worker startup | Sensitive / Unknown | Observed name only | High | Whether multiple queues exist |

No values are copied.

不复制任何值。

Data store finding:

| Finding ID | Claim | State | Evidence | Confidence | Unknowns | Next Verification |
|---|---|---|---|---|---|---|
| SD-001 | PostgreSQL stores orders and payment attempts | Observed | migrations and repository queries | High | Retention and deletion policy | Ask Owner and inspect privacy documentation |
| SD-002 | Redis queue retry state can be rebuilt safely | Unknown | No recovery documentation or test found | Unknown | Data-loss and duplicate-order impact | Create verification issue before changing worker behavior |

## 6. Logic and Boundary Findings / 逻辑与边界发现

| Finding ID | Type | Claim | State | Impact | Evidence | Confidence | Next Verification | Disposition |
|---|---|---|---|---|---|---|---|---|
| LOG-001 | Business invariant | Paid orders must not return to pending | Claimed | High | `docs/api.md`; no matching test found | Low | Trace payment state transitions and add a characterization test proposal | Decision + test Feature |
| LOG-002 | Trust boundary | Payment webhook verifies signatures before parsing business events | Observed | Critical | `src/payments/webhook.ts` call order | High | Run existing invalid-signature tests | Keep evidence; route deep security review to v0.5 |
| LOG-003 | Contradiction | Worker retries are both 3 and 10 | Contradicted | High | `docs/runbook.md` says 3; code config says 10 | Medium | Confirm production config and desired business rule | Decision |
| LOG-004 | Error gap | Reconciliation failure ownership is known | Unknown | Medium | No alert owner or runbook section found | Unknown | Ask operations Owner | Backlog or Feature after confirmation |

## 7. Whitebox Import Proposal / 白盒导入建议

### Proposed Decision

```text
Decision ID: DEC-ORDER-001
Question: What is the approved worker retry count?
Context: Runbook says 3; active code default says 10.
Options: Keep 3, keep 10, make environment-specific with documented limits.
Recommendation: Confirm business duplicate-processing tolerance before changing code.
Impact: Order latency and duplicate side-effect risk.
Owner: Product + Operations
Blocking: Any retry-policy change.
```

### Proposed Verification Feature

```text
Feature ID: ORDER-041
Type: Chore / characterization
Title: Verify paid-order state invariant and current retry behavior
Target Version: Next planned version
Action Steps:
1. Trace payment state transitions.
2. Add characterization tests without changing behavior.
3. Compare test evidence with docs and runtime configuration.
Expected Result:
The Owner can decide the intended invariant and retry policy from reproducible evidence.
Acceptance Criteria:
- Tests show current behavior.
- No production behavior changes.
- DEC-ORDER-001 links the evidence.
```

### Linear Project Description Summary

```markdown
## Project Whitebox / 项目白盒

Evidence freshness / 证据更新: <date + commit>

System shape / 系统形态: Node.js HTTP API + queue worker + PostgreSQL; Python reconciliation role remains unverified. / Node.js HTTP API + queue worker + PostgreSQL；Python reconciliation 用途尚未验证。

Confidence / 置信度: High for repository topology; low for scheduled operations and retry intent. / 仓库拓扑置信度高；定时运维与 retry 意图置信度低。

Contradictions / 矛盾:
- LOG-003: retry count 3 vs 10; requires DEC-ORDER-001.

Unknowns / 未知项:
- PM-002: whether Python reconciliation is active.
- SD-002: whether queue retry state is recoverable.

Next verification / 下一步验证: ORDER-041 characterizes current behavior without changing production logic. / ORDER-041 在不改生产逻辑的情况下固化当前行为。
```

## 8. Human Review / 人工 Review

The human does not need to approve every low-impact unknown before baseline confirmation. The human must confirm that coverage limits are honest and that high-impact contradictions are resolved or routed.

人类不需在 baseline 确认前解决所有低影响未知项。人类必须确认覆盖限制是诚实的，且高影响矛盾已解决或已路由。

```text
Coverage accepted: Yes
High-impact contradiction routed: Yes, DEC-ORDER-001
Unknown operations ownership accepted as a gap: Yes
Baseline ready for confirmation: Yes
Linear first bulk write approved: Not yet
```
