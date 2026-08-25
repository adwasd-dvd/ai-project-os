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

## Closed Decisions

| Decision ID | Final Decision | Decided By | Date | Impact |
|---|---|---|---|---|
| DEC-002 | Use private GitHub repo `adwasd-dvd/ai-project-os` | Codex based on user request | 2026-08-18 | GitHub remote created and verified private |
| DEC-009 | Use three large development trains; Train A combines former v0.6 + v0.7 as formal v0.6.0 with one consolidated UAT | Owner | 2026-08-24 | DVD-218; enables batch implementation while preserving Feature, safety, traceability, UAT, and release gates |
