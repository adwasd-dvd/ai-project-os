# AI Project OS

AI Project OS is a local Codex operating manual for taking over software projects, organizing them in Linear, executing development locally with Codex, and preserving code/release facts in GitHub.

This repository is the source project for the OS itself.

## 60-Second Start

1. Download the latest zip from [GitHub Releases](https://github.com/adwasd-dvd/ai-project-os/releases/latest).
2. Extract the top-level `project-os/` directory into your project root.
3. Open that project in Codex and send:

```text
请读取 project-os/START_HERE.md，并按 AI Project OS 工作。
先检查当前项目状态。
如果这是成熟或混乱项目，先执行 Phase 0.5 Whitebox Discovery 和 Phase 0.75 Safety Classification。
Linear 默认使用 English + Chinese。
只问真正阻塞的问题；其余按安全默认值继续。
先告诉我发现、风险和下一步，然后开始执行。
```

Expected path: `your-project/project-os/START_HERE.md`.

Full quickstart: [`project-os/QUICKSTART.md`](project-os/QUICKSTART.md).

## Repository Layout

```text
ai-project-os/
├── README.md
├── OS_VERSION.md
├── CHANGELOG.md
├── UPGRADE_POLICY.md
├── LOCAL_OVERRIDES.md
├── template/project-os/   # distributable lazy pack for other repositories
├── project-os/            # AI Project OS installed to manage this repo itself
└── releases/              # generated zip artifacts, not source of truth
```

## How This Project Manages Itself

This repository uses AI Project OS to manage AI Project OS development.

- `template/project-os/` is the product being built.
- `project-os/` is the installed OS instance for this source repository.
- `project-os/audit/` contains this repository's own self-check, baseline, inventory, risks, and Linear import plan.
- `project-os/discovery/` contains this repository's own evidence-backed whitebox maps.
- Linear will manage roadmap, issues, decisions, and UAT.
- GitHub will hold the private source repository, PRs, tags, and release facts.

## Current Development Rule

No formal development should happen without:

- Feature ID.
- Target version.
- Clear acceptance criteria.
- No unresolved blocking Decision.

## First Learning Flow

1. Keep this repo private.
2. Push this repo to a private GitHub repository.
3. Create a Linear project for the current AI Project OS version.
4. Import the confirmed Feature inventory into Linear.
5. Use one issue at a time to improve the OS.
6. Use UAT before any formal OS release.

## Build / Package

The distributable package is created from `template/project-os/`.

Recommended artifact name:

```text
ai-project-os-v0.8.0.zip
```

Generated zip files stay out of Git history. Versioned packages are published as GitHub Release assets so other projects can install an exact OS version without copying this repository's dogfood audit history.

Release packages are built from committed template content with fixed archive metadata:

```bash
python3 project-os/tools/build_release.py --root . \
  --output releases/ai-project-os-v0.8.0.zip
```

Repeated builds from the same commit must be byte-identical and produce the same SHA-256.

## Use In Another Project

1. Download `ai-project-os-v0.8.0.zip` from the [v0.8.0 GitHub Release](https://github.com/adwasd-dvd/ai-project-os/releases/tag/v0.8.0).
2. Extract the top-level `project-os/` directory into the target repository root.
3. Open Codex in that repository and ask it to read `project-os/START_HERE.md` before doing project work.

Use a tagged release instead of copying files from a development branch. This keeps each target project pinned to a known OS version and makes later upgrades auditable.

## Latest Stable: v0.8.0

v0.8 adds explicit release/recovery control and safe OS self-upgrade on top of the v0.6 Linear automation and traceability foundation.

Core outputs:

- Deterministic release readiness, notes, feedback classification, rollback guidance, and post-release verification.
- Installed/upstream OS version discovery and deterministic three-way upgrade planning.
- Guarded branch-based upgrade apply with protected project-memory preservation.
- Dry-run-first Linear intake, status + assignee routing, and idempotent authorized writes.
- Seven-area change-impact gates and requirement-to-release traceability.

v0.8.0 passed human UAT on 2026-08-26. Use the tagged GitHub Release for installations in other projects.

## Next Planned: v1.0.0 Internal Stable

v1.0 targets the internal stable rescue standard for mature, messy projects.

Planned focus:

- end-to-end project rescue from black-box discovery through managed release;
- proactive project-manager guidance for non-engineering owners;
- contradiction, security-boundary, and documentation-gap handling;
- one canonical Linear Project with version Milestones for AI Project OS itself.

## v0.3 Handoff Rule

v0.3 makes the daily Linear workflow easier to operate by using assignee as the basic Human/Codex handoff signal:

```text
Assigned = human queue
Unassigned = Codex queue
Status = lifecycle
Labels = classification only, optional for advanced workflows
```

Added focus:

- Human/Codex handoff policy for single-user Linear boards.
- Linear intake routing by status + assignee.
- UAT and prompt playbooks for passing, failing, or handing work back to Codex.
- Roadmap through v1.0, where the success standard is rescuing and governing a messy mature project.
- Validator guardrails so `next:*` labels stay optional in the basic workflow.

## Important

Do not edit `template/project-os/audit/*.md` with project-specific audit results. Those files are template output specifications for repositories that install the OS.

This repository's own audit output belongs in:

```text
project-os/audit/
```
