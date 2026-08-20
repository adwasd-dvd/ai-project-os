# SECURITY_BOUNDARY

AI Project OS v0.5 uses this policy to decide what may stay local, enter Git, be shared with a team, or be published.

AI Project OS v0.5 使用本政策判断哪些内容只能留在本地、可以进入 Git、可以团队共享或可以公开。

## Core Rule / 核心规则

```text
Repository visibility is not data classification.
A private repository is not a secret store.
Unknown high-impact material is Review or Block, never automatic Go.
```

```text
仓库 visibility 不等于数据分类。
私有仓库不是 secret store。
高影响未知内容必须 Review 或 Block，不能自动 Go。
```

## Destinations / 目标位置

| Classification | Meaning | Typical Examples | Allowed Destination |
|---|---|---|---|
| Local Only | Must not be committed or shared | Real `.env`, credentials, private keys, cookies, raw production exports, personal notes | Local encrypted/controlled storage only |
| Team Shared | Needed by authorized collaborators, sanitized | Stable team workflow, non-secret environment key names, internal runbook | Approved team system or private repo |
| Private Repo | Useful project evidence that is not public-safe | Internal architecture, audit details, private dependency names, Linear mappings | Authorized private repository |
| Public Safe | Reviewed, generic, and free of private context | Product source intended for release, generic policy, sanitized examples | Public repository or release |

中文分类：

| 分类 | 含义 | 常见示例 | 允许目标 |
|---|---|---|---|
| 仅本地 | 不得提交或共享 | 真实 `.env`、凭证、私钥、cookie、生产导出、个人笔记 | 受控本地存储 |
| 团队共享 | 授权协作者需要，且已脱敏 | 稳定团队流程、非 secret 的环境变量名、内部 runbook | 获批团队系统或私有仓库 |
| 私有仓库 | 对项目有用，但不适合公开 | 内部架构、audit 细节、私有依赖名、Linear mapping | 授权私有仓库 |
| 公开安全 | 已复核、通用、无私有上下文 | 计划发布的源码、通用政策、脱敏示例 | 公开仓库或 release |

## Protected Assets / 受保护资产

- credentials, tokens, passwords, cookies, private keys, and connection strings;
- personal data, customer data, production records, and raw logs;
- private architecture, internal URLs, account identifiers, and commercial terms;
- local user paths, device details, raw conversations, and personal AI memory;
- unresolved security findings whose disclosure could increase risk;
- project decisions that are not yet authorized for the destination.

- 凭证、token、密码、cookie、私钥和连接字符串；
- 个人数据、客户数据、生产记录和原始日志；
- 私有架构、内部 URL、账号标识和商业条款；
- 本地用户路径、设备信息、原始聊天和个人 AI 记忆；
- 披露后可能增加风险的未解决安全发现；
- 尚未获准进入目标位置的项目决定。

## Actors And Trust Boundaries / 角色与信任边界

| Actor or Boundary | Trusted For | Not Automatically Trusted For |
|---|---|---|
| Local Operator | Approving local access and UAT | Public disclosure or credential handling without review |
| Codex | Read-only analysis, sanitized evidence, scoped edits | Self-approving UAT, rotating credentials, publishing unknown material |
| Linear | Workflow, decisions, summaries, status | Secret storage or detailed sensitive evidence |
| Private GitHub repo | Authorized source collaboration | Storing secrets or public-safe classification |
| Public GitHub/Release | Reviewed public artifacts | Internal memory, raw audit data, local overrides |
| Scheduled automation | Approved bounded scans | Surprise code changes, publication, or UAT approval |

## Finding Record / 发现记录

Every important safety conclusion records:

```text
Finding ID:
Claim:
State: Observed / Derived / Claimed / Inferred / Contradicted / Unknown
Evidence:
Evidence Freshness:
Confidence: High / Medium / Low / Unknown
Classification: Local Only / Team Shared / Private Repo / Public Safe
Impact:
Owner:
Disposition: Go / Review / Block
Remediation:
Next Verification:
Secret Values Present: Must be No
```

## Safe Evidence / 安全证据

Allowed:

- rule ID;
- repository-relative path;
- classification and severity;
- whether a file is tracked, staged, or untracked;
- sanitized remediation and next verification;
- counts and deterministic hashes of generated reports.

Not allowed:

- matched secret value;
- matching source line;
- environment-variable value;
- raw private key, cookie, production record, or conversation dump;
- unnecessary absolute user path.

## Stop Conditions / 停止条件

Codex must stop and ask a human when:

- a probable active credential or private key is found;
- material may contain customer, personal, regulated, or production data;
- public publication is requested but classification is missing or contradictory;
- a security-critical claim is Low/Unknown confidence;
- remediation would require deleting evidence, rewriting Git history, rotating credentials, or changing repository visibility;
- an Agent document contains personal memory or conflicting authority.

Codex 必须停止并询问人类，当：

- 发现可能仍有效的凭证或私钥；
- 内容可能包含客户、个人、受监管或生产数据；
- 请求公开发布，但分类缺失或冲突；
- 安全关键结论置信度为 Low/Unknown；
- 修复需要删除证据、重写 Git 历史、轮换凭证或改变仓库 visibility；
- Agent 文档包含个人记忆或权威冲突。

## Secret Incident Rule / Secret 事件规则

If a probable real secret was committed:

1. Do not paste it into Linear, GitHub comments, reports, or chat.
2. Stop publication.
3. Tell the Owner which rule and repository-relative path triggered.
4. Rotate/revoke the credential through the owning provider.
5. Decide whether Git history must be rewritten.
6. Re-run the staged and tracked safety gates.
7. Record only sanitized incident evidence.

发现可能已提交的真实 secret 时：不要复制值，停止发布，通知 Owner 规则和相对路径，通过 provider 轮换/撤销凭证，决定是否重写历史，重新运行门禁，只记录脱敏证据。

## Completion Gate / 完成门槛

Safety classification is complete only when:

- the intended destination is named;
- important artifacts have classification, evidence, owner, and disposition;
- no Block finding remains unresolved;
- Review findings have explicit human conclusions;
- reports contain no protected values;
- public publication has explicit human approval.
