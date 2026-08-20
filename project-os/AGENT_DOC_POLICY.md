# AGENT_DOC_POLICY

This policy decides when AI/Agent instruction files should stay local or enter Git.

本政策决定 AI/Agent 指令文件何时应留在本地，何时可以进入 Git。

## Core Rule / 核心规则

```text
Commit stable shared operating rules.
Keep personal memory, raw prompts, credentials, and machine-specific context local.
Use one canonical source; tool-specific wrappers may point to it but may not silently override it.
```

## Project Modes / 项目模式

| Mode | Default | Commit Agent Docs? |
|---|---|---|
| Single user | Local context stays local | Only if the file is useful project documentation, not personal memory |
| Small trusted team | Share stable rules through one canonical file | Yes, after private/team safety review |
| Large organization | Canonical rules plus owned tool wrappers | Yes, with review ownership and change control |
| Public repository | Generic contributor instructions only | Yes, only after public-profile sanitization |

## Canonical Source / 规范来源

Recommended authority order:

1. `project-os/AGENTS.md` for AI Project OS operating rules.
2. `project-os/PROJECT.md` for project-level operating facts.
3. `project-os/LOCAL_OVERRIDES.md` for project-specific overrides, classified before commit.
4. Tool wrappers such as `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md` only when the tool needs a repository-root entry point.

Wrappers should point to the canonical source and contain only the minimum tool-specific difference.

Wrapper 应指向规范来源，并只保留最少的工具差异。

## Allowed Shared Content / 可共享内容

- stable build/test commands;
- repository-relative paths;
- coding and review rules;
- approved architecture boundaries;
- handoff and UAT process;
- non-secret environment key names;
- safety and publication gates;
- links to tagged, authorized evidence.

## Local-Only Content / 仅本地内容

- real credentials, cookies, tokens, private keys, and connection strings;
- raw conversation transcripts or copied personal prompts;
- user home paths, device names, private email, or unrelated identity data;
- private scratch notes and unapproved hypotheses;
- production records, customer data, or sensitive screenshots;
- hidden instructions intended to bypass team policy or human review.

## Review Triggers / 复核触发器

Review an Agent document before commit/share when it contains:

- absolute paths such as `/Users/...`, `/home/...`, or `C:\\Users\\...`;
- internal URLs, account identifiers, organization names, or commercial facts;
- copied issue/comment/chat content rather than a stable decision summary;
- instructions that conflict with `AGENTS.md`, safety policy, or human UAT;
- commands that publish, delete, rotate credentials, rewrite history, or access production;
- claims without evidence, owner, or freshness.

## Single-User Pattern / 单人模式

Use the installed `project-os/` as the stable system. Keep personal preferences outside Git or in a local-only override. Do not create extra Agent files just to mirror the same instructions.

使用安装的 `project-os/` 作为稳定系统。个人偏好留在 Git 外或仅本地 override 中。不要为了重复同样指令而创建额外 Agent 文件。

## Team Pattern / 团队模式

1. Choose one canonical instruction source.
2. Assign an owner and review path.
3. Keep shared rules short, stable, and testable.
4. Put project decisions in Decision records, not hidden Agent prose.
5. Use tool wrappers only for discovery/compatibility.
6. Run the team/private safety profile before commit.

## Public Pattern / 公开模式

Public Agent docs must:

- work without private accounts or internal links;
- avoid company-private assumptions;
- use sanitized examples;
- disclose no hidden credentials or private operational topology;
- clearly separate contributor guidance from local maintainer memory;
- pass the public safety profile and human review.

## Conflict Rule / 冲突规则

If two Agent documents disagree:

1. mark the conflict in `safety/DOC_GAP_REGISTER.md`;
2. identify authority and owner;
3. stop affected work if the conflict changes safety, scope, release, or data handling;
4. resolve through a Decision;
5. update or remove the weaker wrapper.

Never let a tool-specific wrapper silently override project safety or human UAT.

不得让工具 wrapper 静默覆盖项目安全政策或人类 UAT。
