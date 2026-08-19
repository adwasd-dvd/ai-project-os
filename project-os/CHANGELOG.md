# CHANGELOG

## v0.3.0 - 2026-08-19

Human/Codex handoff release for low-friction single-user Linear operation.

Added:

- Assignee-driven routing:
  `Assigned = human queue`, `Unassigned = Codex queue`, `Status = lifecycle`.
- Codex Queue, Human Queue, Review Queue, and inconsistent-state reporting in Linear intake.
- Human/Codex handoff playbook for pass, failed UAT, clarification, and rework.
- v0.3 UAT scenarios for status + assignee transitions.
- `ROADMAP.md` with v0.4 through v1.0 and post-1.0 open-source readiness.
- Validator checks for v0.3 handoff policy.

Updated:

- `LINEAR_POLICY.md`, `LINEAR_INTAKE.md`, `AUTOMATION_POLICY.md`, `WORKFLOW.md`, `QUALITY_GATE.md`, `FEATURE_TEMPLATE.md`, `UAT_TEMPLATE.md`, and `examples/FIRST_PROJECT.md`.
- `next:*` labels are optional advanced signals, not required in the basic Human/Codex loop.

## v0.2.0 - 2026-08-19

Operational workflow release for day-to-day Linear usage.

Added:

- Requirement and issue management workflow.
- Version planning and staged delivery workflow.
- Linear intake scan contract for broad prompts and scheduled runs.
- Cron-ready Linear follow-up automation policy with dry-run defaults.
- Bilingual Linear output policy for comments, status updates, decisions, UAT notes, and run summaries.
- Version closeout and carry-over revalidation workflow.
- Linear-driven Codex handoff prompt library in `START_HERE.md` and supporting docs.
- Worked first-project example in `examples/FIRST_PROJECT.md`.
- Lightweight validator in `tools/validate_project_os.py`.

Updated:

- `AGENTS.md` now treats broad Linear checks and automation boundaries as hard rules.
- `LINEAR_POLICY.md` now covers comments, status updates, run summaries, carry-over issues, and automation boundaries.
- `RELEASE_POLICY.md` now requires carry-over instead of moving old completed issues.
- `QUALITY_GATE.md` now includes Linear intake, scheduled scan, and carry-over gates.
- `UAT_TEMPLATE.md` now validates bilingual Linear output, cross-version intake, carry-over, and scheduled dry-run idempotency.

## v0.1.0 - 2026-08-18

Initial AI Project OS lazy pack.

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

Updated after UAT:

- Phase 0 now asks or confirms Linear Issue description language.
- Default Linear Issue description language is `English + Chinese`.
- Linear Issue templates now require `Action Steps` and `Expected Result`.
