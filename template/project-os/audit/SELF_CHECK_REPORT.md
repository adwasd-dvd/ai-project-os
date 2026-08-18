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
完成 AI Project OS Phase 0 Self-Check，并判断是否可以进入 Phase 1 Audit。
```

## Project Location

| Check | Result | Notes |
|---|---|---|
| Current directory is project root | Yes / No / Unknown |  |
| `.git` exists | Yes / No |  |
| `project-os/` exists | Yes / No |  |
| Required project-os files exist | Yes / No |  |
| `project-os/audit/` exists | Yes / No |  |

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
Phase 0/1 permissions:
- Read project files: Yes
- Write project-os/audit docs: Yes
- Modify product code: No
- Write Linear: No
- Create GitHub PR: No
```

## Blocking Items

These block Phase 1.

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
Can start Phase 1 Audit: Yes / No
Reason:
Recommended next step:
```

