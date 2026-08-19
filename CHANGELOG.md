# CHANGELOG

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
