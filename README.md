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
3. Create a Linear project for `AI Project OS v0.1`.
4. Import the confirmed Feature inventory into Linear.
5. Use one issue at a time to improve the OS.
6. Use UAT before any formal OS release.

## Build / Package

The distributable package is created from `template/project-os/`.

Recommended artifact name:

```text
ai-project-os-v0.1.0.zip
```

## Important

Do not edit `template/project-os/audit/*.md` with project-specific audit results. Those files are template output specifications for repositories that install the OS.

This repository's own audit output belongs in:

```text
project-os/audit/
```

