# SECRET_SCAN_REPORT

This is the sanitized human report for repository safety evidence. Never paste matched values or matching source lines.

本文件是仓库安全证据的脱敏人工报告。不得粘贴命中值或命中源码行。

## Header

```text
Scan Date:
Repository Commit:
Scanner Version:
Scope: worktree / staged / tracked
Profile: local / private / team / public
Command:
Evidence Path:
Evidence Hash:
Matched Values Emitted: Must be No
Source Lines Emitted: Must be No
Environment Values Emitted: Must be No
```

## Summary

```text
Files Considered:
Files Scanned:
Block Findings:
Review Findings:
Info Findings:
Gate Result: Go / Review / Block
```

## Findings

| Finding ID | Rule ID | Repository-Relative Path | Severity | Classification | Disposition | Tracked/Staged | Remediation | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  | Local Only / Team Shared / Private Repo / Public Safe | Block / Review / Info |  |  |  | Open |

Do not add:

- the value that matched;
- the matching line;
- a private-key body;
- an environment value;
- customer/production data;
- raw chat content.

不得添加命中值、命中行、私钥正文、环境变量值、客户/生产数据或原始聊天内容。

## Review Conclusions

| Finding ID | Human Conclusion | Evidence | Approved Destination | Approved By | Date |
|---|---|---|---|---|---|
|  | False Positive / Sanitized / Local Only / Removed / Rotated / Other |  |  |  |  |

## Credential Response

If a probable active credential was found:

```text
Publication Stopped: Yes
Owner Notified: Yes
Provider Rotation/Revocation Required:
Git History Review Required:
Published Asset Review Required:
Sanitized Evidence Recorded:
Re-scan Result:
```

Never record the credential itself.

## Final Decision

```text
Decision: Go / Review / Block
Unresolved Block Findings:
Unresolved Review Findings:
Human Approver:
Next Action:
```
