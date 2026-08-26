# Release v0.8.0

Release notes for AI Project OS v0.8.0 Development Train B.

AI Project OS v0.8.0 Development Train B 发布说明。

## Summary / 摘要

v0.8 makes release readiness, human acceptance, recovery, and OS upgrades explicit and testable. It adds deterministic release evidence, feedback routing, post-release verification, installed/upstream version discovery, three-way upgrade planning, guarded branch-based migration, protected-memory preservation, and a real v0.6-to-v0.8 dogfood upgrade.

v0.8 把发布就绪、人工验收、恢复和 OS 升级变成明确、可测试的流程。它增加确定性的发布证据、反馈路由、发布后验证、已安装/上游版本发现、三方升级计划、受门禁保护的分支迁移、项目记忆保护，以及真实的 v0.6 到 v0.8 dogfood 升级。

## Included Features / 包含功能

| Feature ID | Linear Record | Summary / 摘要 |
|---|---|---|
| AIPOS-045 | Train B Feature Register | Release lifecycle and structured human UAT evidence / 发布生命周期与结构化人工 UAT 证据 |
| AIPOS-046 | Train B Feature Register | Deterministic release readiness and notes / 确定性发布就绪与说明 |
| AIPOS-047 | Train B Feature Register | Feedback classification, rollback guidance, and post-release receipt / 反馈分类、回滚指导和发布后收据 |
| AIPOS-048 | Train B Feature Register | Installed/upstream version discovery / 已安装与上游版本发现 |
| AIPOS-049 | Train B Feature Register | Three-way upgrade plan and conflict report / 三方升级计划与冲突报告 |
| AIPOS-050 | Train B Feature Register | Guarded apply, idempotent restart, and verification / 受控应用、幂等重启与验证 |
| AIPOS-051 | Train B Feature Register | Isolated dogfood, deterministic package, Draft PR, and consolidated UAT / 隔离 dogfood、确定性安装包、Draft PR 与集中 UAT |

## What Users Get / 用户得到什么

- A release-readiness report that blocks on missing UAT, safety, package, rollback, test, traceability, or PR evidence.
- Release notes generated from the same structured input as the readiness gate.
- Feedback classification for current fixes, hotfixes, patches, carry-over revalidation, next-version work, Backlog, and Decisions.
- Sanitized post-release verification with tag, URL, local/remote digest, checks, and rollback target.
- Version discovery from a directory, zip, metadata file, or configured GitHub Release.
- A deterministic installed/base/target upgrade plan with add, update, migrate, preserve, conflict, and removal-candidate classes.
- Explicit preservation for local overrides, audit/Linear history, safety dispositions, discovery evidence, and private runtime context.
- Branch, authorization, freshness, source-integrity, path-confinement, idempotency, verification, and rollback gates.

## Verification / 验证

```text
Change-impact gate: READY
Source strict validator: 0 failures, 0 warnings
Source automated tests: 59/59 passed
Candidate builds: byte-identical
Candidate SHA-256: ec81d2439a4802fc19e1d03cc3a9b7bd739c7c92cd37af4134385d016bd3df92
Extracted candidate: archive valid; strict validator clean; 59/59 tests passed
Dogfood: v0.6.0 -> v0.8.0 apply + idempotent restart + verify passed
Protected memory: 4/4 before/after digests byte-identical
Human UAT: Pass - Owner approved 2026-08-26
```

## Known Limitations / 已知限制

- GitHub latest-release discovery requires network access.
- Ambiguous both-modified files intentionally block for human review.
- OS upgrade does not modify project product code or automatically resolve business decisions.
- Production rollback, Git history rewrite, merge, tag, Release, and UAT approval remain human-controlled.
- The Linear free workspace issue limit required one Project Document as the temporary equivalent record for the seven Train B features.

## Rollback / 回滚

Return to the immutable v0.6.0 package on a dedicated branch while preserving project-specific memory. Run strict validation, all tests, safety gates, and project UAT before accepting the rollback. The tool supplies evidence and guidance; it never rewrites Git history or rolls production back automatically.

在专用分支上恢复不可变的 v0.6.0 安装包，同时保留项目自己的记忆。接受回滚前运行严格验证、全部测试、安全门和项目 UAT。工具只提供证据和指导，不会自动改写 Git 历史或回滚生产。

## Release State / 发布状态

Human UAT passed and the Owner authorized merge, tag, and GitHub Release to the verified private destination.

人工 UAT 已通过，Owner 已授权向已验证的 private 目标执行 merge、tag 和 GitHub Release。

Draft PR: https://github.com/adwasd-dvd/ai-project-os/pull/7
