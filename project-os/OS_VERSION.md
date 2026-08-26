# OS_VERSION

```text
Product: AI Project OS
Installed OS Version: v0.8.0
Installed Date: 2026-08-18
Local Customizations: This repo manages the AI Project OS source package itself.
Last Upgrade: 2026-08-26 to v0.8.0
```

## Compatibility

AI Project OS v0.8.0 expects:

- Local Codex as the development executor.
- Linear as the project management system.
- GitHub as the source, PR, CI, tag, and release fact source.
- Linear intake/follow-up automation may run as manual or scheduled dry-run/advisory scans.
- No automatic local code execution from scheduled automation by default.
- Basic Human/Codex handoff uses status + assignee, not required `next:*` labels.
- Mature or unclear repositories run Phase 0.5 Whitebox Discovery before baseline confirmation.
- Important whitebox findings record state, evidence, confidence, and next verification.
- The whitebox scanner is read-only by default and never emits secret values.
- Repository artifacts use Local Only, Team Shared, Private Repo, or Public Safe classification.
- Private repositories are never treated as secret stores.
- Commit/publication gates use sanitized safety evidence and human approval.
- Agent documents separate stable shared rules from local personal context.
- Project-memory gaps and chat-only claims remain visible until verified.
- Linear intake uses an executable dry-run-first runner with status + assignee routing.
- Linear writes require config allowlist, CLI authorization, runtime authorization, and idempotent receipts.
- Scheduled automation never modifies local product code or approves Decision, scope, UAT, merge, tag, or release.
- Formal work uses a seven-area change-impact gate before development.
- Formal features maintain requirement-to-release traceability, with automated tests and human UAT kept separate.
- Release readiness, human UAT, GitHub Release, and post-release verification remain separate evidence states.
- OS upgrades use installed/base/target planning, protected-path preservation, branch-only apply, dual authorization, hash verification, and project human UAT.

## Upgrade Rule

All upgrades must follow `UPGRADE_POLICY.md`.

Do not overwrite local project overrides during OS upgrades.
