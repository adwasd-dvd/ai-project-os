# UAT v1.0.0 - Internal Stable Rescue

This is the consolidated human acceptance checklist for AIPOS-052 through AIPOS-059 and the v1.0 success standard.

本清单是 AIPOS-052 到 AIPOS-059 以及 v1.0 成功标准的统一人工验收。

## Header / 头部

```text
Version: v1.0.0
Date Prepared: 2026-08-26
Branch: codex/v1.0-internal-stable
Initial Functional Commit: c6317fa
Real-Project UAT Fix Commit: 544cd32
Accepted Package Commit: 817cae8
Accepted Package SHA-256: 6dcec2eae38af467ec68062a5e18be1171152af558578b03323f7a5be1cfdd99
Draft PR: https://github.com/adwasd-dvd/ai-project-os/pull/9
Tester: Owner / dvdTeacher
Result: Pass - release authorized
```

## Success Standard / 成功标准

```text
Drop AI Project OS into a messy mature project. It can whitebox the project,
expose risks and contradictions, build a Linear-managed roadmap,
and guide humans and AI through stable releases.
```

```text
把 AI Project OS 丢进一个已经糊掉的成熟项目里。它能白盒化项目，
暴露风险和矛盾，建立 Linear 管理的路线图，
并带着人类和 AI 稳定发版。
```

## Automated Preflight / 自动预检

| Check | Candidate Result | Status |
|---|---|---|
| Change impact | Seven required areas; gate READY | Pass |
| Candidate traceability | AIPOS-052 through AIPOS-059 at UAT Pending; structural PASS | Pass |
| Source tests | 73/73 | Pass |
| Source strict validator | 0 failures, 0 warnings | Pass |
| Private staged safety | Go; Block 0; Review 0 | Pass |
| Representative messy fixture | combined contradiction, dependency, test, CI, safety, and Git conditions | Pass |
| Real-repository rescue dogfood | READY_FOR_DEVELOPMENT; deterministic run3/run4; verify PASS | Pass |
| Real mature-project UAT | 展会宝 TradeShow Copilot; two OS defects found and fixed; final gate NEEDS_HUMAN_DECISION; Safety Block 0; deterministic rerun; verify PASS; product/external/Linear writes 0 | Pass |
| Candidate determinism | two delayed builds byte-identical | Pass |
| Accepted package digest | `6dcec2eae38af467ec68062a5e18be1171152af558578b03323f7a5be1cfdd99` | Pass |
| Extracted candidate | archive valid; strict validator clean; 73/73 tests | Pass |

## Human UAT Scenarios / 人工验收场景

