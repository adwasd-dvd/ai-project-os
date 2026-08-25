# PUBLICATION_MANIFEST v0.6.0 Approved

This is the release-specific publication approval for AI Project OS v0.6.0 Development Train A.

本文件是 AI Project OS v0.6.0 Development Train A 的版本专用发布批准记录。

## Header

```text
Manifest ID: AIPOS-PUB-v0.6.0
Prepared Date: 2026-08-24
Prepared By: Codex
Destination Profile: private
Repository / Channel: GitHub repository + GitHub Release
Repository Visibility: PRIVATE; verified before publication
Commit / Tag: PR #4; tag v0.6.0 authorized after human UAT
Release Asset: ai-project-os-v0.6.0.zip
Human Approver: dvdTeacher / Owner
Decision: Go for the current PRIVATE GitHub destination
```

## Scope

```text
Purpose: Publish the approved v0.6 automation and traceability release.
Audience: AI-assisted project owners, operators, and maintainers.
Included Paths: Source changes; distributable template/project-os/ in release zip.
Excluded Paths: Runtime config/ledger, tokens, raw Linear exports, raw conversations, local generated evidence, and zip from Git source history.
Generated Artifact Source: template/project-os/
Rollback Location: v0.5.0 GitHub tag and Release.
```

## Artifact Classification

| Artifact / Path | Classification | Destination | Evidence | Included? | Notes |
|---|---|---|---|---|---|
| Root README and stable-release links | Public Safe | Private GitHub source | human review + validator | Yes | Latest stable becomes v0.6.0 with publication |
| `template/project-os/` | Public Safe candidate | Private GitHub + future Release zip | standalone validation | Yes | Product distribution source |
| `project-os/` generic policies/tools | Team Shared | Private GitHub source | source/template drift check | Yes | Dogfood installation |
| `project-os/audit/` Train A evidence | Private Repo | Private GitHub source | safety scan + human review | Yes | No raw Linear body export or token |
| `project-os/runtime/` generated files | Local Only | None | nested `.gitignore` + policy | No | Config, reports, ledger, logs |
| `LINEAR_API_KEY` / OAuth token | Local Only secret | Process environment only | credential boundary | No | Never write value to repo/Linear/report |
| `releases/ai-project-os-v0.6.0.zip` | Public Safe candidate | Future GitHub Release asset | archive + extracted validation | Release only | Never commit zip to source |

## Required Evidence

```text
Strict Validator: source and extracted package both 0 failures, 0 warnings
Automated Tests: source 38/38 pass; extracted deterministic package 38/38 pass
Change Impact: READY
Traceability: accepted, structural PASS
Safety Scan: private staged Block 0 / Review 0; public staged Block 0 / 13 expected publication-review items
UAT: Pass - Owner approved 2026-08-25
Archive / Artifact: two delayed builds byte-identical; SHA-256 565e81b722ddba1b02514c2a8485e2f831332125428f2ae7284f55be3c45639b
PR: https://github.com/adwasd-dvd/ai-project-os/pull/4
Remote Asset Digest: pending publication verification
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
Decision: Go for current private destination
Blocking Conditions: none before the authorized release transaction
Approved By: dvdTeacher / Owner
Approved Date: 2026-08-25
Post-Publication Verification: compare uploaded asset SHA-256, tag, README stable link, traceability release state, and Linear closeout
Rollback Trigger: digest mismatch, Block finding, live runner safety failure, traceability failure, package validation failure, or human UAT failure
```

The Owner explicitly approved v0.6.0 UAT and the current private publication destination.

Owner 已明确批准 v0.6.0 UAT 和当前 private 发布目标。
