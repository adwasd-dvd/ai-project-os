# RISKS_AND_DECISIONS

## Risk Summary

The project is low technical risk because it is Markdown-only. The main risks are process drift, accidental public GitHub creation, Linear import into the wrong team, and template/self-management file confusion.

## Open Decisions

| Decision ID | Question | Context | Options | Recommendation | Owner | Blocking | Needed By | Status |
|---|---|---|---|---|---|---|---|---|
| DEC-001 | Which Linear team should own AI Project OS? | Linear import needs a team | Existing team / new team | Use an existing personal/product team if available | Owner | Yes for Phase 3 | Before Linear import | Open |
| DEC-002 | Confirm GitHub repo owner/name | Private repo creation needed target | `adwasd-dvd/ai-project-os` / other | Use `adwasd-dvd/ai-project-os` | Owner | No | Completed during setup | Closed |
| DEC-003 | Should release zips be committed? | Generated artifacts can clutter repo | GitHub Releases only / commit zips | GitHub Releases only | Owner | No | Before first release | Open |

## Business Risks

| Risk ID | Risk | Impact | Evidence | Mitigation | Owner | Severity |
|---|---|---|---|---|---|---|
| RISK-001 | OS feels too heavy for users | Adoption friction | Multiple policy files | Keep START_HERE simple and add examples | Owner | Medium |
| RISK-002 | Users skip approval gates | Linear/GitHub mess | Process depends on prompts | Keep hard rules repeated in key files | Owner | Medium |

## Technical Risks

| Risk ID | Risk | Impact | Evidence | Mitigation | Owner | Severity |
|---|---|---|---|---|---|---|
| RISK-TECH-001 | Template and installed OS drift | Confusing upgrades | Two `project-os` copies | Add validator or sync policy | Codex | Medium |
| RISK-TECH-002 | No automated checks | Regressions in docs | Manual verification only | Add v0.2 validator | Codex | Medium |
| RISK-AUTO-001 | Scheduled polling misses or over-fetches Linear changes | Stale or rate-limited intake | Cron MVP reads a bounded issue window | Explicit project scope, update ordering, small max, lookback, bounded retries; use webhooks at larger scale | Codex | Medium |
| RISK-AUTO-002 | Linear GraphQL schema or permissions change | Live scan or mutation fails | External API dependency | Fail closed on GraphQL errors; fixture tests; do not apply a failed/partial scan | Codex | Medium |
| RISK-AUTO-003 | Authorized automation writes an unwanted comment/update | Linear noise or workflow drift | Semi-automatic write capability | Scan/apply separation, minimal allowlist, runtime authorization, stable idempotency key, sanitized ledger | Owner / Codex | High |
| RISK-TRACE-001 | Traceability manifest becomes stale | False confidence in release readiness | Evidence is partly maintained by process | Validate paths/states before PR, UAT, and release; include in quality gate | Codex | Medium |
| RISK-TRACE-002 | Change-impact claim is incomplete or overconfident | Missed dependency, security, test, or UAT impact | AI-generated analysis can be wrong | Seven required areas, confidence, evidence, next verification, high-impact low-confidence blocker | Owner / Codex | High |
| RISK-REL-001 | Release readiness evidence becomes stale or internally contradictory | A release may be published with missing UAT, rollback, safety, or package facts | Train B combines multiple release gates | Deterministic input, freshness checks, fail-closed readiness, and human publication approval | Owner / Codex | High |
| RISK-REL-002 | Rollback automation damages Git or project state | Recovery can make an incident worse | Rollback touches version and publication state | Generate human-approved guidance and receipts; never rewrite history, delete releases, or roll production back automatically | Owner / Codex | High |
| RISK-UPG-001 | OS upgrade overwrites project memory or local policy | Project-specific decisions, Linear mappings, and safety dispositions can be lost | Installed OS and upstream share paths | Protected-path policy, three-way classification, conflict blocking, byte-preservation tests, and branch-only apply | Owner / Codex | High |
| RISK-UPG-002 | A stale or untrusted upgrade plan writes unexpected files | Repository integrity or private context may be damaged | Plan and source can change between inspect and apply | Source/target hashes, plan freshness, path confinement, explicit CLI/runtime authorization, idempotent receipt | Codex | High |
| RISK-UPG-003 | Upstream metadata or network state is unavailable or misleading | Wrong version comparison or unsafe downgrade | GitHub/local package is an external evidence source | Validate semantic versions and source evidence; fail closed on ambiguity; require explicit downgrade policy | Codex | Medium |
| RISK-LIN-001 | Free Linear issue limit prevents one-issue-per-feature tracking | Individual queue assignment and issue lifecycle are unavailable | Workspace rejected AIPOS-045..051 creation at 250 non-archived issues | Use a Project Document as an explicit equivalent record; never invent IDs; idempotently create issues after capacity is available | Owner / Codex | Medium |
| RISK-LIN-002 | A legacy version-prefix scan includes completed historical Projects or truncates the canonical Project | Intake can become noisy or fail closed before reaching current work | DEC-010 consolidated 53 issues into one Project while the v0.6 runner supports exact Project scope and a bounded maximum | Configure exact Project AI Project OS, empty project_name_prefixes, and max_issues 250; use Milestone plus Target Version for release scope | Owner / Codex | Medium |

## Security / Privacy / Compliance Risks

| Risk ID | Risk | Impact | Evidence | Mitigation | Owner | Severity |
|---|---|---|---|---|---|---|
| RISK-SEC-001 | GitHub repo accidentally public | Exposes process docs or project details | User explicitly requested private | Mitigated: repo visibility verified as `PRIVATE` | Codex | Low |

## Release Risks

| Version | Risk | Impact | Mitigation | Decision Needed |
|---|---|---|---|---|
| v0.1.0 | Manual-only validation | Package may be incomplete | File inventory check before tag | No |
| v0.2.0 | Validator scope creep | Overcomplicates OS | Define acceptance criteria first | Yes |
| v0.6.0 | Automation and traceability land as disconnected tools | Users cannot operate the full loop | One worked scenario, one trace manifest, one consolidated UAT | No; covered by DEC-009 |
| v0.6.0 | Live API write behavior differs from fixture | Unintended Linear changes | Default dry-run, comments-only starting allowlist, human review before first live apply | Human approval before live apply |
| v0.8.0 | Release and self-upgrade controls pass separately but fail as one workflow | False confidence in recoverability | Isolated older-to-candidate dogfood, deterministic package tests, and one consolidated UAT | No; covered by DEC-009 |
| v0.8.0 | Upgrade conflict handling loses local project memory | Irreversible loss or silent policy drift | Protected-path fixtures, hash verification, branch-only apply, and no automatic destructive rollback | Human approval before any real-project apply |

## Closed Decisions

| Decision ID | Final Decision | Decided By | Date | Impact |
|---|---|---|---|---|
| DEC-002 | Use private GitHub repo `adwasd-dvd/ai-project-os` | Codex based on user request | 2026-08-18 | GitHub remote created and verified private |
| DEC-009 | Use three large development trains; Train A combines former v0.6 + v0.7 as formal v0.6.0 with one consolidated UAT | Owner | 2026-08-24 | DVD-218; enables batch implementation while preserving Feature, safety, traceability, UAT, and release gates |
| DEC-010 | Use one long-lived Linear Project named AI Project OS; represent releases as Milestones and never create per-version Projects by default | Owner | 2026-08-25 | Consolidated 53 issues into one active Project; six old Projects are empty Completed history pointers; future work uses one Project plus one target-version Milestone |
