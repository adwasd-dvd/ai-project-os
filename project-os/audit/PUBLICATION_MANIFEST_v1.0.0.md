# PUBLICATION MANIFEST v1.0.0

This is the release-specific publication review for AI Project OS v1.0.0 Internal Stable Rescue.

本文件是 AI Project OS v1.0.0 内部稳定救援版的版本专用发布复核记录。

## Header

```text
Manifest ID: AIPOS-PUB-v1.0.0
Prepared Date: 2026-08-26
Prepared By: Codex
Destination Profile: private
Repository / Channel: current private GitHub repository + GitHub Release
Repository Visibility: PRIVATE; verified during candidate preparation
Initial Functional Candidate Commit: c6317fa
Real-Project UAT Fix Commit: 544cd32
Draft PR: https://github.com/adwasd-dvd/ai-project-os/pull/9
Release Asset: ai-project-os-v1.0.0.zip
Human Approver: dvdTeacher / Owner
Decision: Go - Owner UAT passed and publication is authorized
```

## Scope

```text
Purpose: Publish the internal-stable mature-project rescue workflow and certification.
Audience: AI-assisted project owners, operators, and maintainers.
Included Paths: reviewed source changes; distributable template/project-os/ in the Release zip.
Excluded Paths: runtime config/receipts, credentials, protected dogfood content, raw Linear exports, raw conversations, and zip from Git source history.
Generated Artifact Source: template/project-os/
Rollback Location: immutable v0.8.0 GitHub tag and Release.
```

## Artifact Classification

| Artifact / Path | Classification | Destination | Included? | Notes |
|---|---|---|---|---|
| Root README and stable-release links | Public Safe | Current private GitHub source | Yes | Switch to v1.0.0 in the authorized release transaction |
| `template/project-os/` | Public Safe | GitHub source + Release zip | Yes | Standalone distributable |
| `project-os/` generic policies/tools | Team Shared | GitHub source | Yes | Dogfood installation |
| `project-os/audit/` v1.0 evidence | Private Repo | Current private GitHub source | Yes | Sanitized summaries and hashes only |
| Rescue runtime output and protected file contents | Local Only | None | No | Never copied into Git or publication evidence |
| Release zip | Public Safe | GitHub Release asset | Release only | Never commit to source |

## Required Evidence

```text
Change Impact: READY
Traceability: candidate / accepted / PASS
Source: strict validator clean; 73/73 tests pass
Messy-Project Fixture: representative combined certification passes
Real Repository Dogfood: deterministic; verify PASS; product/external writes 0
Real Mature Project UAT: two OS defects found and fixed; final safety Block 0; deterministic rescue verify PASS
Package: two builds byte-identical; extracted validator clean; 73/73 tests pass
Current Candidate SHA-256: e86be5ebaa9670d4a41717132b2754e5d49302fac319cc2094d8b772e21f2f2e
Human UAT: Pass; accepted by dvdTeacher / Owner on 2026-08-26
GitHub Draft PR: https://github.com/adwasd-dvd/ai-project-os/pull/9
Linear UAT Handoff: Project update 676ec315-ac91-4bdb-8c7c-e549e02f24ae
Linear Real-Project UAT Update: Project update 86556cc0-6c6e-4c0d-821e-8b300c5e3fb9
```

## Go / Review / Block

```text
Decision: Go
Safety Block Findings: 0 in the isolated private candidate gate
Safety Review Findings: 0 in the isolated private candidate gate
Remaining Human Gates: None for the authorized v1.0.0 release transaction
Approved By: dvdTeacher / Owner
Approved Date: 2026-08-26
Rollback Trigger: digest mismatch, verification failure, safety Block, unresolved rescue contradiction, UAT failure, or post-release failure
```

The Owner said `UAT 通过，允许发布 v1.0.0` and then confirmed `好的 继续发布`. Merge, tag, GitHub Release, and stable-link updates are authorized subject to the recorded verification gates.

Owner 已明确说 `UAT 通过，允许发布 v1.0.0`，并再次确认 `好的 继续发布`。在已记录的验证门禁持续通过的前提下，merge、tag、GitHub Release 和稳定版入口更新均已获授权。

## Publication Result / 发布结果

Authorized but not yet published. Draft PR #9 is ready to leave Draft; v0.8.0 remains the remote stable release until the transaction completes.

已授权但尚未发布。Draft PR #9 可以离开 Draft；在发布事务完成前，远端 latest stable 仍为 v0.8.0。
