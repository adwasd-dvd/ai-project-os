# GAPS_AND_DUPLICATES

## Summary

No duplicate features were found. Main gaps are around automation, first GitHub/Linear setup, and example-based onboarding.

## Suspected Duplicate Features

| Candidate A | Candidate B | Why Duplicate | Evidence | Recommendation | Needs Human Decision |
|---|---|---|---|---|---|
| None | None | No duplicate found | Current feature inventory | Keep Separate | No |

## Missing Features

| Missing Feature | Module | Why It Seems Missing | Evidence | Suggested Target Version |
|---|---|---|---|---|
| Automated OS policy validator | QUALITY | Current verification is manual | No scripts or CI | v0.2.0 |
| Worked example walkthrough | DOCS | User wants to learn Linear/GitHub workflow by doing | Current docs are mostly templates | v0.2.0 |
| GitHub Release publishing guide | GITHUB | Zip packaging exists but release publication is not formalized | No release doc beyond policy | v0.2.0 |

## Partial Implementations

| Feature ID | What Exists | What Is Missing | Risk | Suggested Action |
|---|---|---|---|---|
| AIPOS-005 | GitHub policy and CLI auth | Private repo creation/push | Cannot use GitHub as fact source yet | Create private repo after confirmation |
| AIPOS-008 | Release artifact directory | Final zip build from `template/project-os/` | Package may drift | Build zip after Git init |

## Missing Tests

| Area | Missing Test | Risk | Suggested Owner |
|---|---|---|---|
| File inventory | Required files check | Package may miss files | Codex |
| Policy gates | Check for hard-rule text | Future edits may remove gates | Codex |
| Zip packaging | Verify top-level `project-os/` in zip | Bad package shape | Codex |

## Missing Acceptance Criteria

| Feature ID | Missing Criteria | Why It Matters | Decision Needed |
|---|---|---|---|
| AIPOS-009 | Validator scope | Avoid overbuilding | Yes |
| AIPOS-010 | Example project format | Could be docs, video script, or guided Linear project | Yes |

## Documentation Gaps

| Gap | Impact | Suggested Fix |
|---|---|---|
| No hands-on walkthrough yet | User may still not know Linear/GitHub flow | Add v0.2 worked example |
| No upgrade dry-run example | OS upgrades are abstract | Add sample `OS_UPGRADE_PLAN.md` |

## Linear Follow-up Suggestions

- Create `AIPOS-001` through `AIPOS-010`.
- Create Decisions for Linear team and GitHub repo owner/name if not confirmed.
- Mark v0.2 ideas as Backlog or Planned.

