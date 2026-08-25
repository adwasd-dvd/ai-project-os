# TRACEABILITY

Traceability keeps requirement, Linear, implementation, evidence, tests, human UAT, and release claims in one auditable chain.

Traceability 把需求、Linear、实现、证据、测试、人工 UAT 和 release 声明串成一条可审计证据链。

## Chain / 证据链

```text
Requirement
-> Feature ID
-> Linear Issue
-> Change Impact
-> Code / Evidence Paths
-> Automated Tests
-> Human UAT
-> PR / Commit
-> Tag / GitHub Release
```

Chat history is context, not sufficient release evidence.

聊天记录可以提供上下文，但不能单独作为 release 证据。

## Trace States / 追踪状态

| State | Minimum Evidence / 最低证据 |
|---|---|
| `planned` | Feature ID, target version, requirement source, Linear issue, impact input/report |
| `implemented` | Planned evidence plus code or durable implementation evidence paths |
| `verified` | Implemented evidence plus passing automated tests |
| `uat_pending` | Verified evidence plus an explicit pending human UAT record |
| `accepted` | Human UAT Pass and durable UAT evidence |
| `released` | Accepted evidence plus tag and GitHub Release URL |

States cannot be skipped by changing a string. `tools/trace_project.py` validates the evidence required by the declared state.

不能只改一个字符串就跳过状态。`tools/trace_project.py` 会验证声明状态需要的证据。

## Manifest / 清单

Start from:

```text
project-os/traceability/TRACEABILITY_MANIFEST.example.json
```

Keep project-specific manifests in project memory, normally:

```text
project-os/audit/TRACEABILITY_MANIFEST_<version>.json
```

Each feature records:

- stable Feature ID and target version;
- Linear issue, or in schema v2 an explicit Linear Project/Document equivalent record with ID, URL, and reason when issue creation is unavailable;
- requirement source paths;
- change-impact report;
- code and evidence paths;
- test IDs, paths, and result status;
- human UAT status and evidence;
- Decisions and risks;
- release-level branch, PR, tag, and release evidence.

Schema v2 also separates:

- feature-level UAT evidence;
- version-level UAT evidence;
- GitHub Release state;
- post-release verification state.

An equivalent record is a capacity/permission fallback, not a fake Issue. Never invent a Linear identifier. Create the real Issue later when capacity becomes available and update the manifest.

Schema v2 还会分别记录 Feature 级 UAT、版本级 UAT、GitHub Release 和发布后验证。等价记录只是容量或权限受限时的 fallback，不能伪造 Linear Issue ID；容量恢复后应补建真实 Issue 并更新 manifest。

## Validate and Render / 验证并生成报告

```bash
python3 project-os/tools/trace_project.py --root . trace \
  --manifest project-os/audit/TRACEABILITY_MANIFEST_v0.6.0.json \
  --output project-os/audit/TRACEABILITY_REPORT_v0.6.0.md
```

The command exits `2` when evidence is missing or a declared state is not justified.

当证据缺失或声明状态没有依据时，命令退出码为 `2`。

## Hard Rules / 硬规则

- Automated test Pass never means human UAT Pass.
- `Done` in Linear does not prove a GitHub release exists.
- A PR URL does not prove code is merged.
- A tag without the expected release asset/digest does not complete release closeout.
- Missing paths, duplicate Feature IDs, and cross-version drift are blockers.
- Scope changes and unresolved Decisions must appear in change-impact evidence.

- 自动测试 Pass 永远不等于人工 UAT Pass。
- Linear 的 `Done` 不能证明 GitHub release 存在。
- PR URL 不能证明代码已经 merge。
- 只有 tag、没有预期 release asset/digest，不能完成发布 closeout。
- 路径缺失、Feature ID 重复和跨版本漂移都是 blocker。
- Scope change 与未解决 Decision 必须出现在 change-impact 证据中。
