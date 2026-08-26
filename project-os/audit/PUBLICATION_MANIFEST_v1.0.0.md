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
Functional Candidate Source Commit: c6317fa
Candidate Branch Verification Commit: 2fa9d6f
Draft PR: https://github.com/adwasd-dvd/ai-project-os/pull/9
Release Asset: ai-project-os-v1.0.0.zip
Human Approver: dvdTeacher / Owner
Decision: Review - candidate is ready for Owner UAT; publication is not authorized
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
| Root README and stable-release links | Public Safe | Current private GitHub source | After approval | Keep v0.8.0 stable until release transaction |
| `template/project-os/` | Public Safe | GitHub source + Release zip | Yes | Standalone distributable |
| `project-os/` generic policies/tools | Team Shared | GitHub source | Yes | Dogfood installation |
| `project-os/audit/` v1.0 evidence | Private Repo | Current private GitHub source | Yes | Sanitized summaries and hashes only |
| Rescue runtime output and protected file contents | Local Only | None | No | Never copied into Git or publication evidence |
| Release zip | Public Safe | GitHub Release asset | Release only | Never commit to source |

## Required Evidence

```text
Change Impact: READY
Traceability: candidate / uat_pending / structural PASS
Source: strict validator clean; 72/72 tests pass
Messy-Project Fixture: representative combined certification passes
Real Repository Dogfood: deterministic; verify PASS; product/external writes 0
Package: two delayed builds byte-identical; extracted validator clean; 72/72 tests pass
Functional Candidate SHA-256: e8926363aec753dc613a7bde2df2f5906106e778c4b769432c84419328f8094e
Human UAT: Pending
GitHub Draft PR: https://github.com/adwasd-dvd/ai-project-os/pull/9
Linear UAT Handoff: Project update 676ec315-ac91-4bdb-8c7c-e549e02f24ae
```

## Go / Review / Block

```text
Decision: Review
Safety Block Findings: 0 in the isolated private candidate gate
Safety Review Findings: 0 in the isolated private candidate gate
Remaining Human Gates: consolidated v1.0.0 Owner UAT and explicit publication authorization
Approved By: Pending
Approved Date: Pending
Rollback Trigger: digest mismatch, verification failure, safety Block, unresolved rescue contradiction, UAT failure, or post-release failure
```

The private candidate is safe to review, but merge, tag, GitHub Release, and stable-link updates remain blocked until the Owner says `UAT 通过，允许发布 v1.0.0。`.

private 候选可以开始审查，但 merge、tag、GitHub Release 和 stable 链接更新继续阻塞，直到 Owner 明确说 `UAT 通过，允许发布 v1.0.0。`。

## Publication Result / 发布结果

Not published. Draft PR #9 is the current review surface and v0.8.0 remains the latest stable release.

尚未发布。Draft PR #9 是当前审查入口，v0.8.0 继续作为 latest stable release。
