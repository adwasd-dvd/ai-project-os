# Rescue Evidence / 救援证据

This directory contains the v1.0 mature-project rescue input and generated evidence package.

本目录保存 v1.0 成熟项目救援输入和生成的证据包。

## Start / 启动

```bash
python3 project-os/tools/rescue_project.py --root . inspect --summary
```

After Codex prepares `RESCUE_INPUT.json` from `RESCUE_INPUT.example.json`:

Codex 根据模板准备 `RESCUE_INPUT.json` 后：

```bash
python3 project-os/tools/rescue_project.py --root . plan \
  --input project-os/rescue/RESCUE_INPUT.json \
  --profile private --write --summary
```

## Boundaries / 边界

- `inspect` is read-only.
- `plan` is read-only unless `--write` is explicit.
- `--write` writes generated evidence in this directory only.
- Product and external writes remain zero.
- Linear output is a dry-run proposal; approval and actual import are separate.
- `inspect` 只读。
- `plan` 默认只读，只有明确使用 `--write` 才写证据。
- `--write` 只在本目录写入生成证据。
- 产品和外部写入保持为零。
- Linear 输出是 dry-run 建议；批准与实际导入是独立步骤。

Read `../RESCUE_PROTOCOL.md` for gates, evidence fields, stop conditions, and human handoffs.

门禁、证据字段、停止条件和人工交接见 `../RESCUE_PROTOCOL.md`。
