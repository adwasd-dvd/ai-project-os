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
Merged PR: https://github.com/adwasd-dvd/ai-project-os/pull/9
Merge Commit: 48a0c3a12154d5c1aeee1c12d0c241b6d5ae9bfc
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
| Root README and stable-release links | Public Safe | Current private GitHub source | Yes | v1.0.0 is latest stable |
| `template/project-os/` | Public Safe | GitHub source + Release zip | Yes | Standalone distributable |
| `project-os/` generic policies/tools | Team Shared | GitHub source | Yes | Dogfood installation |
| `project-os/audit/` v1.0 evidence | Private Repo | Current private GitHub source | Yes | Sanitized summaries and hashes only |
| Rescue runtime output and protected file contents | Local Only | None | No | Never copied into Git or publication evidence |
| Release zip | Public Safe | GitHub Release asset | Release only | Never commit to source |

## Required Evidence

```text
Change Impact: READY
Traceability: released / post-release PASS
Source: strict validator clean; 73/73 tests pass
Messy-Project Fixture: representative combined certification passes
Real Repository Dogfood: deterministic; verify PASS; product/external writes 0
Real Mature Project UAT: two OS defects found and fixed; final safety Block 0; deterministic rescue verify PASS
Package: two builds byte-identical; extracted validator clean; 73/73 tests pass
Accepted Package Commit: 817cae8
Accepted Package SHA-256: 6dcec2eae38af467ec68062a5e18be1171152af558578b03323f7a5be1cfdd99
Human UAT: Pass; accepted by dvdTeacher / Owner on 2026-08-26
GitHub Merged PR: https://github.com/adwasd-dvd/ai-project-os/pull/9
GitHub Release: https://github.com/adwasd-dvd/ai-project-os/releases/tag/v1.0.0
Remote Asset Verification: 275400 bytes; byte-identical; SHA-256 matches
Linear UAT Handoff: Project update 676ec315-ac91-4bdb-8c7c-e549e02f24ae
Linear Real-Project UAT Update: Project update 86556cc0-6c6e-4c0d-821e-8b300c5e3fb9
Linear Owner UAT Pass Update: Project update ade71b54-fc15-4cbb-8482-66dccea5cf82
Linear Release Closeout Update: Project update dfa0aa13-f7b9-46b6-b4ac-cb18e1dfcfb3
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

Published and verified. PR #9 merged at `48a0c3a`; tag `v1.0.0` and the non-draft, non-prerelease GitHub Release are published. The remote asset is byte-identical to the accepted local package and all SHA-256 evidence matches. Post-release verification is PASS.

已发布并核验。PR #9 已合并到 `48a0c3a`；`v1.0.0` tag 与非草稿、非预发布 GitHub Release 已发布。远端资产与已验收本地安装包逐字节一致，全部 SHA-256 证据一致；发布后验证为 PASS。
