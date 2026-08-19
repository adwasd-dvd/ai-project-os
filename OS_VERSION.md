# OS_VERSION

```text
Product: AI Project OS
Source Repository Version: v0.3.0
Installed Self-Management Version: v0.3.0
Release Channel: experimental
Installed Date: 2026-08-18
Last Upgrade: 2026-08-19 to v0.3.0
```

## Compatibility

AI Project OS v0.3.0 expects:

- Local Codex as the development executor.
- Linear as the project management system.
- GitHub as the private source, PR, CI, tag, and release fact source.
- Linear intake/follow-up automation may run as manual or scheduled dry-run/advisory scans.
- No automatic local code execution from scheduled automation by default.
- Basic Human/Codex handoff uses status + assignee, not required `next:*` labels.

## Upgrade Rule

All upgrades must follow `UPGRADE_POLICY.md`.

Do not overwrite local project overrides during OS upgrades.
