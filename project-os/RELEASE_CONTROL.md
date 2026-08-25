# RELEASE_CONTROL

This file defines the executable Train B release, recovery, and post-release evidence flow.

本文件定义 Train B 可执行的发布、恢复与发布后证据流程。

## Lifecycle Separation / 生命周期分离

```text
implemented -> verified -> uat_pending -> accepted -> released
                                                     -> post_release pending/pass/fail
```

- `implemented`: durable implementation evidence exists.
- `verified`: automated tests pass.
- `uat_pending`: a human UAT plan exists and waits for a person.
- `accepted`: human UAT Pass includes actor, date, scenarios, evidence, and limitation disposition.
- `released`: accepted evidence plus an immutable tag and GitHub Release URL.
- `post_release`: separate verification after publication; it never rewrites the meaning of UAT or Release.

- `implemented`：已有持久实现证据。
- `verified`：自动测试通过。
- `uat_pending`：已有人工 UAT 计划并等待人类。
- `accepted`：人工 UAT Pass 包含验收人、日期、场景、证据和遗留项处置。
- `released`：Accepted 证据加不可变 tag 与 GitHub Release URL。
- `post_release`：发布后的独立验证，不会改写 UAT 或 Release 的含义。

Automated tests, Linear `Done`, a PR, or a generated report can never create human UAT Pass.

自动测试、Linear `Done`、PR 或生成报告永远不能产生人工 UAT Pass。

## Release Plan / 发布计划

Start from `release/RELEASE_INPUT.example.json` and run:

```bash
python3 project-os/tools/release_project.py --root . plan \
  --input project-os/release/RELEASE_INPUT.example.json \
  --report project-os/runtime/RELEASE_READINESS.md \
  --notes project-os/runtime/RELEASE_NOTES_DRAFT.md
```

The command is deterministic and local. It does not mutate Git, GitHub, Linear, tags, Releases, credentials, or production.

命令是确定性且只在本地生成证据；不会修改 Git、GitHub、Linear、tag、Release、凭证或生产环境。

`READY` requires:

- exact Included Feature and traceability alignment;
- accepted/released Feature states;
- explicit human version UAT Pass;
- READY change-impact report;
- safety `Go`, Block 0, and disposition for Review findings;
- passing tests with evidence paths;
- deterministic package SHA-256 and extracted validation;
- rollback target, plan, authority, and verification;
- GitHub branch and PR evidence.

任何缺失或冲突都会返回 `BLOCKED` 并显示下一步，不会“尽量发布”。

## Feedback Classification / 反馈分类

Use `release/FEEDBACK_TRIAGE.example.json`:

```bash
python3 project-os/tools/release_project.py --root . classify \
  --input project-os/release/FEEDBACK_TRIAGE.example.json
```

Possible results:

```text
current_fix
hotfix
patch
carry_over
next_version
backlog
decision
```

Completed old-version scope plus later-version feedback must become `carry_over`; do not move the old Issue.

旧版本原范围已完成但出现下版本反馈时，必须归类为 `carry_over`，不得移动旧 Issue。

## Rollback Boundary / 回滚边界

The tool may generate a rollback plan and post-release receipt. It never:

- rolls back production automatically;
- deletes a GitHub Release;
- moves or rewrites a tag;
- rewrites Git history;
- rotates credentials;
- removes files or project memory automatically.

工具可以生成回滚计划和发布后回执，但绝不自动回滚生产、删除 Release、移动 tag、改写历史、轮换凭证或删除项目记忆。

## Post-Release Verification / 发布后验证

After the human-authorized release transaction, populate `release/POST_RELEASE_INPUT.example.json` with observed metadata and run:

```bash
python3 project-os/tools/release_project.py --root . post-release \
  --input project-os/release/POST_RELEASE_INPUT.example.json \
  --output project-os/runtime/POST_RELEASE_RECEIPT.md
```

The local and remote asset digests must match and every declared check must pass. Receipts contain metadata only; raw payloads, tokens, comment bodies, file content, and source lines are rejected.

本地与远端资产摘要必须一致，所有检查必须通过。回执只记录元数据；raw payload、token、评论正文、文件内容和源代码行都会被拒绝。