| ID | Feature | Action Steps / 执行动作 | Expected Result / 期待结果 | Actual | Pass/Fail | Notes |
|---|---|---|---|---|---|---|
| UAT-1001 | AIPOS-052 | Read the mature-project prompt in `QUICKSTART.md`, then read the One Guided Entry section in `RESCUE_PROTOCOL.md`. / 阅读 `QUICKSTART.md` 的混乱项目口令，再阅读 `RESCUE_PROTOCOL.md` 的单一引导入口。 | It is clear that placing `project-os/` in a repository and asking Codex to rescue it starts one inspect/plan/verify workflow, not a manual hunt across many files. / 能清楚理解：把 `project-os/` 放进仓库并要求 Codex 救援，会启动一条 inspect/plan/verify 流程，而不是让用户手工翻很多文件。 | Owner reviewed the guided entry and accepted the workflow. | Pass | Explicit v1.0.0 UAT approval received. |
| UAT-1002 | AIPOS-052/053 | Run `python3 project-os/tools/rescue_project.py --root . inspect --summary` in a suitable test repository, or review the real-repository section of `DOGFOOD_REPORT_v1.0.0.md`. / 在合适测试仓库运行该 inspect 命令，或审查 dogfood 报告的真实仓库部分。 | Inspect writes no evidence, product code, or external state; product file count excludes installed `project-os/`. / Inspect 不写证据、产品代码或外部状态；产品文件数排除已安装的 `project-os/`。 | Real mature-project evidence was reviewed and accepted; product/external writes remained zero. | Pass | Explicit v1.0.0 UAT approval received. |
| UAT-1003 | AIPOS-053/054 | Review the Representative Messy Fixture and Safety Resolution Boundary sections in `DOGFOOD_REPORT_v1.0.0.md`. / 审查 dogfood 报告中的代表性混乱 fixture 和安全解决边界。 | Contradiction, missing lock/tests/CI, unsafe file, and Git overlap remain visible; credential-like values never appear; a current safety Block cannot be signed away. / 矛盾、缺 lock/测试/CI、不安全文件和 Git 重叠保持可见；疑似凭证值不出现；当前安全 Block 不能靠文字签掉。 | Owner accepted the visible findings and enforced safety boundary. | Pass | Known limitations accepted. |
| UAT-1004 | AIPOS-054 | Review the finding fields and gate sequence in `RESCUE_PROTOCOL.md`. / 审查 `RESCUE_PROTOCOL.md` 的发现字段和门禁顺序。 | State, evidence, impact, confidence, bilingual Action Steps/Expected Result, next verification, owner, and blocking gates are distinct; high-impact contradictions/unknowns go to humans instead of being guessed. / State、证据、影响、置信度、双语执行动作/期待结果、下一步验证、Owner 和阻塞门禁彼此清楚；高影响矛盾/未知项交给人类，不由 AI 猜测。 | Owner reviewed and accepted the diagnosis and routing model. | Pass | Explicit v1.0.0 UAT approval received. |
| UAT-1005 | AIPOS-055/057 | Review the roadmap and PM sections described in `RESCUE_EXAMPLE.md` and the real-repository PM result in `DOGFOOD_REPORT_v1.0.0.md`. / 审查救援示例中的路线图/PM 部分和 dogfood 报告中的真实 PM 结果。 | You can tell the current gate, recovery order, completion evidence, Human/Codex/Review queues, blockers, Backlog, and highest-value safe next action. / 能看懂当前门禁、恢复顺序、完成证据、人类/Codex/Review 队列、阻塞、Backlog 和最高价值安全下一步。 | Owner reviewed and accepted the roadmap and proactive PM output. | Pass | Explicit v1.0.0 UAT approval received. |
| UAT-1006 | AIPOS-056 | Review the Linear Boundary section in `RESCUE_EXAMPLE.md` and the Linear facts in `DOGFOOD_REPORT_v1.0.0.md`. / 审查救援示例的 Linear 边界和 dogfood 报告中的 Linear 事实。 | The proposal uses English + Chinese, one Project, one Milestone, Feature IDs, stable keys, Action Steps and Expected Result; writes remain zero even when approval is recorded in input. / 建议使用中英文、一个 Project、一个 Milestone、Feature ID、稳定键、执行动作和期待结果；即使输入记录批准，实际写入仍为零。 | Owner reviewed and accepted the bilingual one-Project Linear boundary. | Pass | Live writes remain separately authorized. |
| UAT-1007 | AIPOS-058 | Review the Determinism And Freshness section in `DOGFOOD_REPORT_v1.0.0.md`. / 审查 dogfood 报告中的确定性与新鲜度部分。 | Two independent full runs are identical; `verify` passes when current and fails after product evidence changes. / 两次独立完整运行完全一致；证据新鲜时 `verify` 通过，产品证据变化后会失败。 | Owner accepted the deterministic rescue and freshness evidence. | Pass | Explicit v1.0.0 UAT approval received. |
| UAT-1008 | AIPOS-059 | Inspect the Draft PR, source/template diff, candidate/package verification, known limitations, and rollback below. / 检查 Draft PR、源码/模板差异、候选包验证、已知限制和下方回滚。 | GitHub remains clean, the zip remains a Release-only artifact, source and extracted suites pass, and merge/tag/Release still wait for explicit Owner approval. / GitHub 保持整洁，zip 仍只作为 Release 资产，源码和解压包测试通过，merge/tag/Release 继续等待 Owner 明确批准。 | Owner approved v1.0.0 release; source remains clean and the zip remains Release-only. | Pass | Authorization: `UAT 通过，允许发布 v1.0.0`. |

## Known Limitations / 已知限制

- Mechanical evidence cannot prove unavailable production behavior; high-impact gaps require human verification.
- Codex still interprets project-specific logic and writes declared contradiction/Decision findings; the deterministic tool validates and routes them but does not replace engineering judgment.
- Product commands and dependency installation are intentionally not executed by rescue inspection.
- Linear rescue output is a proposal only; actual duplicate checks and writes use the separate Linear workflow and authorization.
- The free Linear workspace issue limit requires the attached v1.0 Project Document as the current equivalent requirement record.
- Public/team publication profiles may produce additional Review or Block findings beyond the private candidate gate.
- 机械证据无法证明不可用的生产行为；高影响缺口需要人工验证。
- Codex 仍需解释项目专属逻辑并写入声明矛盾/Decision；确定性工具负责验证和路由，但不能替代工程判断。
- 救援检查有意不运行产品命令或安装依赖。
- Linear 救援输出只是建议；真实重复检查和写入使用独立 Linear 流程及授权。
- 免费 Linear workspace 的 Issue 上限使 v1.0 暂时使用所附 Project Document 作为等价需求记录。
- public/team 发布 profile 可能比 private 候选门禁产生更多 Review 或 Block。

## Rollback / 回滚

Before release, abandon the branch or remove generated rescue evidence. After release, reinstall immutable v0.8.0 on a dedicated branch while preserving `LOCAL_OVERRIDES.md`, audit/Linear history, safety dispositions, discovery evidence, and private runtime context. No tool rewrites Git history or rolls production back automatically.

发布前可放弃分支或删除生成的救援证据。发布后可在专用分支重装不可变的 v0.8.0，同时保留 `LOCAL_OVERRIDES.md`、audit/Linear 历史、安全处置、discovery 证据和私密 runtime context。任何工具都不会自动改写 Git 历史或回滚生产。

## UAT Decision / UAT 决定

Pass:

```text
UAT 通过，允许发布 v1.0.0。
```

Fail:

```text
UAT 未通过，请根据我在 Linear 或 Codex 中的反馈继续修改 v1.0.0。
```

## Sign-off / 签署

```text
Accepted By: dvdTeacher / Owner
Date: 2026-08-26
Decision: Pass - release authorized
Known Limitation Disposition: Accepted for the v1.0.0 internal-stable release
```
