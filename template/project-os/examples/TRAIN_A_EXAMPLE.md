# Development Train A Worked Example

This example shows one full safe loop from Linear intake to change impact and traceability without using a live credential.

本示例展示从 Linear intake 到 change impact 和 traceability 的完整安全闭环，不需要真实凭证。

## Scenario / 场景

The fixture contains seven issues:

| Issue | State | Expected Route / 期待路由 |
|---|---|---|
| EX-901 | Todo + unassigned + Ready fields | Codex Queue |
| EX-902 | Todo + assigned | Human Queue |
| EX-903 | In Review + assigned | Review Queue |
| EX-904 | In Review + unassigned | Inconsistent; recommend a human reviewer |
| EX-905 | Done in v0.5 + recent v0.6 revalidation comment | Closed Watch; preserve old scope and carry over |
| EX-906 | Todo + unassigned but missing ID/version/acceptance | Blocked/Ambiguous |
| OTHER-999 | Different product | Skipped outside scope |

## 1. Run Intake / 执行 Intake

```bash
python3 project-os/tools/linear_intake.py --root . scan \
  --config project-os/automation/linear_intake.example.json \
  --snapshot project-os/automation/fixtures/train_a_snapshot.json \
  --as-of 2026-08-24T18:00:00Z \
  --markdown-out project-os/examples/TRAIN_A_INTAKE_REPORT.md
```

Observed result / 观察结果：

- Six in-scope issues were scanned and one issue was skipped.
- All expected queues appeared.
- EX-905 was classified `carry_over_revalidation`; the old issue was not moved.
- EX-906 listed three Ready blockers.
- Three advisory actions received stable idempotency keys.
- No Linear mutation ran: `Write Actions: None. Dry run only.`

- 扫描了六个范围内 issue，跳过一个其他产品 issue。
- 所有期待队列都出现。
- EX-905 被分类为 `carry_over_revalidation`，旧 issue 没有被移动。
- EX-906 列出三个 Ready blocker。
- 三个 advisory action 获得稳定幂等 key。
- 没有执行 Linear mutation。

Full generated output / 完整生成输出：`examples/TRAIN_A_INTAKE_REPORT.md`。

## 2. Interpret the Handoff / 理解交接

The scheduled worker does not start EX-901. It tells the Owner or interactive Codex task:

定时 worker 不会自己开始 EX-901。它只告诉 Owner 或交互式 Codex task：

```text
Interactive Codex may start EX-901 after confirming local context.
交互式 Codex 确认本地上下文后可开始 EX-901。
```

EX-902 and EX-903 remain human-owned because they have assignees. EX-904 is not silently accepted; it needs a reviewer. EX-905 needs a new carry-over issue or confirmed target, not a reopened historical issue.

## 3. Check Change Impact / 检查变更影响

```bash
python3 project-os/tools/trace_project.py --root . impact \
  --input project-os/traceability/CHANGE_IMPACT_INPUT.example.json \
  --output project-os/examples/CHANGE_IMPACT_REPORT.md
```

The example covers all seven required areas and returns `Development Gate: READY`. Changing `scope_change` to true, adding an unresolved Decision, or making a high-impact claim low-confidence changes the gate to `BLOCKED`.

示例覆盖全部七个必填区域并返回 `READY`。如果扩大 scope、加入未解决 Decision，或把高影响结论设为低置信度，gate 会变为 `BLOCKED`。

## 4. Check Traceability / 检查追踪链

```bash
python3 project-os/tools/trace_project.py --root . trace \
  --manifest project-os/traceability/TRACEABILITY_MANIFEST.example.json \
  --output project-os/examples/TRACEABILITY_REPORT.md
```

The example feature is only `planned`, so it does not claim implementation, test, UAT, or release evidence. Later states add stricter requirements:

示例 Feature 只有 `planned`，因此不会声称已经实现、测试、UAT 或 release。后续状态要求更严格：

```text
verified -> passing automated tests
uat_pending -> explicit pending human UAT
accepted -> human UAT Pass + evidence path
released -> accepted + tag + GitHub Release URL
```

## 5. What an Authorized Apply Would Do / 授权 Apply 会做什么

The dry-run plan contains only advisory comments for the inconsistent, closed-watch, and readiness-gap issues. The example config keeps writes disabled. A real apply requires config enablement, an operation allowlist, `--authorize-writes`, and `AIPOS_LINEAR_WRITE_APPROVED=1`.

Dry-run plan 只为状态不一致、closed-watch 和 Ready 缺口 issue 准备 advisory comment。示例配置保持 writes disabled。真实 apply 必须同时有配置启用、操作白名单、`--authorize-writes` 和 `AIPOS_LINEAR_WRITE_APPROVED=1`。

Repeating an authorized plan skips successful idempotency keys. A failed key can retry without repeating successful writes. The ledger stores no token or comment body.

重复执行已授权 plan 会跳过成功 key；失败 key 可以重试而不重复成功写入。账本不保存 token 或 comment body。

## Human Check / 人工检查

The Owner should be able to answer:

- Which issue can interactive Codex start?
- Which issues are waiting for a human?
- Why is EX-905 not reopened?
- What prevents a scheduled scan from changing code?
- What additional evidence is needed before `accepted` or `released`?

Owner 应能回答：哪个 issue 可交给交互式 Codex、哪些等人类、为何不重开 EX-905、什么阻止定时扫描改代码，以及进入 `accepted`/`released` 还缺什么证据。
