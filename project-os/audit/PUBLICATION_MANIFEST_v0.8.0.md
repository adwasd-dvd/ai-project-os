# PUBLICATION MANIFEST v0.8.0

This is the release-specific publication review for AI Project OS v0.8.0 Development Train B.

本文件是 AI Project OS v0.8.0 Development Train B 的版本专用发布复核记录。

## Header

```text
Manifest ID: AIPOS-PUB-v0.8.0
Prepared Date: 2026-08-25
Prepared By: Codex
Destination Profile: private
Repository / Channel: current private GitHub repository + GitHub Release
Repository Visibility: must be re-verified immediately before publication
Candidate Commit: 6ea9e8fe4b004f415c530a118f9f28fa02931e11
Release Asset: ai-project-os-v0.8.0.zip
Human Approver: Pending
Decision: Review - pending explicit v0.8.0 UAT and publication approval
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
| Root README and stable-release links | Public Safe | Current private GitHub source | Yes | Remains v0.6.0 until authorized release |
| `template/project-os/` | Public Safe | GitHub source + Release zip | Yes | Standalone distributable |
| `project-os/` generic policies/tools | Team Shared | GitHub source | Yes | Dogfood installation |
| `project-os/audit/` Train B evidence | Private Repo | Current private GitHub source | Yes | Summaries and hashes only |
| Dogfood protected file contents | Local Only | None | No | Never copied into evidence |
| `project-os/runtime/` generated receipts | Local Only | None | No | Ignored runtime state |
| Release zip | Public Safe | GitHub Release asset | Release only | Never commit to source |

## Required Evidence

```text
Change Impact: READY
Traceability: candidate / UAT pending / structural PASS
Source: strict validator clean; 59/59 tests pass
Package: two builds byte-identical; extracted validator clean; 59/59 tests pass
Dogfood: v0.6.0 to v0.8.0 apply, restart, and verify pass
Protected Memory: four before/after SHA-256 values byte-identical
Candidate SHA-256: ec81d2439a4802fc19e1d03cc3a9b7bd739c7c92cd37af4134385d016bd3df92
Human UAT: Pending
GitHub Draft PR: https://github.com/adwasd-dvd/ai-project-os/pull/7
Linear UAT Handoff: project update 8ef6411d-303b-4eb4-b5ff-31d3ab2bbc64
```

## Go / Review / Block

```text
Decision: Review
Block Findings: 0 in the isolated private dogfood gate
Review Findings: 0 in the isolated private dogfood gate
Remaining Human Gates: consolidated v0.8.0 UAT; publication approval; final destination visibility check
Approved By: Pending
Approved Date: Pending
Rollback Trigger: digest mismatch, verification failure, safety Block, unresolved upgrade conflict, UAT failure, or post-release failure
```

Codex may prepare and verify the candidate. Only the Owner may change this decision to Go and authorize merge, tag, and GitHub Release.

Codex 可以准备并验证候选版。只有 Owner 可以把决定改为 Go，并授权合并、tag 和 GitHub Release。
