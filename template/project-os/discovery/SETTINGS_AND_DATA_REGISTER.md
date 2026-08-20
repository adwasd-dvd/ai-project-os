# SETTINGS_AND_DATA_REGISTER

## Safety Rule / 安全规则

Record setting names, purpose, source paths, and ownership. Never record values for passwords, tokens, keys, cookies, connection strings, private URLs, or personal data.

记录设置名、用途、来源路径和 owner。不得记录密码、token、key、cookie、连接字符串、私有 URL 或个人数据值。

## Header / 头部

```text
Project:
Scan Evidence:
Git Commit:
Prepared Date:
Coverage Status: Draft / Partial / Complete
Secret Values Present: Must be No
```

## Settings Register / 设置登记表

| Setting Name | Purpose | Source or Example Path | Required In | Default Exists | Sensitive Claim | Owner | State | Evidence | Confidence | Unknowns |
|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  | Local / CI / Staging / Production / Unknown | Yes / No / Unknown | Secret / Sensitive / Public / Unknown |  | Observed / Claimed / Inferred / Unknown |  |  |  |

Do not paste values into this table.

不得把值粘贴进本表。

## Configuration Sources / 配置来源

| Source | Format | Scope | Loaded By | Precedence Claim | Evidence | State | Confidence | Contradiction |
|---|---|---|---|---|---|---|---|---|
| Environment / File / Secret Store / Flag / Database |  |  |  |  |  |  |  |  |

## Data Stores and Assets / 数据存储与资产

| Store or Asset | Kind | Purpose | Schema Source | Writer | Reader | Lifecycle or Retention Claim | Sensitivity Claim | Owner | Evidence | Confidence | Unknowns |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  | Database / File / Object Store / Cache / Queue / Search / Analytics / External |  |  |  |  |  |  |  |  |  |  |

## Schemas, Migrations, Seeds, and Fixtures / Schema、Migration、Seed 与 Fixture

| Path | Type | Applies To | Ordering or Version | Production Use Claim | Evidence | State | Confidence | Gap |
|---|---|---|---|---|---|---|---|---|
|  | Schema / Migration / Seed / Fixture / Generated |  |  |  |  |  |  |  |

## Data Flows / 数据流

| Flow ID | Source | Transform | Destination | Trigger | Failure Handling | Sensitive Boundary Claim | Evidence | Confidence | Next Verification |
|---|---|---|---|---|---|---|---|---|---|
| DATA-001 |  |  |  |  |  |  |  |  |  |

## Settings and Data Findings / 设置与数据发现

| Finding ID | Type | Claim | Impact | Evidence | Confidence | Next Verification | Disposition |
|---|---|---|---|---|---|---|---|
| SD-001 | Orphan Setting / Missing Example / Undocumented Data / Conflicting Precedence / Missing Owner / Unknown Retention |  |  |  |  |  | Decision / Bug / Feature / Backlog / Accept Risk |

## Completion / 完成

```text
Setting names inventoried:
Data stores inventoried:
Schemas and migrations reviewed:
Secret values copied into report: No
Critical unknown owners:
High-impact low-confidence findings:
Ready for baseline: Yes / No
```
