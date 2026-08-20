# DEPENDENCY_MAP

## Header / 头部

```text
Project:
Scan Evidence:
Git Commit:
Prepared Date:
Coverage Status: Draft / Partial / Complete
```

## Manifest and Lockfile Inventory / Manifest 与 Lockfile 清单

| Path | Kind | Ecosystem | Lockfile or Version Source | State | Evidence | Confidence | Gap |
|---|---|---|---|---|---|---|---|
|  | Manifest / Lockfile / Runtime / Infrastructure |  |  | Observed / Claimed / Unknown |  |  |  |

Finding a declaration proves that a dependency is declared. It does not by itself prove that the dependency is used at runtime.

发现声明只能证明依赖被声明，不能单独证明它在运行时被使用。

## Important Package Dependencies / 重要 Package 依赖

| Dependency | Scope | Purpose | Used By | Version Source | Owner | Failure Impact | Evidence | State | Confidence | Next Verification |
|---|---|---|---|---|---|---|---|---|---|---|
|  | Runtime / Development / Build / Test |  |  |  |  |  |  |  |  |  |

## Runtime and Platform Dependencies / 运行时与平台依赖

| Runtime or Platform | Required Version | Purpose | Local / CI / Production | Version Evidence | Failure Impact | Confidence | Unknowns |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

## External Services and Integrations / 外部服务与集成

| Service | Purpose | Direction | Boundary | Auth Key Names Only | Owner | Failure Behavior | Evidence | Confidence | Next Verification |
|---|---|---|---|---|---|---|---|---|---|
|  |  | Inbound / Outbound / Both |  |  |  |  |  |  |  |

Never record credential values, connection strings, tokens, or private endpoints here.

不得在此记录凭证值、连接字符串、token 或私有 endpoint。

## Infrastructure Dependencies / 基础设施依赖

| Dependency | Purpose | Definition Path | Environment | Owner | State | Evidence | Confidence | Unknowns |
|---|---|---|---|---|---|---|---|---|
| Container / Queue / Cache / Database / Storage / DNS / CDN |  |  |  |  |  |  |  |  |

## Dependency Risks and Gaps / 依赖风险与缺口

| Finding ID | Type | Claim | Impact | Evidence | Confidence | Next Verification | Disposition |
|---|---|---|---|---|---|---|---|
| DEP-001 | Unknown Purpose / Unused / Duplicate / Unpinned / Unsupported / Missing Owner / Failure Gap |  |  |  |  |  | Decision / Bug / Feature / Backlog / Accept Risk |

## Completion / 完成

```text
Supported manifests reviewed:
Lockfiles reviewed:
Critical integrations reviewed:
Unowned critical dependencies:
High-impact low-confidence findings:
Ready for baseline: Yes / No
```
