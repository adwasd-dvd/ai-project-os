# PUBLICATION_MANIFEST

Complete this record before a release, repository visibility change, or material team/public share.

在 release、仓库 visibility 变更或重要团队/公开共享前填写本记录。

## Header

```text
Manifest ID:
Prepared Date:
Prepared By:
Destination Profile: local / private / team / public
Repository / Channel:
Repository Visibility:
Commit / Tag:
Release Asset:
Human Approver:
Decision: Go / Review / Block
```

## Scope

```text
Purpose:
Audience:
Included Paths:
Excluded Paths:
Generated Artifact Source:
Rollback Location:
```

## Artifact Classification

| Artifact / Path | Classification | Destination | Evidence | Owner | Included? | Notes |
|---|---|---|---|---|---|---|
|  | Local Only / Team Shared / Private Repo / Public Safe |  |  |  | Yes / No |  |

## Required Evidence

```text
Safety Scan Command:
Safety Evidence Path:
Safety Evidence Hash:
Block Findings: 0 required for Go
Review Findings:
Review Conclusions:
Validator Result:
Test Result:
UAT Result:
Archive / Artifact Check:
Remote Asset Digest:
```

## Agent Documents

| File | Canonical or Wrapper | Classification | Conflict Checked | Public Safe | Owner |
|---|---|---|---|---|---|
|  |  |  | Yes / No | Yes / No / N/A |  |

## Project Memory

```text
Private Audit Included: Yes / No
Discovery Detail Included: Yes / No
Raw Conversation Included: Must be No
Local Overrides Included:
Unresolved High-Impact Gaps:
Human Conclusion:
```

## Go / Review / Block

Go requires:

- zero unresolved Block findings;
- every Review finding has a human conclusion;
- no protected values in reports or artifacts;
- destination matches every included artifact classification;
- validator, tests, UAT, and artifact checks pass;
- public publication is explicitly approved.

```text
Decision:
Decision Evidence:
Approved By:
Approved Date:
Post-Publication Verification:
Rollback Trigger:
```
