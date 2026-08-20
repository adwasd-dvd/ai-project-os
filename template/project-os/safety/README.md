# SAFETY OUTPUTS

This directory holds project-specific v0.5 safety and project-memory outputs.

本目录保存项目自己的 v0.5 安全和项目记忆产物。

## Files

| File | Purpose |
|---|---|
| `PUBLICATION_MANIFEST.md` | Destination, included/excluded artifacts, evidence, and Go/Review/Block decision |
| `PROJECT_MEMORY_AUDIT.md` | Authority, freshness, conflicts, chat-only claims, and continuity risk |
| `DOC_GAP_REGISTER.md` | Missing, stale, orphaned, duplicated, or disputed knowledge |
| `SECRET_SCAN_REPORT.md` | Sanitized human summary of scanner evidence and remediation |
| `SAFETY_EVIDENCE.json` | Optional deterministic machine evidence generated with `--write` |

## Safety Rule

Reports may contain repository-relative paths, rule IDs, classifications, counts, evidence freshness, and remediation.

Reports must not contain matched secret values, source lines containing secrets, environment values, private keys, raw production data, or raw conversation dumps.

报告可包含仓库相对路径、规则 ID、分类、数量、证据新鲜度和修复动作。

报告不得包含命中的 secret 值、含 secret 的源码行、环境变量值、私钥、原始生产数据或原始聊天转储。

## Commands

Read-only worktree review:

```bash
python3 project-os/tools/safety_scan.py --root . --summary
```

Staged private-repo gate:

```bash
python3 project-os/tools/safety_scan.py --root . --scope staged --profile private --fail-on-block --summary
```

Tracked public-publication gate:

```bash
python3 project-os/tools/safety_scan.py --root . --scope tracked --profile public --fail-on-block --summary
```

Write deterministic evidence:

```bash
python3 project-os/tools/safety_scan.py --root . --profile private --write
python3 project-os/tools/safety_scan.py --root . --profile private --check
```

`--write` may only write `SAFETY_EVIDENCE.json` under the selected repository-internal output directory.

## Human Ownership

Codex may prepare and classify findings. A human approves public publication, credential response, history rewriting, repository visibility changes, and final UAT.
