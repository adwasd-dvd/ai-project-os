# FIRST_PROJECT Example

本文是 AI Project OS v0.3 的第一个真实项目 walkthrough。

示例项目：

```text
Tiny Lesson Tracker
```

它是一个小型课程记录应用，有登录、课程列表、学习进度和导出功能。这个示例不要求真实代码存在，重点是展示用户和 Codex 怎么配合。

## 1. 安装 OS

把 `project-os/` 放到目标仓库根目录：

```text
tiny-lesson-tracker/
├── project-os/
├── src/
├── tests/
└── package.json
```

用户在本地 Codex 输入：

```text
请读取 project-os/START_HERE.md、project-os/SELF_CHECK.md、project-os/AGENTS.md、project-os/BOOTSTRAP.md。

请按 AI Project OS v0.3 工作。

先执行 Phase 0 Self-Check。
如果 Phase 0 没有阻塞项，再进入 Phase 1 Audit。
```

## 2. Phase 0 Self-Check

Codex 应检查：

- 当前目录是否是项目根目录。
- Git/GitHub remote 是否存在。
- `project-os/` 是否完整。
- Linear 是否可用。
- Linear Issue 描述语言，默认 `English + Chinese`。
- 测试、构建、lint 和环境变量入口。

Codex 输出示例：

```text
Phase 0 Self-Check complete.

Can start Phase 1 Audit: Yes

Blocking items:
- None

Non-blocking missing items:
- Linear team not confirmed yet; required before Phase 3 write.
- No .env.example found; runtime checks may need user help later.

Linear Issue Description Language:
- English + Chinese

Recommended next step:
- Start Phase 1 Audit.
```

## 3. Phase 1 Audit

Codex 只读项目，生成：

```text
project-os/audit/PROJECT_BASELINE_DRAFT.md
project-os/audit/PRODUCT_MAP.md
project-os/audit/FEATURE_INVENTORY.md
project-os/audit/GAPS_AND_DUPLICATES.md
project-os/audit/RISKS_AND_DECISIONS.md
project-os/audit/LINEAR_IMPORT_PLAN.md
```

Feature inventory 示例：

| Feature ID | Title | Module | Target Version | Status |
|---|---|---|---|---|
| LESSON-001 | Course list supports search | lesson | v0.1.0 | Ready |
| LESSON-002 | Progress can be marked complete | progress | v0.1.0 | Ready |
| EXPORT-001 | Export progress CSV | export | v0.2.0 | Backlog |
| DEC-001 | Choose export format | export | v0.2.0 | Needs Decision |

## 4. Baseline Confirmation

Codex 停下来等待人工确认。

用户检查 audit 文件后输入：

```text
Baseline 已人工确认。
Linear team 使用 DvdTeacher。
状态映射确认。
标签使用 namespaced OS labels。
批准写入 Linear。
```

没有这类明确授权时，Codex 不得首次批量写入 Linear。

## 5. Phase 3 Linear Import

Codex 先做 Linear preflight：

- 读取 team/project/issue/label/status。
- 检查疑似重复。
- 展示最终写入清单。
- 确认每个 Issue 有 Action Steps 和 Expected Result。

Feature Issue 示例：

```text
Feature ID: LESSON-001
Module: lesson
Target Version: v0.1.0
Type: feature
Source: Phase 1 audit
Linear Description Language: English + Chinese

Problem / 问题:
Users cannot quickly find a course in a long list.
用户在课程很多时无法快速找到课程。

Action Steps / 执行动作:
1. Add search input to the course list.
   在课程列表增加搜索输入。
2. Filter courses by title.
   按课程标题过滤。
3. Add tests for empty query and matching query.
   增加空查询和命中查询测试。

Expected Result / 期待结果:
Typing a keyword narrows the list without losing course progress state.
输入关键词后列表被过滤，且课程进度状态不丢失。

Acceptance Criteria / 验收标准:
- Empty search shows all courses.
- Matching search shows matching courses only.
- Search state survives refresh if product policy requires it, otherwise DEC needed.
```

## 6. One Issue Lifecycle

