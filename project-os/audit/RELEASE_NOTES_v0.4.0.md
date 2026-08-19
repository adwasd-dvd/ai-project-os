# Release v0.4.0

Draft release notes for AI Project OS v0.4.0. Publication requires explicit human UAT approval.

AI Project OS v0.4.0 发布说明草案。正式发布必须获得明确的人类 UAT 批准。

## Summary

v0.4 adds Project Whitebox: a read-only intake phase that turns an existing gray-box repository into an evidence-linked project map before baseline confirmation or implementation.

v0.4 增加 Project Whitebox：在确认 baseline 或开始开发前，用只读方式把既有灰盒仓库整理为可追踪证据的项目地图。

## Included Features

| Feature ID | Linear | Summary |
|---|---|---|
| DEC-007 | DVD-58 | Whitebox evidence and read-only discovery contract |
| AIPOS-024 | DVD-60 | Discovery protocol and evidence-confidence model |
| AIPOS-025 | DVD-59 | Read-only repository scanner and project topology map |
| AIPOS-026 | DVD-63 | Dependency, runtime, and integration mapping |
| AIPOS-027 | DVD-62 | Document, settings, and data inventory |
| AIPOS-028 | DVD-61 | Logic, design-boundary, and contradiction audit |
| AIPOS-029 | DVD-64 | Whitebox import report and Linear project summary |
| AIPOS-030 | DVD-65 | Validator, worked fixture, package, and v0.4 UAT |

## Safety Boundary

- Discovery is read-only by default.
- Findings distinguish Observed, Derived, Claimed, Inferred, Contradicted, and Unknown.
- Reports record confidence, freshness, evidence, and next verification.
- Scanner output may include names and paths, but never secret or environment values.
- Findings require human confirmation before they become an approved baseline or implementation scope.

## Known Limitations

- v0.4 inventories potential security-sensitive surfaces but does not replace the v0.5 repository safety gate.
- Static discovery cannot prove runtime behavior without tests, logs, or human evidence.
- The scanner recognizes common manifests and layouts; uncommon project conventions may require manual additions.
- Automated scheduled execution remains planned for v0.6.

## UAT Result

```text
Pending human UAT.
等待人类 UAT。
```

## Verification

See `project-os/audit/UAT_v0.4.0.md` for commands and human scenarios.

Codex verification result:

```text
Strict validators: 0 failures, 0 warnings
Scanner tests: 8 passed
Python compilation: Passed
Repository scan: 99 files, 0 secret-like paths, no secret values emitted
Release archive test: Passed
git diff --check: Passed
```

## GitHub

```text
Branch: codex/v0.4-whitebox
PR: https://github.com/adwasd-dvd/ai-project-os/pull/2 (Draft)
Implementation commit: 168ea9266e5dfb8bd60f3029e10995972d16d89d
Tag: Not created
Release: Not published
Release asset: releases/ai-project-os-v0.4.0.zip (local, ignored by Git)
Candidate SHA-256: 6d9a88e4ee42cb653ea23faa3b182ecace30de76dd337d252ac8e7c67d60bdb6
```
