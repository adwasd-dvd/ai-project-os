# Release v0.4.0

Release notes for AI Project OS v0.4.0.

AI Project OS v0.4.0 发布说明。

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
Pass - approved by Owner on 2026-08-19.
通过 - Owner 于 2026-08-19 批准。
```

## Verification

See `project-os/audit/UAT_v0.4.0.md` for commands and human scenarios.

Codex verification result:

```text
Strict validators: 0 failures, 0 warnings
Automated tests: 10 passed (8 scanner + 2 validator-layout)
Python compilation: Passed
Repository scan: 101 files, 0 secret-like paths, no secret values emitted
Release archive test: Passed
Extracted standalone package strict validation: Passed
git diff --check: Passed
```

## GitHub

```text
Branch: codex/v0.4-whitebox
PR: https://github.com/adwasd-dvd/ai-project-os/pull/2
Tag: v0.4.0
Release: https://github.com/adwasd-dvd/ai-project-os/releases/tag/v0.4.0
Release asset: ai-project-os-v0.4.0.zip
Release SHA-256: 7482351b91167e624efda97fb518d2f6a0690c39c1c7bbd4f1d5987744d90477
```
