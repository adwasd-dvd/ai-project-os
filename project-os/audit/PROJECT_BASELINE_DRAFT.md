# PROJECT_BASELINE_DRAFT

## Audit Metadata

```text
Audit Date: 2026-08-18
Codex Session: initial AI Project OS source setup
Repository: ai-project-os
Branch: main
Commit: 64d6504
Auditor: Codex
Status: Draft
```

## Executive Summary

- This repository is the source project for AI Project OS v0.1.0.
- The product is a distributable `project-os/` lazy pack for local Codex projects.
- The repository also installs AI Project OS into itself under root `project-os/`.
- The distributable template lives under `template/project-os/`.
- The project is Markdown/documentation-only at v0.1.0.
- No runtime dependencies are required.
- GitHub CLI is available and authenticated as `adwasd-dvd`.
- Linear tools are installed but the Linear app is not connected in this Codex session.
- Private GitHub repository exists at `https://github.com/adwasd-dvd/ai-project-os`.
- First Linear bulk import requires human approval.

## Repository Overview

```text
Project Name: AI Project OS
Primary Language: Markdown
Frameworks: None
Package Manager: None
Runtime: None
Database: None
External Services: GitHub, Linear
Deployment: zip package / private GitHub release
CI: Not configured
Test Framework: Manual policy/file inventory checks
```

## Areas Read

| Area | Path / Source | What Was Found | Confidence |
|---|---|---|---|
| OS template | `template/project-os/` | Distributable lazy pack source | High |
| Self-management OS | `project-os/` | Installed OS instance for this repo | High |
| Root governance | `README.md`, `OS_VERSION.md`, `UPGRADE_POLICY.md` | Source repo rules | High |
| GitHub auth | local `gh auth status` | Logged in as `adwasd-dvd` | High |
| Linear tools | Codex Linear tools | Installed but returned `USER_NOT_LOGGED_IN` | High |

## Areas Not Read

| Area | Reason | Risk |
|---|---|---|
| GitHub remote repo | Created and private | Push is working |
| Linear existing project | Linear app not connected yet | Duplicate preflight pending |
| CI | Not configured | No automated validation yet |

## Current Product Understanding

AI Project OS is a project operating manual for local Codex. It helps a team take over a codebase, audit current state, organize work in Linear, execute development locally, preserve code facts in GitHub, and require human UAT for each formal version.

## Current Technical Understanding

The project is currently a documentation/template repository. It does not ship executable code. Its main build artifact is a zip of `template/project-os/`.

## Known Entry Points

| Type | Path / Command | Notes |
|---|---|---|
| Start Here | `template/project-os/START_HERE.md` | User-facing install/start instructions |
| Self Check | `template/project-os/SELF_CHECK.md` | Phase 0 entry |
| Package | `cd template && zip -r ../releases/ai-project-os-v0.1.0.zip project-os` | Generates distributable zip |
| Test | manual inventory | Automated validator is a v0.2 candidate |

## Main Risks

- Linear app connection and team/project selection are not yet confirmed.
- GitHub private repo exists and is verified private.
- No automated policy validator exists.
- Template and self-installed OS can drift if updates are not managed.

## Main Unknowns

- Which Linear team should own this project, after Linear app connection.
- Whether GitHub Releases should host generated zip artifacts.
- Whether release zip files should be stored only as GitHub Releases or also tracked locally.

## Human Confirmation Needed

- [x] Confirm GitHub repo owner/name: `adwasd-dvd/ai-project-os`.
- [ ] Confirm Linear team.
- [ ] Approve first Linear import.
- [ ] Confirm v0.1.0 scope.

## Codex Phase 1 Completion Statement

```text
Phase 1 Audit is complete for the AI Project OS source project.
No product code was modified.
No Linear writes were performed.
The project is in a private GitHub repo and is ready for Linear import after Linear connection and human approval.
```
