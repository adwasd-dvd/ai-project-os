# LINEAR PROJECT CONSOLIDATION

## Decision

Decision ID: DEC-010
Date: 2026-08-25
Owner: dvdTeacher
Status: Done

AI Project OS uses one long-lived Linear Project. Release versions use Project Milestones, not separate Projects.

AI Project OS 只使用一个长期 Linear Project。发布版本使用 Project Milestone，不再按版本新建 Project。

## Canonical Project / 唯一主 Project

Name: AI Project OS
ID: 2a8e9515-50be-40fe-981b-8cd29690d513
URL: https://linear.app/dvdteacher/project/ai-project-os-e72aba5f39a2
Team: DvdTeacher
Status: In Progress

## Operating Rule / 工作规则

1. Every new Feature, Bug, Chore, Decision, UAT, or carry-over issue uses the canonical Project.
2. Every issue has one target-version Milestone.
3. A new release version creates a Milestone, never another AI Project OS Project.
4. Released source issues remain Done in their original Milestone.
5. Next-version feedback creates a new carry-over revalidation issue in the new Milestone and links back to the released source issue.
6. The six historical Projects receive no new issues.
7. Only an explicit Owner Decision may replace this model.

1. 所有新 Feature、Bug、Chore、Decision、UAT 或 carry-over Issue 都进入唯一主 Project。
2. 每个 Issue 指定一个目标版本 Milestone。
3. 新版本只创建 Milestone，不再创建新的 AI Project OS Project。
4. 已发布源 Issue 保持 Done，并留在原 Milestone。
5. 下版本反馈在新 Milestone 创建 carry-over revalidation Issue，并链接已发布源 Issue。
6. 六个历史 Project 不再接收新 Issue。
7. 只有 Owner 的明确 Decision 才能替换本模型。

This project-specific Decision supersedes the older per-version-Project recommendation for AI Project OS itself. Generic template behavior may remain configurable for other products.

本项目专属 Decision 覆盖 AI Project OS 自身此前“每版本一个 Project”的建议；其他产品的通用模板仍可按项目情况配置。

## Milestones / 版本 Milestone

| Milestone | Linear ID | Purpose | Historical Issues |
|---|---|---|---:|
| v0.1.0 | 900515d9-8a3a-4678-a90c-7156eb9b644b | Released history | 11 |
| v0.2.0 | 5b6c2774-a965-4a0b-9a97-279ca02fc551 | Released history | 12 |
| v0.3.0 | c74e8cd4-a6ce-4c5f-a1e8-ee58077e6e2f | Released history | 6 |
| v0.4.0 | 64890c8c-73af-4254-a498-cb595f47dddc | Released history | 8 |
| v0.5.0 | 3b522dcb-e3b9-4268-895c-84430926d3a7 | Released history | 8 |
| v0.6.0 | e590cb91-dfad-488a-92c0-54542c356afd | Released Development Train A | 8 |
| v0.8.0 | 320389b9-05e7-44d9-ad3a-4d6888624f7d | Development Train B candidate | 0; Feature Register is the temporary equivalent record |
| v1.0.0 | 5c401d12-22b1-45bd-959a-cf8c58116f45 | Future internal stable release | 0 |

## Historical Project Pointers / 历史 Project 指针

| Former Project ID | Final Name | Final Status | Issues After Merge |
|---|---|---|---:|
| 1ef51e67-aae6-4c89-bce8-21cfde105def | History - AI Project OS v0.1 | Completed | 0 |
| a6e24ed6-d562-48b7-b3c3-313699badc64 | History - AI Project OS v0.2 | Completed | 0 |
| 8d1e72c7-e0f1-4eff-bcb6-b883f4c37ce9 | History - AI Project OS v0.3 | Completed | 0 |
| 5647caf5-3ff8-424a-be52-9d36e5000028 | History - AI Project OS v0.4 | Completed | 0 |
| 6e957cef-d72f-4f10-ba81-8337c05ae8e8 | History - AI Project OS v0.5 | Completed | 0 |
| 0f99810a-c014-4b2b-9203-791c32535053 | History - AI Project OS v0.6 Train A | Completed | 0 |

Linear does not expose a Project-archive write through the connected tool. Completed historical pointers are therefore retained instead of deleted. Their descriptions point to the canonical Project.

当前连接工具没有提供 Project 归档写入，因此旧 Project 以 Completed 历史指针保留，不删除；其描述已指向唯一主 Project。

## Migration Receipt / 合并收据

Projects scanned: 7
Canonical Projects after merge: 1 active
Historical Projects emptied: 6/6
Issues moved: 53
Issue status changes: 0
Done issues after move: 53
Issues missing Milestone: 0
Project Document retained: f8583467-5009-4f8a-bb3f-f312ece4c704
Linear status update: 3e56d7ad-fe67-4e92-9fd1-12eabcd67f3a

## Intake Configuration / 扫描配置

AI Project OS scans must target the canonical Project exactly. Do not use the old version-name prefix as the normal scope.

AI Project OS 扫描必须精确指向唯一主 Project，不再把旧版本名称前缀作为日常范围。

    "projects": ["AI Project OS"]
    "project_name_prefixes": []
    "max_issues": 250

Version scope is determined by Milestone plus the Issue Target Version. Explicitly named historical issues remain eligible for carry-over review.

版本范围由 Milestone 和 Issue 的 Target Version 共同决定；被明确点名的历史 Issue 仍可进入 carry-over 检查。

## Expected Result / 期待结果

- Linear's active Project list has one AI Project OS entry.
- Version views use Milestones.
- Broad Codex requests scan the canonical Project without recreating version Projects.
- Historical traceability remains available without cluttering the active workflow.

- Linear 活跃 Project 列表只有一个 AI Project OS。
- 版本视图使用 Milestone。
- 宽泛 Codex 请求扫描唯一主 Project，不再重建版本 Project。
- 历史追踪继续保留，但不干扰当前工作。
