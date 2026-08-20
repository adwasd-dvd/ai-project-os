# OS_VERSION

```text
Product: AI Project OS
Installed OS Version: v0.4.0
Installed Date: 2026-08-18
Local Customizations: This repo manages the AI Project OS source package itself.
Last Upgrade: 2026-08-19 to v0.4.0
```

## Compatibility

AI Project OS v0.4.0 expects:

- Local Codex as the development executor.
- Linear as the project management system.
- GitHub as the source, PR, CI, tag, and release fact source.
- Linear intake/follow-up automation may run as manual or scheduled dry-run/advisory scans.
- No automatic local code execution from scheduled automation by default.
- Basic Human/Codex handoff uses status + assignee, not required `next:*` labels.
- Mature or unclear repositories run Phase 0.5 Whitebox Discovery before baseline confirmation.
- Important whitebox findings record state, evidence, confidence, and next verification.
- The whitebox scanner is read-only by default and never emits secret values.

## Upgrade Rule

All upgrades must follow `UPGRADE_POLICY.md`.

Do not overwrite local project overrides during OS upgrades.
