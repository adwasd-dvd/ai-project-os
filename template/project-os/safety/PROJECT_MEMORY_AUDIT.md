# PROJECT_MEMORY_AUDIT

Use this report to determine what the project knows, what it merely claims, and what has been lost or left unresolved.

使用本报告判断项目真正知道什么、只是声称什么，以及哪些知识已经丢失或未解决。

## Audit Header

```text
Audit Date:
Repository Commit:
Auditor:
Project Stage:
Safety Profile:
Sources Reviewed:
Raw Conversation Copied: Must be No
Secret Values Present: Must be No
```

## Source Register

| Source | Authority | Freshness | Owner | Evidence | Confidence | Sensitive? | Notes |
|---|---|---|---|---|---|---|---|
| Requirements |  |  |  |  |  |  |  |
| Decisions |  |  |  |  |  |  |  |
| Code and tests |  |  |  |  |  |  |  |
| Git history |  |  |  |  |  |  |  |
| Linear |  |  |  |  |  |  |  |
| Current docs |  |  |  |  |  |  |  |
| Chat-only claims |  |  |  |  |  |  | Summary only; no raw dump |

## Memory Finding States

```text
Observed: directly supported by current evidence
Derived: mechanically computed from evidence
Claimed: stated by a source but not independently confirmed
Inferred: reasoned conclusion requiring verification
Contradicted: authoritative sources disagree
Unknown: important answer is missing
Stale: once useful, but freshness is no longer adequate
Orphaned: no current owner or decision path
Chat Only: exists only as a sanitized conversation claim
```

## Finding Register

| Finding ID | Claim | State | Evidence | Freshness | Confidence | Impact | Classification | Owner | Next Verification |
|---|---|---|---|---|---|---|---|---|---|
| MEM-001 |  |  |  |  |  |  |  |  |  |

## Decision Continuity

| Decision | Current Outcome | Evidence | Implemented In | Still Valid? | Owner | Gap ID |
|---|---|---|---|---|---|---|
|  |  |  |  | Yes / No / Unknown |  |  |

## Requirement To Reality

| Requirement | Documented Behavior | Code/Test Evidence | Runtime Evidence | Conflict | Confidence | Next Verification |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## Chat-Only Claims

Record only a sanitized summary, source date/reference, authority, and verification path. Never paste raw conversations, credentials, personal context, or unrelated content.

仅记录脱敏摘要、来源日期/引用、权威性和验证路径。不得粘贴原始聊天、凭证、个人上下文或无关内容。

| Claim ID | Sanitized Summary | Source Reference | Authority | Confidence | Risk If Lost | Next Verification | Gap ID |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

## Contradictions And Unknowns

| ID | Type | Evidence A | Evidence B / Missing Evidence | Impact | Owner | Decision Needed | Next Verification |
|---|---|---|---|---|---|---|---|
|  | Contradicted / Unknown |  |  |  |  |  |  |

## Continuity Conclusion

```text
High-Impact Gaps:
Blocking Contradictions:
Unowned Decisions:
Chat-Only Risks:
Safe To Baseline: Yes / No / With Conditions
Safe To Publish: Yes / No / Separate Review Required
Required Human Decisions:
```
