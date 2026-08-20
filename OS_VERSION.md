# OS_VERSION

```text
Product: AI Project OS
Source Repository Version: v0.5.0
Installed Self-Management Version: v0.5.0
Release Channel: experimental
Installed Date: 2026-08-18
Last Upgrade: 2026-08-19 to v0.5.0
```

## Compatibility

AI Project OS v0.5.0 expects:

- Local Codex as the development executor.
- Linear as the project management system.
- GitHub as the private source, PR, CI, tag, and release fact source.
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

## Upgrade Rule

All upgrades must follow `UPGRADE_POLICY.md`.

Do not overwrite local project overrides during OS upgrades.
