# DOGFOOD REPORT v0.8.0

This report records an isolated upgrade of a real v0.6.0 package to the committed v0.8.0 candidate package.

本报告记录一次隔离环境中的真实升级：从 v0.6.0 正式包升级到已提交的 v0.8.0 候选包。

## Inputs / 输入

```text
Installed package: ai-project-os-v0.6.0.zip
Target package: ai-project-os-v0.8.0.zip
Target source commit: 6ea9e8fe4b004f415c530a118f9f28fa02931e11
Target SHA-256: ec81d2439a4802fc19e1d03cc3a9b7bd739c7c92cd37af4134385d016bd3df92
Upgrade branch: codex/upgrade-dogfood
Plan ID: aipos-upgrade:cc8564271fbbdbf21ecaef44
```

## Plan Result / 计划结果

| Classification | Count | Result |
|---|---:|---|
| Add | 13 | Ready |
| Identical | 54 | Ready |
| Safe update | 17 | Ready |
| Migrate | 1 | Ready |
| Preserve | 4 | Ready |
| Conflict | 0 | Ready |

The plan was generated from installed, base, and target trees. It contained no ambiguous or both-modified conflict.

计划由 installed、base、target 三棵目录生成，没有歧义或双方同时修改冲突。

## Apply And Restart / 应用与重复执行

- First apply: `applied_pending_verification`; every planned write completed.
- Second apply: changed paths reported `already_applied`; preserved and identical paths remained unchanged.
- Verification: `pass`; no finding.
- The tool did not merge, tag, publish, rewrite Git history, or execute rollback.

- 第一次执行：全部计划动作完成，等待验证。
- 第二次执行：已变更路径均报告 `already_applied`，保留项和相同项保持不变。
- 验证：`pass`，无发现。
- 工具没有合并、打 tag、发布、改写 Git 历史或自动回滚。

## Protected Memory / 受保护项目记忆

Only SHA-256 values are recorded. No protected file content is included in this report.

本报告只记录 SHA-256，不包含任何受保护文件内容。

| Protected Area | Classification | Before SHA-256 | After SHA-256 | Result |
|---|---|---|---|---|
| `LOCAL_OVERRIDES.md` | Preserve | `8affdfe427d78771427f98990afe66f19927db81a4ddf72af3448f09f92babd4` | `8affdfe427d78771427f98990afe66f19927db81a4ddf72af3448f09f92babd4` | Byte-identical |
| `audit/LINEAR_IMPORT_PLAN.md` | Preserve | `3519d3faeb0a0551acb5efd870784893fda677ede68cf3424ab1055c485e9e21` | `3519d3faeb0a0551acb5efd870784893fda677ede68cf3424ab1055c485e9e21` | Byte-identical |
| `safety/PUBLICATION_MANIFEST.md` | Preserve | `1b99cb283a2989056a638ab04260f1a7cac5dc00936d23b6287786dabd18f61b` | `1b99cb283a2989056a638ab04260f1a7cac5dc00936d23b6287786dabd18f61b` | Byte-identical |
| `runtime/private-note.md` | Preserve | `895339336a5d8f2c0b533835789521326370898892d3d9e2e600fe4f542fdc93` | `895339336a5d8f2c0b533835789521326370898892d3d9e2e600fe4f542fdc93` | Byte-identical |

## Upgraded Installation Verification / 升级后验证

```text
Strict validator: 0 failures, 0 warnings
Full tests: 59/59 passed
Private worktree safety gate: Go; Block 0; Review 0
Package archive check: pass
Repeated candidate builds: byte-identical
Extracted candidate strict validator: 0 failures, 0 warnings
Extracted candidate tests: 59/59 passed
```

## Final Release-Metadata Package / 最终发布元数据安装包

After human UAT, only release-state metadata changed in the distributable template: OS version history, changelog status, and roadmap status. No release or upgrade behavior changed.

人工 UAT 后，分发模板只更新了发布状态元数据：OS 版本历史、changelog 状态和 roadmap 状态；发布或升级行为没有变化。

```text
Final package source commit: 2a93fdc
Two final builds: byte-identical
Final SHA-256: cf9989b993b28689da367d532db233a6d369a8edbe041712951ddc5e99cdfc1f
Archive integrity: pass
Extracted strict validator: 0 failures, 0 warnings
Extracted tests: 59/59 passed
```

## Conclusion / 结论

Automated dogfood passed. The candidate is technically ready for consolidated human UAT; this is not human acceptance and does not authorize release.

自动 dogfood 已通过。候选版在技术上可以进入集中人工 UAT；本结论不等于人工验收，也不授权发布。
