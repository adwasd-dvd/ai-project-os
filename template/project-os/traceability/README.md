# Traceability Workspace

This directory contains reusable traceability and change-impact input examples.

本目录保存可复用的 traceability 与 change-impact 输入示例。

- `TRACEABILITY_MANIFEST.example.json`: requirement-to-release manifest.
- `CHANGE_IMPACT_INPUT.example.json`: seven-area pre-development impact input.

Project-specific inputs and generated reports should normally go to `project-os/audit/`. Runtime-only experiments belong in `project-os/runtime/`.

项目自己的输入与生成报告通常放在 `project-os/audit/`；仅运行时实验放在 `project-os/runtime/`。

Read `TRACEABILITY.md` and `CHANGE_IMPACT.md` before using `tools/trace_project.py`.
