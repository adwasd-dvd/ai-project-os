# REPO_PUBLICATION_POLICY

This policy governs commits, team sharing, private repositories, public repositories, and release assets.

本政策管理 commit、团队共享、私有仓库、公开仓库和 release asset。

## Publication Profiles / 发布 Profile

| Profile | Intended Use | Default Gate |
|---|---|---|
| `local` | Local analysis before deciding what to share | Review secret candidates; no publication conclusion |
| `private` | Commit or release to an authorized private repository | Block probable secrets and Local Only files |
| `team` | Share with authorized collaborators | Block secrets/local-only material; review private context and Agent docs |
| `public` | Publish source or release publicly | Block secrets/private material; review all project memory and Agent docs |

## Mandatory Gates / 必需门禁

Before committing staged changes to any repository:

```bash
python3 project-os/tools/safety_scan.py \
  --root . \
  --scope staged \
  --profile private \
  --fail-on-block \
  --summary
```

Before public publication:

```bash
python3 project-os/tools/safety_scan.py \
  --root . \
  --scope tracked \
  --profile public \
  --fail-on-block \
  --summary
```

Also run:

```bash
python3 project-os/tools/validate_project_os.py --root . --strict
```

The scanner is not a guarantee that the repository is vulnerability-free. It is one evidence source in a human-controlled publication gate.

Scanner 不保证仓库不存在漏洞。它只是人类控制发布门禁中的一项证据。

## Decision Outcomes / 决定结果

### Go

- no Block finding;
- every Review finding has an explicit owner conclusion;
- destination matches the publication manifest;
- tests, UAT, and release policy pass;
- public publication has explicit human approval.

### Review

- no probable secret is exposed;
- context, ownership, freshness, or public suitability is uncertain;
- a human must classify or sanitize the artifact before Go.

### Block

- probable credential/private key;
- Local Only material is staged, tracked, or included in an artifact;
- public profile includes Private Repo material without a sanitized replacement;
- customer, personal, production, or regulated data may be present;
- release asset shape or source does not match the approved manifest.

## Publication Manifest / 发布清单

Complete `safety/PUBLICATION_MANIFEST.md` for a release or visibility change.

Minimum fields:

```text
Destination Profile:
Repository Visibility:
Commit / Tag:
Included Artifacts:
Excluded Artifacts:
Safety Evidence:
Review Findings:
Block Findings:
Human Approver:
Decision: Go / Review / Block
```

## File Defaults / 文件默认值

| Artifact | Default | Notes |
|---|---|---|
| Real `.env`, private key, token file | Local Only | Never commit |
| `.env.example` containing names/placeholders only | Public Safe after review | No real values |
| `LOCAL_OVERRIDES.md` | Local Only or Private Repo | Public only after project-specific sanitization |
| `project-os/audit/` | Private Repo | Public only if every project-specific fact is intended for disclosure |
| `project-os/discovery/` | Private Repo | Public summary may be derived after review |
| `project-os/safety/` reports | Private Repo | Generated evidence may reveal paths even without values |
| Generic OS policies/templates | Public Safe after review | No company/private assumptions |
| Release zip | Same as approved source/tag | Generate from the distributable template only |

## GitHub Rules / GitHub 规则

- Use a branch and PR for repository changes.
- Keep generated release zips out of Git history; publish them as Release assets.
- Link release notes to a tag and immutable evidence.
- Do not use a development branch as a permanent evidence URL.
- Verify remote visibility before using a private/public profile.
- A private repo still runs the secret gate.
- Public conversion is a separate human-approved operation.

## Remediation / 修复

For a Block finding:

1. Do not publish.
2. Remove the risky artifact from the proposed destination without deleting needed local evidence.
3. Rotate/revoke any potentially exposed credential.
4. Determine whether Git history or already-published assets require cleanup.
5. Add ignore rules or a sanitized template.
6. Re-run the same profile and scope.
7. Record rule ID, path, action, and verification, never the protected value.

## Release Gate / Release 门禁

A release cannot proceed until:

- publication manifest says Go;
- safety scan has zero Block findings;
- all Review findings are resolved by a human;
- validator, tests, archive check, and standalone install check pass;
- UAT explicitly allows the exact version;
- release asset digest is recorded and verified after upload.
