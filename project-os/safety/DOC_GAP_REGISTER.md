# DOC_GAP_REGISTER

Track project knowledge that is missing, stale, duplicated, contradictory, orphaned, unsafe, or trapped in chat.

跟踪缺失、过期、重复、矛盾、孤立、不安全或只存在于聊天中的项目知识。

## Gap Types

```text
Missing: required knowledge does not exist
Stale: document freshness is insufficient
Contradicted: authoritative sources disagree
Duplicated: multiple sources may drift
Orphaned: no owner or maintenance path
Chat Only: decision exists only as a sanitized conversation claim
Unsafe Location: knowledge exists where it should not be stored/shared
Unverified: claim lacks adequate evidence
```

## Gap Register

| Gap ID | Type | Description | Evidence | Impact | Classification | Owner | Target Version | Next Verification | Status |
|---|---|---|---|---|---|---|---|---|---|
| GAP-001 |  |  |  |  | Local Only / Team Shared / Private Repo / Public Safe |  |  |  | Open |

## Routing

| Condition | Default Route |
|---|---|
| Blocks security, publication, data handling, or UAT | Decision or blocking verification issue |
| Confirmed behavior differs from approved expectation | Bug |
| Missing user-visible capability | Feature |
| Stale/duplicate documentation only | Chore |
| Important but unplanned | Backlog with owner and evidence |
| Low-impact unknown | Keep in verification queue |

## Required Fields For High Impact

```text
Gap ID:
State:
Evidence:
Evidence Freshness:
Confidence:
Impact:
Classification:
Owner:
Decision Needed:
Next Verification:
Target Version:
```

## Closure Rule

A gap closes only when:

- the authoritative source is named;
- the contradiction or missing knowledge is resolved;
- the destination classification is safe;
- affected requirements/issues/docs are updated;
- evidence and verification are linked;
- the human Owner accepts high-impact closure.

Do not close a gap merely because a new document was created.

不能因为创建了新文档就关闭 gap。