v0.3 的基础交接规则：

```text
Assigned = human queue
Unassigned = Codex queue
Status = lifecycle
Labels = classification only, optional for advanced workflows
```

中文规则：

```text
有 assignee = 人类队列
无 assignee = Codex 队列
Status = 生命周期
Labels = 只做分类，高级流程可选
```

用户启动开发：

```text
请读取 project-os/AGENTS.md、project-os/WORKFLOW.md、project-os/QUALITY_GATE.md。

我要处理 Feature ID: LESSON-001，目标版本: v0.1.0。

请先从 Linear/GitHub/本地代码确认上下文，然后给出开发计划。
如果 Feature ID 或目标版本缺失，请不要开始正式开发。
```

Codex 应做：

1. 读取 Linear Issue、相关代码和测试。
2. 确认 Ready for Development。
3. 如果 issue 是 `Todo + unassigned`，把状态改为 `In Progress`，保持 unassigned。
4. 修改代码。
5. 运行测试。
6. 汇报 changed files、tests、risks、needs human check。
7. 把 Linear 状态推进到 `In Review`，assign 给 Owner/reviewer，但不声称 UAT 通过。

人工 review 后，如果需要修改：

```text
我已经在 DVD-123 留了 review feedback。
请读取 DVD-123 的最新评论。
如果它是 Todo + unassigned，请按 feedback 修改 LESSON-001。
目标版本仍是 v0.1.0。
```

人类在 Linear 里的操作：

| 场景 | 人类操作 |
|---|---|
| 验收通过 | 改为 `Done` |
| 验收失败，需要 Codex 改 | 留评论，清空 assignee，改为 `Todo` |
| 需要自己补信息 | assign 给自己，保持 `Todo` |
| 是下一版本需求 | 不移动旧 issue；创建或让 Codex 创建下一版本 issue |

## 7. UAT

版本进入 UAT 前，用户使用 `project-os/UAT_TEMPLATE.md`。

UAT 场景示例：

| Scenario ID | Feature ID | Scenario | Expected Result |
|---|---|---|---|
| UAT-001 | LESSON-001 | Search for an existing course title | Only matching courses are shown |
| UAT-002 | LESSON-002 | Mark one course complete | Progress shows complete after refresh |

最终用户必须给出人工结论：

```text
UAT 通过，允许发布 v0.1.0。
```

Codex 不能替用户写这个结论。

## 8. Next Version Carry-over

如果在 v0.1 UAT 后，用户在 `LESSON-001` 留言：

```text
下一版希望搜索支持拼音首字母。
```

正确做法：

- 不移动 `LESSON-001` 到 v0.2。
- 在 `LESSON-001` 留 carry-over comment。
- 创建 `LESSON-010`，Target Version `v0.2.0`。
- `LESSON-010` 写明 source issue、validation scenario、expected result。

承接 Issue 示例：

```text
Feature ID: LESSON-010
Module: lesson
Target Version: v0.2.0
Type: feature
Source: Carry-over from LESSON-001

Problem / 问题:
Users want course search to support pinyin initials.
用户希望课程搜索支持拼音首字母。

Expected Result / 期待结果:
Searching `sx` can find `数学入门` if pinyin-initial search is approved.
如果拼音首字母搜索被确认，搜索 `sx` 能找到 `数学入门`。
```

## 9. Daily Prompts

检查 Linear 但不直接开工：

```text
请检查 Linear，然后按 AI Project OS 规则给我一个双语 run summary。
先不要写代码。
```

开始下一个安全事项：

```text
请检查 Linear，然后处理下一个 Codex-ready issue。
Codex-ready 的基础定义是：Todo + unassigned + Feature ID + 目标版本 + 验收标准 + 无阻塞 Decision。
开始前先汇报 scan scope、Codex Queue、Human Queue、Review Queue 和将处理的 issue。
```

版本收尾：

```text
请准备 v0.2.0 closeout。
扫描旧版本 open issues 和近期评论。
对已完成但有下版本反馈的 issue 创建 carry-over revalidation issue。
不要直接移动旧 issue。
```
