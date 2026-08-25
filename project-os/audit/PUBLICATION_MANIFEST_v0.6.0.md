# PUBLICATION_MANIFEST v0.6.0 Candidate

This is the release-specific publication review for AI Project OS v0.6.0 Development Train A.

本文件是 AI Project OS v0.6.0 Development Train A 的版本专用发布审查记录。

## Header

```text
Manifest ID: AIPOS-PUB-v0.6.0
Prepared Date: 2026-08-24
Prepared By: Codex
Destination Profile: private
Repository / Channel: GitHub repository + future GitHub Release
Repository Visibility: PRIVATE; reverify before publication
Commit / Tag: Draft PR candidate; no tag before human UAT
Release Asset: ai-project-os-v0.6.0.zip candidate
Human Approver: dvdTeacher / Owner
Decision: Review - blocked on human UAT and final release verification
```

## Scope

```text
Purpose: Review the v0.6 automation and traceability candidate.
Audience: AI-assisted project owners, operators, and maintainers.
Included Paths: Source changes; distributable template/project-os/ in release zip.
Excluded Paths: Runtime config/ledger, tokens, raw Linear exports, raw conversations, local generated evidence, and zip from Git source history.
Generated Artifact Source: template/project-os/
Rollback Location: v0.5.0 GitHub tag and Release.
```

## Artifact Classification

| Artifact / Path | Classification | Destination | Evidence | Included? | Notes |
|---|---|---|---|---|---|
| Root README and stable-release links | Public Safe candidate | Private GitHub source | human review + validator | Yes | Latest stable remains v0.5.0 before UAT |
| `template/project-os/` | Public Safe candidate | Private GitHub + future Release zip | standalone validation | Yes | Product distribution source |
| `project-os/` generic policies/tools | Team Shared | Private GitHub source | source/template drift check | Yes | Dogfood installation |
| `project-os/audit/` Train A evidence | Private Repo | Private GitHub source | safety scan + human review | Yes | No raw Linear body export or token |
| `project-os/runtime/` generated files | Local Only | None | nested `.gitignore` + policy | No | Config, reports, ledger, logs |
| `LINEAR_API_KEY` / OAuth token | Local Only secret | Process environment only | credential boundary | No | Never write value to repo/Linear/report |
| `releases/ai-project-os-v0.6.0.zip` | Public Safe candidate | Future GitHub Release asset | archive + extracted validation | Release only | Never commit zip to source |

## Required Evidence

```text
Strict Validator: source and extracted package both 0 failures, 0 warnings
Automated Tests: source 36/36 pass; extracted package 36/36 pass
Change Impact: READY
Traceability: uat_pending, structural PASS
Safety Scan: private staged Block 0 / Review 0; public staged Block 0 / 13 expected publication-review items
UAT: Pending Human
Archive / Artifact: valid; SHA-256 c453e8732a4b77907055ebb82fb980a864201a7ffefd090d3ac2f95a4c65f217
Draft PR: pending
Remote Asset Digest: N/A before release
```

## Automation Data Boundary

```text
Committed Example Config: placeholders only; writes disabled
Committed Fixture: synthetic issues/comments only
Runtime Config: Local Only under project-os/runtime/
Runtime Ledger: sanitized operation/target/status/attempt/result/time only
Token Values: not committed, logged, copied to issue, or stored in ledger
Raw Live Snapshot: not committed by default
Scheduled Code Modification: forbidden
```

## Go / Review / Block

```text
Decision: Review
Blocking Conditions: Draft PR evidence and explicit human UAT Pass
Approved By: Pending
Approved Date: Pending
Post-Publication Verification: compare uploaded asset SHA-256, tag, README stable link, traceability release state, and Linear closeout
Rollback Trigger: digest mismatch, Block finding, live runner safety failure, traceability failure, package validation failure, or human UAT failure
```

Only the Owner can change this candidate from `Review` to `Go` by explicitly passing v0.6.0 UAT.

只有 Owner 明确通过 v0.6.0 UAT，才能把本候选从 `Review` 改为 `Go`。
