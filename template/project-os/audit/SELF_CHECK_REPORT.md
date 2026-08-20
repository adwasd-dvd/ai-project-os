# SELF_CHECK_REPORT

本文件由 Codex 在 Phase 0 Self-Check 中生成或更新。

用途：记录本地 Codex 第一次接管项目前，项目位置、工具连接、依赖、账号和权限边界是否准备好。

## Metadata

```text
Check Date:
Codex Session:
Repository:
Branch:
Commit:
Status: Draft / Complete / Blocked
```

## Current Goal

```text
完成 AI Project OS Phase 0 Self-Check，并判断是否需要 Phase 0.5 Whitebox Discovery 和 Phase 0.75 Safety Classification。
```

## Project Location

| Check | Result | Notes |
|---|---|---|
| Current directory is project root | Yes / No / Unknown |  |
| `.git` exists | Yes / No |  |
| `project-os/` exists | Yes / No |  |
| Required project-os files exist | Yes / No |  |
| `project-os/audit/` exists | Yes / No |  |
| `project-os/discovery/` exists | Yes / No |  |
| Whitebox scanner exists | Yes / No | `project-os/tools/whitebox_scan.py` |
| `project-os/safety/` exists | Yes / No |  |
| Safety scanner exists | Yes / No | `project-os/tools/safety_scan.py` |

## Git / GitHub

| Check | Result | Notes |
|---|---|---|
| Git repository detected | Yes / No |  |
| Current branch detected | Yes / No |  |
| Current commit detected | Yes / No |  |
| Uncommitted changes | Yes / No / Unknown |  |
| Git remote detected | Yes / No |  |
| GitHub remote detected | Yes / No |  |
| GitHub write access ready | Yes / No / Not checked |  |

## Linear

| Check | Result | Notes |
|---|---|---|
| Linear MCP available | Yes / No / Not checked |  |
| Linear workspace known | Yes / No |  |
| Linear team known | Yes / No |  |
| Existing Linear project found | Yes / No / Not checked |  |
| Linear issue description language | English + Chinese / Chinese / English / Other | Default: English + Chinese unless user chooses otherwise |
| Linear issue description detail level | Actions + Expected Results / Basic | Linear issues should include execution actions and expected results |
| Ready for Phase 3 import | Yes / No |  |

## Project Shape

| Item | Detected Value | Evidence |
|---|---|---|
| Primary language |  |  |
| Framework |  |  |
| Package manager |  |  |
| App start command |  |  |
| Build command |  |  |
| Test command |  |  |
| Lint/typecheck command |  |  |
| Database / migrations |  |  |
| CI/CD |  |  |

## Whitebox Readiness

| Check | Result | Notes |
|---|---|---|
| Project is mature or context is incomplete | Yes / No / Unknown |  |
| Phase 0.5 required | Yes / No / Not Applicable | New empty projects may use Not Applicable with evidence |
| Read scope confirmed | Yes / No / Partial |  |
| Excluded/unavailable areas recorded | Yes / No |  |
| Scanner dry-run safe | Yes / No / Not checked | Must not write files |
| Discovery output confined to repository | Yes / No / Not checked | Default: `project-os/discovery/` |
| Production access required | Must be No |  |
| Secret values will be recorded | Must be No | Names and paths only |

## Safety / Publication Readiness

| Check | Result | Notes |
|---|---|---|
| Phase 0.75 required | Yes / No | Required before Git/team/public publication |
| Intended publication profile | local / private / team / public / Unknown |  |
| Intended destination |  | Repository, Release, or local-only |
| Agent document mode | local-only / team-shared / organization-shared / public-safe / Unknown |  |
| Safety scanner dry-run safe | Yes / No / Not checked | Must not write files |
| Safety output confined to repository | Yes / No / Not checked | Default: `project-os/safety/` |
| Project memory gaps identified | Yes / No / Not checked | No raw chat dumps |
| Matched values/source lines emitted | Must be No | Sanitized evidence only |
| Private repo treated as secret store | Must be No |  |

## Local Dependencies

| Check | Result | Notes |
|---|---|---|
| Dependencies installed | Yes / No / Unknown |  |
| Lockfile exists | Yes / No |  |
| Install command known | Yes / No |  |
| Safe to install now | Yes / No / Needs approval |  |

## Environment

| Check | Result | Notes |
|---|---|---|
| `.env.example` or equivalent exists | Yes / No |  |
| Required env vars known | Yes / No / Partial |  |
| Local app can run without secrets | Yes / No / Unknown |  |
| External services needed | Yes / No / Unknown |  |

## Permission Boundary Confirmed

```text
Phase 0/0.5/0.75/1 permissions:
- Read project files: Yes
- Write project-os/audit docs: Yes
- Write project-os/discovery docs: Yes
- Write sanitized project-os/safety docs: Yes
- Modify product code: No
- Write Linear: No
- Create GitHub PR: No
```

## Blocking Items

These block Phase 0.5, Phase 0.75, or Phase 1.

```text
- 
```

## Non-blocking Missing Items

These do not block Phase 1 but must be resolved before later phases.

```text
- 
```

## Questions For User

Ask only the next 1 to 3 blocking questions.

```text
1.
2.
3.
```

## Phase 0 Conclusion

```text
Needs Phase 0.5 Whitebox Discovery: Yes / No / Not Applicable
Needs Phase 0.75 Safety Classification: Yes / No
Can start Phase 0.5, Phase 0.75, or Phase 1 Audit: Yes / No
Reason:
Recommended next step:
```
