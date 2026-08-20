# Release v0.5.0

Candidate release notes for AI Project OS v0.5.0. Do not publish before human UAT.

AI Project OS v0.5.0 候选发布说明。人工 UAT 前不得发布。

## Summary

v0.5 adds a repository-safety and project-memory boundary around the v0.4 whitebox flow. It classifies what stays local, what a team may share, what belongs only in a private repository, and what is safe to publish. Its scanner reports the risk without reproducing the protected value or source line.

v0.5 在 v0.4 白盒流程外增加仓库安全与项目记忆边界：区分仅本地、团队共享、私有仓库和公开安全内容；scanner 报告风险，但不复制被保护的值或源代码行。

## Included Features

| Feature ID | Linear | Summary |
|---|---|---|
| DEC-008 | DVD-82 | Confirm safety classification, publication, Agent-doc, and project-memory boundaries |
| AIPOS-031 | DVD-83 | Four-level security boundary and sanitized finding contract |
| AIPOS-032 | DVD-84 | Repository publication profiles, staged/tracked gates, and human manifest |
| AIPOS-033 | DVD-85 | Single-user, team, organization, and public Agent document modes |
| AIPOS-034 | DVD-86 | Project-memory audit and documentation-gap register |
| AIPOS-035 | DVD-87 | Read-only deterministic safety scanner with sanitized output |
| AIPOS-036 | DVD-88 | Validator guardrails, examples, tests, package, and UAT |
| AIPOS-037 | DVD-89 | GitHub 60-second download/place/prompt startup path |

## What Users Get

- A prominent GitHub README quickstart and full `QUICKSTART.md`.
- Phase 0.75 Safety Classification after mature-project whitebox discovery.
- Publication profiles for local, private, team, and public destinations.
- Explicit rule that a private repository is not a secret store.
- Agent document sharing modes and conflict handling.
- Project-memory and document-gap templates that preserve uncertainty.
- A standard-library scanner with worktree/staged/tracked scopes and local/private/team/public profiles.
- Human Go/Review/Block publication manifest and release digest checks.

## Known Limitations

- The scanner is a bounded heuristic safety gate, not a replacement for a full security audit, provider-side secret scanner, DLP system, or legal/privacy review.
- It can identify a repository-relative path and rule without proving whether a credential is active.
- It never rotates credentials, deletes files, rewrites Git history, changes visibility, or approves publication.
- Human classification is still required for private architecture, Agent documents, and ambiguous project memory.
- Scheduled Linear/Cron execution remains planned for v0.6.

## Verification

```text
Strict validator: 0 failures, 0 warnings
Automated tests: 10 passed
Local/worktree safety scan: Block 0, Review 0, Gate Go
Release archive integrity: Passed
Extracted standalone strict validation: Passed
Extracted standalone tests: 10 passed
Human UAT: Pending
```

## GitHub

```text
Branch: codex/v0.5-repo-safety
Draft PR: Pending
Tag: Pending UAT
Release: Pending UAT
Release asset: ai-project-os-v0.5.0.zip
Release SHA-256: 75eee07ddc40075399ae237044676dfb419f257c7e55461c04205d1fdda44120
```
