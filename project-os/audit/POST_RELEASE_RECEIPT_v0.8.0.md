# Post-Release Verification Receipt / 发布后验证回执

Version: `v0.8.0`
Result: `PASS`
Tag: `v0.8.0`
Release: https://github.com/adwasd-dvd/ai-project-os/releases/tag/v0.8.0
Asset SHA-256: `cf9989b993b28689da367d532db233a6d369a8edbe041712951ddc5e99cdfc1f`
Rollback Target: `v0.6.0`

## Findings / 发现

- Remote and local release evidence match. / 远端与本地发布证据一致。

## Checks / 检查

- TAG-COMMIT: pass / Tag v0.8.0 and origin/main both resolve to merge commit 4cd2412f06f7fe1e368c1efafa862bd62f560a4e
- REMOTE-ASSET: pass / Downloaded GitHub Release asset is byte-identical to the local package and both digests match
- ARCHIVE-INTEGRITY: pass / Downloaded release archive passed zip integrity verification
- RELEASE-VISIBILITY: pass / GitHub Release is published, non-draft, and non-prerelease
- LINEAR-CLOSEOUT: pass / v0.8.0 Milestone is recorded as released; canonical Project remains In Progress and targets v1.0.0

Receipt content is sanitized metadata only; no token, raw payload, comment body, source line, or file content is stored. / 回执只含脱敏元数据，不保存 token、raw payload、评论正文、源代码行或文件内容。
