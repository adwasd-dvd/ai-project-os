# CHANGE_IMPACT

Every formal feature needs a change-impact review before implementation changes begin.

每个正式 Feature 在开始实现变更前都需要 change-impact review。

## Required Areas / 必填区域

The input must cover all seven areas:

```text
modules
dependencies
data_security
documentation
tests
uat
rollout_rollback
```

Each impact claim records:

- level: `low`, `medium`, or `high`;
- confidence: `high`, `medium`, `low`, or `unknown`;
- claim;
- evidence and optional repository evidence path;
- next verification.

每条影响结论都要记录级别、置信度、结论、证据和下一步验证。

## Development Blockers / 开发阻塞

The development gate becomes `BLOCKED` when:

- scope expansion is detected without Owner approval;
- an unresolved Decision exists;
- a high-impact claim has low or unknown confidence;
- a required impact area, test plan, UAT plan, rollout, or rollback is missing;
- a referenced evidence path does not exist.

以下情况会阻塞开发：未批准的范围扩大、未解决 Decision、高影响低置信度结论、必填影响/测试/UAT/上线/回滚缺失，或证据路径不存在。

## Use / 使用

Start from:

```text
project-os/traceability/CHANGE_IMPACT_INPUT.example.json
```

Validate and render:

```bash
python3 project-os/tools/trace_project.py --root . impact \
  --input project-os/audit/CHANGE_IMPACT_INPUT_v0.6.0.json \
  --output project-os/audit/CHANGE_IMPACT_REPORT_v0.6.0.md
```

## Test vs. UAT / 测试与 UAT

The test plan proves technical behavior. The UAT plan asks a human to confirm value, usability, wording, workflow, or business acceptance. They must stay separate in the report.

测试计划证明技术行为；UAT 计划由人类确认价值、可用性、文字、流程或业务接受度。二者必须在报告中分开。
