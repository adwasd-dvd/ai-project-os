# Release Workspace / 发布工作区

Reusable structured inputs for `tools/release_project.py` live here.

这里保存 `tools/release_project.py` 的可复用结构化输入。

- `RELEASE_INPUT.example.json`: release readiness and release-notes input.
- `FEEDBACK_TRIAGE.example.json`: patch/hotfix/carry-over/Decision classification input.
- `POST_RELEASE_INPUT.example.json`: sanitized post-release verification input.

Project-specific release inputs, reports, UAT, and closeout records belong in `project-os/audit/`. Temporary runs belong in ignored `project-os/runtime/`.

项目专属 release 输入、报告、UAT 和关账记录应进入 `project-os/audit/`；临时运行结果进入已忽略的 `project-os/runtime/`。

Read `RELEASE_CONTROL.md`, `RELEASE_POLICY.md`, and `REPO_PUBLICATION_POLICY.md` first.
