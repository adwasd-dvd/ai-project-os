# PUBLICATION MANIFEST v0.8.0

This is the release-specific publication review for AI Project OS v0.8.0 Development Train B.

本文件是 AI Project OS v0.8.0 Development Train B 的版本专用发布复核记录。

## Header

```text
Manifest ID: AIPOS-PUB-v0.8.0
Prepared Date: 2026-08-26
Prepared By: Codex
Destination Profile: private
Repository / Channel: current private GitHub repository + GitHub Release
Repository Visibility: PRIVATE; verified before the authorized release transaction
Final Package Source Commit: 2a93fdc
Merged Release Commit: 4cd2412f06f7fe1e368c1efafa862bd62f560a4e
Release Asset: ai-project-os-v0.8.0.zip
Human Approver: dvdTeacher / Owner
Decision: Go - Owner passed v0.8.0 UAT and authorized the current private GitHub publication transaction
```

## Scope

```text
Purpose: Publish approved release/recovery and safe self-upgrade controls.
Audience: AI-assisted project owners, operators, and maintainers.
Included Paths: reviewed source changes; distributable template/project-os/ in the Release zip.
Excluded Paths: runtime config/receipts, credentials, protected dogfood content, raw Linear exports, raw conversations, and zip from Git source history.
Generated Artifact Source: template/project-os/
Rollback Location: immutable v0.6.0 GitHub tag and Release.
```

## Artifact Classification

| Artifact / Path | Classification | Destination | Included? | Notes |
|---|---|---|---|---|
| Root README and stable-release links | Public Safe | Current private GitHub source | Yes | Update to v0.8.0 during the authorized release transaction |
| `template/project-os/` | Public Safe | GitHub source + Release zip | Yes | Standalone distributable |
| `project-os/` generic policies/tools | Team Shared | GitHub source | Yes | Dogfood installation |
| `project-os/audit/` Train B evidence | Private Repo | Current private GitHub source | Yes | Summaries and hashes only |
| Dogfood protected file contents | Local Only | None | No | Never copied into evidence |
| `project-os/runtime/` generated receipts | Local Only | None | No | Ignored runtime state |
| Release zip | Public Safe | GitHub Release asset | Release only | Never commit to source |

## Required Evidence

```text
Change Impact: READY
Traceability: candidate / accepted / structural PASS
Source: strict validator clean; 59/59 tests pass
Package: two builds byte-identical; extracted validator clean; 59/59 tests pass
Dogfood: v0.6.0 to v0.8.0 apply, restart, and verify pass
Protected Memory: four before/after SHA-256 values byte-identical
Accepted Functional Candidate SHA-256: ec81d2439a4802fc19e1d03cc3a9b7bd739c7c92cd37af4134385d016bd3df92
Final Release Package SHA-256: cf9989b993b28689da367d532db233a6d369a8edbe041712951ddc5e99cdfc1f
Human UAT: Pass - Owner approved 2026-08-26
GitHub Draft PR: https://github.com/adwasd-dvd/ai-project-os/pull/7
Linear UAT Handoff: project update 8ef6411d-303b-4eb4-b5ff-31d3ab2bbc64
GitHub Release: https://github.com/adwasd-dvd/ai-project-os/releases/tag/v0.8.0
Remote Asset Verification: byte-identical; SHA-256 cf9989b993b28689da367d532db233a6d369a8edbe041712951ddc5e99cdfc1f
Post-Release Receipt: project-os/audit/POST_RELEASE_RECEIPT_v0.8.0.md - PASS
```

## Go / Review / Block

```text
Decision: Go
Block Findings: 0 in the isolated private dogfood gate
Review Findings: 0 in the isolated private dogfood gate
Remaining Human Gates: none
Approved By: dvdTeacher / Owner
Approved Date: 2026-08-26
Rollback Trigger: digest mismatch, verification failure, safety Block, unresolved upgrade conflict, UAT failure, or post-release failure
```

The Owner explicitly passed v0.8.0 UAT and authorized merge, tag, and GitHub Release to the verified private destination.

Owner 已明确通过 v0.8.0 UAT，并授权向已验证的 private 目标执行合并、tag 和 GitHub Release。

## Publication Result / 发布结果

PR #7 was merged, tag `v0.8.0` was pushed to merge commit `4cd2412f06f7fe1e368c1efafa862bd62f560a4e`, and the GitHub Release asset was published. The downloaded asset is byte-identical to the local package and post-release verification passed.

PR #7 已合并，tag `v0.8.0` 已指向合并提交 `4cd2412f06f7fe1e368c1efafa862bd62f560a4e`，GitHub Release 资产已发布。远端下载资产与本地安装包逐字节一致，发布后验证通过。
