# AI Project OS

AI Project OS is a local Codex operating manual for taking over software projects, organizing them in Linear, executing development locally with Codex, and preserving code/release facts in GitHub.

This repository is the source project for the OS itself.

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
ai-project-os-v0.4.0.zip
```

Generated zip files stay out of Git history. Versioned packages are published as GitHub Release assets so other projects can install an exact OS version without copying this repository's dogfood audit history.

## Use In Another Project

1. Download `ai-project-os-v0.3.0.zip` from the [v0.3.0 GitHub Release](https://github.com/adwasd-dvd/ai-project-os/releases/tag/v0.3.0).
2. Extract the top-level `project-os/` directory into the target repository root.
3. Open Codex in that repository and ask it to read `project-os/START_HERE.md` before doing project work.

Use a tagged release instead of copying files from a development branch. This keeps each target project pinned to a known OS version and makes later upgrades auditable.

## Current Development: v0.4

v0.4 adds Project Whitebox for taking over mature black-box or gray-box repositories before baseline confirmation.

Core outputs:

- A read-only-by-default repository scanner that emits paths and safe declaration names, never secret values.
- Project, dependency, document, settings/data, and logic/boundary maps.
- Evidence states: Observed, Derived, Claimed, Inferred, Contradicted, and Unknown.
- Confidence levels and required next verification for important findings.
- A compact bilingual Linear project summary backed by detailed GitHub/local evidence.
- Validator and tests that keep source and distributable templates aligned.

The latest stable install remains v0.3.0 until v0.4.0 passes human UAT and is published as a GitHub Release.

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
