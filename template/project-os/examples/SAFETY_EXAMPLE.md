# SAFETY_EXAMPLE

This fictional example shows how a small team classifies files, scans safely, recovers missing project memory, and prepares a public release.

本虚构示例展示小团队如何分类文件、安全扫描、恢复缺失项目记忆并准备公开发布。

## Scenario / 场景

Acme Notes started as one person's Codex experiment. A second developer joined, and the team now wants to publish the core library.

Acme Notes 最初是一个人的 Codex 实验。第二名开发者加入后，团队准备公开核心库。

Repository evidence:

```text
.env                         real local credentials
.env.example                 placeholder key names
AGENTS.md                    stable shared build/test rules
notes/private-plan.md        unreleased commercial plan
project-os/LOCAL_OVERRIDES.md contains a user home path
docs/architecture.md         intended public architecture summary
old-chat-summary.md          sanitized claim with no Decision record
```

No real value is copied into the reports.

报告中不复制任何真实值。

## Step 1: Classify / 分类

| Artifact | Classification | Reason | Destination |
|---|---|---|---|
| `.env` | Local Only | Real credentials | Excluded from Git |
| `.env.example` | Public Safe after review | Names and placeholders only | Public repo |
| `AGENTS.md` | Team Shared, then Public Safe after sanitization | Stable contributor rules | Public repo after public review |
| `notes/private-plan.md` | Private Repo | Commercial context | Excluded from public release |
| `LOCAL_OVERRIDES.md` | Private Repo | Project/user-specific path | Excluded or sanitized |
| `docs/architecture.md` | Public Safe | Approved generic design | Public repo |
| `old-chat-summary.md` | Private Repo | Unverified Chat Only claim | Keep private until Decision |

## Step 2: Run Local Review / 本地检查

```bash
python3 project-os/tools/safety_scan.py --root . --scope worktree --profile local --summary
```

Expected sanitized result:

```text
Block: 0
Review: secret-like path and chat-only path findings
No matched values or source lines emitted
```

The scanner reports `.env` and a rule ID, not the credential.

Scanner 只报告 `.env` 和规则 ID，不报告凭证。

## Step 3: Recover Project Memory / 恢复项目记忆

`safety/PROJECT_MEMORY_AUDIT.md` records:

| Finding ID | Claim | State | Evidence | Confidence | Next Verification |
|---|---|---|---|---|---|
| MEM-001 | Public release excludes commercial roadmap | Claimed / Chat Only | Sanitized old chat summary | Low | Owner Decision |
| MEM-002 | Library has no production-data dependency | Observed | Code and tests | High | Run integration test |
| MEM-003 | AGENTS.md is canonical | Contradicted | AGENTS.md and CLAUDE.md differ | Medium | DEC-ACME-002 |

`safety/DOC_GAP_REGISTER.md` creates:

| Gap ID | Type | Description | Impact | Route |
|---|---|---|---|---|
| GAP-001 | Chat Only | Public/private scope exists only in old conversation | High | Decision |
| GAP-002 | Contradicted | Agent files disagree about release command | High | Decision + docs fix |

## Step 4: Resolve Agent Docs / 处理 Agent 文档

The team chooses `AGENTS.md` as canonical. `CLAUDE.md` becomes a short wrapper pointing to it. User-specific paths are removed from public instructions.

团队选择 `AGENTS.md` 作为规范来源。`CLAUDE.md` 变为指向它的简短 wrapper。公开指令中移除用户路径。

## Step 5: Stage And Gate / 暂存并门禁

```bash
git add <approved paths>
python3 project-os/tools/safety_scan.py \
  --root . \
  --scope staged \
  --profile private \
  --fail-on-block \
  --summary
```

If `.env` was staged, the result is Block. The output contains only:

```text
Rule: SAF001
Path: .env
Classification: Local Only
Remediation: remove from the proposed destination and rotate if exposed
```

## Step 6: Public Manifest / 公开清单

The publication manifest excludes `.env`, private plan, local overrides, detailed audit history, and the chat summary. It includes source, tests, public docs, sanitized Agent guidance, and `.env.example`.

Publication manifest 排除 `.env`、私有计划、本地 override、详细 audit 历史和聊天摘要；包含源码、测试、公开文档、脱敏 Agent 指南和 `.env.example`。

## Step 7: Public Gate / 公开门禁

```bash
python3 project-os/tools/safety_scan.py \
  --root . \
  --scope tracked \
  --profile public \
  --fail-on-block \
  --summary
```

Review findings for Agent docs and project memory require human conclusions. Zero Block findings alone is not public approval.

Agent 文档和项目记忆的 Review finding 需要人类结论。Block 为零不等于已经批准公开。

## Final Result / 最终结果

```text
Secret values emitted: No
Raw conversations copied: No
Block findings: 0
Review findings: resolved by Owner
Manifest decision: Go
Public approval: explicit human approval
```

The project becomes easier to share without pretending that a scanner alone proved it safe.

项目变得更容易共享，但不会假装 scanner 单独就证明了项目绝对安全。
