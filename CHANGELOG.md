# CHANGELOG

## v0.6.0 - 2026-08-25

Development Train A release for safe Linear automation and requirement-to-release traceability.

Added:

- Executable dry-run-first Linear intake with offline fixtures and live GraphQL reads.
- Status + assignee queue routing, Ready checks, cross-version feedback watch, and bilingual reports.
- Explicitly authorized idempotent Linear writes, bounded retries, and a sanitized local ledger.
- Manual, cron-compatible, and Codex recurring automation runbook.
- Seven-area change-impact gates and deterministic requirement-to-release traceability.
- Focused tests, standalone package verification, and one consolidated human UAT.

Updated:

- Workflow, quality, UAT, release, version-planning, roadmap, startup, and validator rules for executable automation and traceability.
- Release artifact name to `ai-project-os-v0.6.0.zip`.

## v0.5.0 - 2026-08-20

Repository safety and project-memory boundary release.

Added:

- `SECURITY_BOUNDARY.md` with Local Only, Team Shared, Private Repo, and Public Safe classifications.
- `REPO_PUBLICATION_POLICY.md` with staged/private and tracked/public gates.
- `AGENT_DOC_POLICY.md` for single-user, team, and public Agent instructions.
- `safety/` publication manifest, memory audit, documentation-gap register, and sanitized secret-scan report.
- Read-only `safety_scan.py` with worktree/staged/tracked scopes and local/private/team/public profiles.
- Scanner tests proving matched values and source lines are never emitted.
- `QUICKSTART.md` and a GitHub 60-second install/start path.
- Worked safety and project-memory example.

Updated:

- Bootstrap, workflow, GitHub, release, quality, and UAT policies for Phase 0.75 Safety Classification.
- Validator coverage for v0.5 files, report fields, scanner guardrails, and install-package support.
- Release artifact name to `ai-project-os-v0.5.0.zip`.

## v0.4.0 - 2026-08-19

Project Whitebox release for evidence-backed takeover of mature black-box and gray-box repositories.

Added:

- Phase 0.5 Whitebox Discovery before baseline confirmation for mature or unclear projects.
- `WHITEBOX_PROTOCOL.md` with evidence states, confidence levels, precedence, stop conditions, and secret-value boundaries.
- Six discovery reports for project shape, dependencies, documents, settings/data, logic/boundaries, and Linear handoff.
- Deterministic, standard-library `whitebox_scan.py` with dry-run, bounded write, and stale-evidence check modes.
- Scanner tests for ignored paths, deterministic output, output confinement, and secret-value non-emission.
- Worked whitebox example with observed, inferred, contradicted, and unknown findings.

Updated:

- Bootstrap, self-check, workflow, quality gates, Linear project descriptions, UAT, and validator now enforce the whitebox contract.
- Validator supports both the source-repository layout and a standalone installed `project-os/` package.
- Release artifact name to `ai-project-os-v0.4.0.zip`.

## v0.3.0 - 2026-08-19

Human/Codex handoff release for low-friction single-user Linear operation.

Added:

- Assignee-driven Human/Codex routing:
  `Assigned = human queue`, `Unassigned = Codex queue`, `Status = lifecycle`.
- Linear intake routing table for Codex Queue, Human Queue, Review Queue, and inconsistent states.
- Handoff prompt and UAT playbook for pass, failed UAT, and rework.
- `ROADMAP.md` with v0.4 through v1.0 and post-1.0 open-source readiness.
- Validator guardrails for v0.3 handoff rules.

Updated:

- `next:*` labels are now optional advanced signals, not basic workflow requirements.
- Release artifact name to `ai-project-os-v0.3.0.zip`.

## v0.2.0 - 2026-08-19

Operational workflow release for daily Linear-driven AI Project OS usage.

Added:

- Requirement and issue management workflow.
- Version planning, staged delivery, patch handling, and carry-over revalidation workflow.
- Linear intake scan contract for broad prompts and scheduled scans.
- Cron-ready automation policy with dry-run defaults and idempotency rules.
- Bilingual Linear output policy for comments, status updates, UAT notes, and run summaries.
- Worked first-project walkthrough.
- Lightweight validator for required files, policy guardrails, template drift, and release zip shape.

Updated:

- Root/source version and installed self-management version to `v0.2.0`.
- Release artifact name to `ai-project-os-v0.2.0.zip`.

## v0.1.0 - 2026-08-18

Initial AI Project OS source project.

Added:

- Phase 0 Self-Check.
- Phase 1 Audit.
- Phase 2 Baseline Confirmation.
- Phase 3 Linear Setup/Import.
- Phase 4 Release Planning.
- Phase 5 Development.
- Phase 6 Human Acceptance.
- Linear governance policy.
- GitHub governance policy.
- Release policy.
- Quality gates.
- Feature and UAT templates.
- OS versioning and upgrade policy.
- Local override policy.

Notes:

- Linear import still requires human approval before first bulk write.
- GitHub repository must be private.
- Cloud Codex is intentionally out of scope for v0.1.0.
