# UAT v0.4.0

This record must be completed by a human Owner or delegated UAT reviewer.

本记录必须由人类 Owner 或被授权的 UAT reviewer 完成。

## UAT Header

```text
Version: v0.4.0
Date: 2026-08-19
Environment: local repo + Linear DvdTeacher + GitHub Draft PR
Build / Commit: Pending GitHub Draft PR
Tester: Owner / dvdTeacher
Owner: dvdTeacher
Result: Pending
```

## Version Goal

Recover a difficult existing project into an evidence-linked whitebox map without changing its code, leaking secrets, or treating guesses as facts.

在不修改项目代码、不泄露秘密、不把推测当事实的前提下，把难以理解的既有项目恢复成有证据链的白盒地图。

## Codex Verification To Run

```text
python3 project-os/tools/validate_project_os.py --root . --strict
python3 template/project-os/tools/validate_project_os.py --root . --strict
python3 -m unittest project-os/tools/test_whitebox_scan.py template/project-os/tools/test_whitebox_scan.py
python3 -m py_compile project-os/tools/validate_project_os.py project-os/tools/whitebox_scan.py project-os/tools/test_whitebox_scan.py template/project-os/tools/validate_project_os.py template/project-os/tools/whitebox_scan.py template/project-os/tools/test_whitebox_scan.py
python3 project-os/tools/whitebox_scan.py --root . --summary
unzip -t releases/ai-project-os-v0.4.0.zip
git diff --check
```

## Human UAT Scenarios

| Scenario ID | Feature ID | Action Steps / 执行动作 | Expected Result / 期待结果 | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|
| WBX-001 | AIPOS-024 | Read `WHITEBOX_PROTOCOL.md`; compare all evidence states and stop conditions / 阅读协议并比较证据状态与停止条件 | Facts, claims, inference, conflict, unknowns, confidence, and human gate are distinct / 各类证据、置信度和人类门槛清晰可分 |  |  |  |
| WBX-002 | AIPOS-025 | Run scanner without `--write`; check working tree / 运行不带 `--write` 的扫描并检查工作树 | JSON or summary is returned and no repository file is written / 返回结果且不写入仓库 |  |  |  |
| WBX-003 | AIPOS-025 | Run scanner with `--write` in an allowed output directory, then `--check` / 在允许目录写入后执行检查 | One deterministic `SCAN_EVIDENCE.json` is created and check passes / 只生成确定性的证据文件且检查通过 |  |  |  |
| WBX-004 | AIPOS-026 | Inspect dependency report against a known manifest / 将依赖报告与已知 manifest 对照 | Manifest, dependency names, runtimes, services, and unknowns are visible without values / 能看到名称、运行环境和未知项且无敏感值 |  |  |  |
| WBX-005 | AIPOS-027 | Inspect document and settings/data reports / 检查文档与设定数据报告 | Authority, freshness, conflicts, config names, stores, schemas, and flows have explicit evidence / 权威性、新鲜度、冲突和数据流均有证据字段 |  |  |  |
| WBX-006 | AIPOS-028 | Record one contradiction and one unknown in the logic audit / 在逻辑审计中记录一个冲突和一个未知项 | Neither is silently converted into an implementation requirement; each has next verification / 不会直接变成开发需求，且都有下一步验证 |  |  |  |
| WBX-007 | AIPOS-029 | Read the copy-ready Linear summary / 阅读可复制到 Linear 的摘要 | Summary links evidence, shows confidence and risk, and excludes secret values / 摘要链接证据、展示置信度风险且不含秘密值 |  |  |  |
| WBX-008 | AIPOS-030 | Run validators and scanner tests / 运行 validator 和 scanner tests | All checks pass for source and distributable template / 源项目与分发模板全部通过 |  |  |  |
| WBX-009 | AIPOS-030 | Open the release zip and inspect its root / 打开发布 zip 并检查根目录 | Archive contains one top-level `project-os/` and no dogfood release/audit history / 只有顶层 `project-os/` 且不带本项目发布历史 |  |  |  |
| WBX-010 | AIPOS-030 | Read `examples/WHITEBOX_EXAMPLE.md` end to end / 完整阅读示例 | A new operator can follow scan, mapping, contradiction, Linear proposal, and human gate / 新操作者能照例完成扫描、映射、冲突、Linear 建议和人类确认 |  |  |  |

## Issues Found

| ID | Description | Severity | Category | Target Version | Linear Issue | Owner |
|---|---|---|---|---|---|---|
|  |  |  | Current Fix / Patch / Next / Backlog / Decision |  |  |  |

## Final UAT Decision

Pass:

```text
UAT 通过，允许发布 v0.4.0。
```

Fail:

```text
UAT 未通过，必须先处理以下问题：
-
```

## Sign-off

```text
Accepted By:
Date:
Notes:
```
