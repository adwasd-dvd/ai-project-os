# Upgrade Workspace / 升级工作区

This directory contains reusable configuration and safe fixtures for `tools/upgrade_project_os.py`.

本目录保存 `tools/upgrade_project_os.py` 的可复用配置与安全 fixture。

- `UPGRADE_CONFIG.example.json`: local installed/base/target package comparison and guarded apply policy.
- `UPSTREAM_GITHUB.example.json`: read-only latest GitHub Release inspection.
- `fixtures/upstream_release.json`: offline metadata inspection fixture.

Project-specific plans and conflict reports belong in `project-os/audit/`. Apply and verify receipts must stay in ignored `project-os/runtime/`.

项目专属计划和冲突报告进入 `project-os/audit/`；apply/verify 回执必须留在已忽略的 `project-os/runtime/`。

Read `UPGRADE_POLICY.md`, `SECURITY_BOUNDARY.md`, and `AGENT_DOC_POLICY.md` before planning or applying an upgrade.
