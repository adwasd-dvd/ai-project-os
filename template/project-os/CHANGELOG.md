# CHANGELOG

## v1.0.0 - In Development

Internal Stable Rescue combines existing whitebox, safety, Linear, traceability, release, and upgrade controls into one mature-project rescue workflow.

In progress:

- `RESCUE_PROTOCOL.md` and `tools/rescue_project.py` with inspect/plan/verify separation.
- Sanitized product evidence that excludes the installed `project-os/` package by default.
- Evidence-backed contradiction, unknown, risk, Decision, impact, confidence, and next-verification routing.
- Deterministic diagnosis, recovery roadmap, bilingual one-Project Linear dry-run package, proactive PM queues, and artifact receipt.
- Representative messy-project tests and end-to-end internal-stable certification.
- Real-project UAT fixes for Worker-context environment lookup classification and portable custom-output references.

## v0.8.0 - 2026-08-26

Development Train B combines release/rollback control with safe OS self-upgrade.

Added:

- Traceability schema v2 with explicit equivalent Linear records, structured Feature/version UAT, and separate post-release state.
- `RELEASE_CONTROL.md`, structured release inputs, and `tools/release_project.py` for deterministic readiness, release notes, feedback classification, and sanitized post-release receipts.
- Executable `UPGRADE_POLICY.md` flow, reusable upgrade configs, and `tools/upgrade_project_os.py` for version discovery, three-way planning, guarded branch apply, idempotency, and hash verification.
- Focused release and upgrade tests for evidence gates, conflicts, preservation, authorization, path confinement, downgrade, stale plans, recovery, and deterministic outputs.

Human UAT passed on 2026-08-26 and the release was authorized by the Owner.

## v0.6.0 - 2026-08-25

Development Train A combines scheduled Linear intake automation with change-impact and requirement-to-release traceability.

Added:

- `tools/linear_intake.py` with offline/live reads, deterministic queue routing, bilingual reports, planned actions, guarded writes, idempotency, retry handling, and sanitized receipts.
- `automation/` config and cross-version fixture plus ignored `runtime/` state boundary.
- `AUTOMATION_RUNBOOK.md` with manual, cron-compatible, Codex recurring, credential, write-enable, and failure-handoff steps.
- `CHANGE_IMPACT.md`, `TRACEABILITY.md`, reusable JSON inputs, and `tools/trace_project.py`.
- Automated tests for routing, Ready checks, credentials, triple write gates, idempotency, partial failure, evidence states, and change-impact blockers.
- Deterministic release packaging from committed template content with fixed archive metadata.
- Development Train cadence from DEC-009 and one consolidated v0.6.0 human UAT.

Updated:

- Core Agent, workflow, Linear, quality, UAT, version-planning, roadmap, startup, and package rules for executable automation and traceability.
- Validator coverage for v0.6 files and safety boundaries.

Human UAT passed on 2026-08-25 and the release was authorized by the Owner.

## v0.5.0 - 2026-08-20

Repository safety and project-memory boundary release.

Added:

- `SECURITY_BOUNDARY.md` with Local Only, Team Shared, Private Repo, and Public Safe classifications.
- `REPO_PUBLICATION_POLICY.md` with staged/private and tracked/public gates.
- `AGENT_DOC_POLICY.md` for single-user, team, and public Agent instructions.
- `safety/` publication manifest, memory audit, documentation-gap register, and sanitized secret-scan report.
- Read-only `tools/safety_scan.py` with worktree/staged/tracked scopes and local/private/team/public profiles.
- Scanner tests proving matched values and source lines are never emitted.
- `QUICKSTART.md` with a 60-second install and Codex startup path.
- `examples/SAFETY_EXAMPLE.md`.

Updated:

- Bootstrap, workflow, GitHub, release, quality, and UAT policies for Phase 0.75 Safety Classification.
- Validator coverage for v0.5 files, report fields, scanner guardrails, and install-package support.

## v0.4.0 - 2026-08-19

Project Whitebox release for evidence-backed takeover of mature black-box and gray-box repositories.

Added:

- Phase 0.5 Whitebox Discovery before baseline confirmation for mature or unclear projects.
- `WHITEBOX_PROTOCOL.md` with Observed, Derived, Claimed, Inferred, Contradicted, and Unknown evidence states.
- High, Medium, Low, and Unknown confidence levels with explicit next verification.
- `discovery/PROJECT_MAP.md`, `DEPENDENCY_MAP.md`, `DOCUMENT_INVENTORY.md`, `SETTINGS_AND_DATA_REGISTER.md`, `LOGIC_BOUNDARY_AUDIT.md`, and `WHITEBOX_IMPORT_REPORT.md`.
- Read-only-by-default `tools/whitebox_scan.py` and scanner unit tests.
- `examples/WHITEBOX_EXAMPLE.md` with a full evidence-to-Linear handoff.

Updated:

- `BOOTSTRAP.md`, `SELF_CHECK.md`, `AGENTS.md`, `WORKFLOW.md`, `PROJECT.md`, `QUALITY_GATE.md`, `LINEAR_POLICY.md`, `START_HERE.md`, and `UAT_TEMPLATE.md` for Phase 0.5.
- Validator coverage for required whitebox files, report fields, template sync, and scanner safety guardrails.
- Validator layout detection so strict checks pass in both the source repository and an installed package containing only `project-os/`.

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
