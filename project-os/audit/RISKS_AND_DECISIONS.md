# RISKS_AND_DECISIONS

## Risk Summary

The project is low technical risk because it is Markdown-only. The main risks are process drift, accidental public GitHub creation, Linear import into the wrong team, and template/self-management file confusion.

## Open Decisions

| Decision ID | Question | Context | Options | Recommendation | Owner | Blocking | Needed By | Status |
|---|---|---|---|---|---|---|---|---|
| DEC-001 | Which Linear team should own AI Project OS? | Linear import needs a team | Existing team / new team | Use an existing personal/product team if available | Owner | Yes for Phase 3 | Before Linear import | Open |
| DEC-002 | Confirm GitHub repo owner/name | Private repo creation needs target | `adwasd-dvd/ai-project-os` / other | Use `adwasd-dvd/ai-project-os` | Owner | Yes for GitHub remote | Before repo creation | Open |
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

## Security / Privacy / Compliance Risks

| Risk ID | Risk | Impact | Evidence | Mitigation | Owner | Severity |
|---|---|---|---|---|---|---|
| RISK-SEC-001 | GitHub repo accidentally public | Exposes process docs or project details | User explicitly requested private | Use `gh repo create --private` only and verify visibility | Codex | High |

## Release Risks

| Version | Risk | Impact | Mitigation | Decision Needed |
|---|---|---|---|---|
| v0.1.0 | Manual-only validation | Package may be incomplete | File inventory check before tag | No |
| v0.2.0 | Validator scope creep | Overcomplicates OS | Define acceptance criteria first | Yes |

## Closed Decisions

| Decision ID | Final Decision | Decided By | Date | Impact |
|---|---|---|---|---|
| None |  |  |  |  |

