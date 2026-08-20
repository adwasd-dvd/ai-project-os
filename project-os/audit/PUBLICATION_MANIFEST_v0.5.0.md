# PUBLICATION_MANIFEST v0.5.0

This is the release-specific publication record for AI Project OS v0.5.0.

本文件是 AI Project OS v0.5.0 的版本专用发布记录。

## Header

```text
Manifest ID: AIPOS-PUB-v0.5.0
Prepared Date: 2026-08-20
Prepared By: Codex
Destination Profile: private
Repository / Channel: GitHub repository + GitHub Release
Repository Visibility: PRIVATE (verified with GitHub)
Commit / Tag: codex/v0.5-repo-safety; tag pending human UAT
Release Asset: ai-project-os-v0.5.0.zip
Human Approver: dvdTeacher / Owner
Decision: Review - pending human UAT and final tracked/public scan
```

## Scope

```text
Purpose: Publish the v0.5 repository-safety and project-memory release.
Audience: AI-assisted project owners, operators, and maintainers.
Included Paths: Source repository changes; distributable template/project-os/ as release zip.
Excluded Paths: Dogfood audit history, local generated evidence, raw conversations, credentials, and release zip from Git source history.
Generated Artifact Source: template/project-os/
Rollback Location: v0.4.0 GitHub tag and Release.
```

## Artifact Classification

| Artifact / Path | Classification | Destination | Evidence | Owner | Included? | Notes |
|---|---|---|---|---|---|---|
| Root README and version metadata | Public Safe | Private GitHub source | validator + human review | Owner | Yes | Includes 60-second start |
| `template/project-os/` | Public Safe candidate | Private GitHub source + Release zip | strict standalone validation | Owner | Yes | Product distribution source; public reuse needs later approval |
| `project-os/` generic policies/tools | Team Shared | Private GitHub source | source/template drift check | Owner | Yes | Dogfood installation |
| `project-os/audit/` release evidence | Private Repo | Private GitHub source | safety scan + human review | Owner | Yes | No raw chat or secret values |
| Existing dogfood discovery details | Private Repo | Private GitHub source | public-profile Review classification | Owner | Yes | Excluded from distribution zip |
| `releases/ai-project-os-v0.5.0.zip` | Public Safe candidate | Private GitHub Release asset | archive + extracted-package validation | Owner | Release only | Not committed as source |
| Credentials, local environment, raw chat | Local Only | None | policy boundary | Owner | No | Must never enter artifact |

## Required Evidence

```text
Safety Scan Command: private/staged release gate; public/tracked advisory preflight for future visibility change
Safety Evidence Path: sanitized terminal summary; no persistent matched content
Safety Evidence Hash: N/A - summary-only scan
Block Findings: 0 required for Go
Review Findings: private/staged 0; public/tracked advisory 32
Review Conclusions: 30 SAF008 records fit the current Private Repo destination; 2 SAF009 Agent docs fit Team Shared in the current private repo. This is not approval for future public visibility; reclassification is required before any visibility change.
Validator Result: 0 failures, 0 warnings
Test Result: 10 passed
UAT Result: Pending human Owner
Archive / Artifact Check: unzip test and extracted standalone strict validation passed
Remote Asset Digest: 75eee07ddc40075399ae237044676dfb419f257c7e55461c04205d1fdda44120
```

## Agent Documents

| File | Canonical or Wrapper | Classification | Conflict Checked | Public Safe | Owner |
|---|---|---|---|---|---|
| `project-os/AGENTS.md` | Canonical | Public Safe | Yes | Yes, pending UAT | Owner |
| `template/project-os/AGENTS.md` | Distribution copy | Public Safe | Yes, validator drift check | Yes, pending UAT | Owner |
| Repository-root Agent wrapper | Not present | N/A | N/A | N/A | Owner |

## Project Memory

```text
Private Audit Included: Yes in the private source repository; no project-specific dogfood audit in the release zip
Discovery Detail Included: Existing dogfood evidence in the private source repository; generic blank templates only in the release zip
Raw Conversation Included: No
Local Overrides Included: Blank distributable template plus existing non-secret repository override
Unresolved High-Impact Gaps: None identified by current automated checks; human review pending
Human Conclusion: Pending
```

## Go / Review / Block

```text
Decision: Review
Decision Evidence: Validator, tests, archive, standalone package, local/worktree, and private/staged gates pass. Public advisory has zero Block and 32 destination-review findings; human UAT remains.
Approved By: Pending
Approved Date: Pending
Post-Publication Verification: Compare uploaded asset SHA-256, Release tag, README latest link, and Linear closeout.
Rollback Trigger: Digest mismatch, Block finding, missing QUICKSTART, failed standalone validation, or human UAT failure.
```
