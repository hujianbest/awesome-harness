# F006 Finalize — Closeout Pack

## Closeout Summary

- Closeout Type: `workflow-closeout`
- Scope: F006 Garage Recall & Knowledge Graph（主动召回 + 知识图最小可用形态）— cycle 内全部任务（T1-T6 in plan, 5 任务全部 done）已完成；3 个新 CLI 子命令端到端可用；零 F003/F004/F005 回归；`KnowledgeEntry.related_decisions` / `related_tasks` 字段第一次接通到用户面
- Conclusion: **F006 cycle 正式关闭**
- Based On Completion Record: `docs/verification/F006-completion-gate.md`（结论：通过）
- Based On Regression Record: `docs/verification/F006-regression-gate.md`（结论：通过）

## Evidence Matrix

| Artifact | Record Path | Status |
|----------|-------------|--------|
| Spec | `docs/features/F006-garage-recall-and-knowledge-graph.md` | 已批准（auto-mode r2） |
| Spec approval | `docs/approvals/F006-spec-approval.md` | Applied |
| Spec review r1 | `docs/reviews/spec-review-F006-recall-and-knowledge-graph.md` | 需修改 → USER-INPUT path B 裁决 → 1:1 闭合 |
| Spec review r2 | `docs/reviews/spec-review-F006-recall-and-knowledge-graph-r2.md` | 通过 |
| Design (r1) | `docs/designs/2026-04-19-garage-recall-and-knowledge-graph-design.md` | 已批准（auto-mode r1 inline-fixed） |
| Design approval | `docs/approvals/F006-design-approval.md` | Applied |
| Design review | `docs/reviews/design-review-F006-recall-and-knowledge-graph.md` | 通过（3 minor inline-fixed） |
| Tasks plan | `docs/tasks/2026-04-19-garage-recall-and-knowledge-graph-tasks.md` | 已批准（auto-mode） |
| Tasks approval | `docs/approvals/F006-tasks-approval.md` | Applied |
| Tasks review | `docs/reviews/tasks-review-F006-recall-and-knowledge-graph.md` | 通过（5 minor; 3 absorbed downstream） |
| Test review | `docs/reviews/test-review-F006-recall-and-knowledge-graph.md` | 通过（3 minor; supplementary tests added） |
| Code review | `docs/reviews/code-review-F006-recall-and-knowledge-graph.md` | 通过（3 minor; CR-1/CR-2 inline-fixed） |
| Traceability review | `docs/reviews/traceability-review-F006-recall-and-knowledge-graph.md` | 通过（3 minor 留 finalize 顺手处理） |
| Regression gate | `docs/verification/F006-regression-gate.md` | 通过 |
| Completion gate | `docs/verification/F006-completion-gate.md` | 通过 |
| Release notes | `RELEASE_NOTES.md` `## F006 — ...` 段 | Updated |
| Finalize closeout pack | `docs/verification/F006-finalize-closeout-pack.md`（本文件） | This file |
| User guide doc section | `docs/guides/garage-os-user-guide.md` "Active recall and knowledge graph" 段 | Updated |
| README EN | `README.md` CLI command list | Updated |
| README ZH | `README.zh-CN.md` CLI command list | Updated |
| E2E walkthrough log | `/opt/cursor/artifacts/f006_cli_walkthrough.log` | Captured |

## State Sync

- Current Stage: `closed`
- Current Active Task: `null`（cycle 已关闭，无活跃任务）
- Workspace Isolation: `in-place`
- Worktree Path: `N/A`（never created worktree）
- Worktree Branch: `cursor/f006-recommend-and-link-177b`（PR branch；未来如需修订，可继续在该分支 work）
- Worktree Disposition: `branch retained on origin/cursor/f006-recommend-and-link-177b`

## Release / Docs Sync

- Release Notes Path: `RELEASE_NOTES.md`（F006 段为最新条目，置顶 F005 条目之上）
- Updated Docs:
  - `docs/guides/garage-os-user-guide.md`（新增 "Active recall and knowledge graph" 段）
  - `README.md`（CLI 命令表追加 3 个新子命令）
  - `README.zh-CN.md`（同上中文版）
  - `docs/features/F006-...md`（状态 = 已批准 auto-mode）
  - `docs/designs/2026-04-19-garage-recall-and-knowledge-graph-design.md`（状态 = 已批准 auto-mode r1）
  - `docs/tasks/2026-04-19-garage-recall-and-knowledge-graph-tasks.md`（状态 = 已批准 auto-mode）

## Handoff

- Remaining Approved Tasks: 无（T1-T5 全部 done）
- Next Action Or Recommended Skill: `null`（workflow 已关闭）
- PR / Branch Status: `cursor/f006-recommend-and-link-177b` 推送至 `origin`，对应 PR #17（draft）；将在本 finalize 后更新 PR 描述
- Limits / Open Notes:
  - **Stage 3 进入信号尚未达标**：`docs/soul/growth-strategy.md` 给出 "知识库条目 >100" 与 "识别到 5+ 可复用模式" 作为 Stage 3 进入信号。F006 把 recall 主动入口与知识图衬底都铺好了，但**实际条目增长 + 模式聚类**仍依赖用户使用频率。下一个 cycle 是否启动 Stage 3 由 `hf-workflow-router` 在新会话独立判断。
  - **`_recommend_experience` 多次累加 vs 单次累加语义微差（code review CR-3 minor）**：tech / pattern / lesson 规则可对同一 record 重复加分；task_type 规则带 break；spec FR-602 措辞已允许此读法。建议下一 cycle 在真实使用数据上观察 score 分布后决定是否对齐。
  - **`task-progress.md` 状态回写在 closeout 时统一处理（traceability TZ5 minor）**：本 cycle 在 closeout 末尾完成回写，后续 cycle 启动时由 router 重新建立。
  - **§ 5 deferred backlog**：unlink / 多跳 graph / experience link / 跨类型 link / 图导出（GraphViz/Mermaid/JSON）/ `recommend --format json` / `--include knowledge-only|experience-only` / embedding-based 相似度 / 自动建议链接 — 全部明确不在本 cycle 内消化。
  - **Pre-existing baseline**：2 个 F004 历史 mypy errors + cli.py 47 个 ruff stylistic warnings（含 1 个 unused import on `recommendation_service.py`），全部由独立 cycle 治理。F006 增量 ruff +4 全部为 UP045 stylistic（与现有 cli.py 30+ 处 `Optional[X]` 一致），未引入新行为问题。

## 触动文件清单

源代码（2 个）:
- `src/garage_os/cli.py`（+ 12 个模块常量 + 3 个 helper + 3 个 handler + 3 个 sub-parser + main 分发扩展；ADR-501 单文件风格保持）
- `src/garage_os/memory/recommendation_service.py`（+ `RecommendationContextBuilder.build_from_query()` 方法；现有 `build()` / `RecommendationService.recommend()` 一字未改 = CON-602 + CON-605）

测试（45 个新增）:
- `tests/test_cli.py`：
  - `TestResolveKnowledgeEntryUnique`(3 个) — FR-605 helper 层
  - `TestRecommendExperienceHelper`(9 个) — FR-602 helper 6 条规则各覆盖
  - `TestRecommend`(11 个) — FR-601/602/603 + build_from_query + happy/edge/zero/no-garage/Source: 行/skill_name_only fallback/CON-605 spot-check/smoke
  - `TestKnowledgeLink`(7 个) — FR-604/605/607 + happy/idempotent/related-task/not-found/external-id/ambiguous/publisher metadata 隔离
  - `TestKnowledgeGraph`(5 个) — FR-606 + 出/入边/孤立/not-found/ambiguous/mixed-edge-kinds
  - `TestRecallAndGraphCrossCutting`(7 个) — FR-608 help (5 命令) + cli: 命名空间 + smoke 重复
- `tests/test_documentation.py`：
  - `test_user_guide_documents_recall_and_knowledge_graph`（7 token grep）
  - `test_readmes_list_f006_cli_subcommands`（双 README × 3 token grep）

文档:
- `docs/features/F006-...md`（spec + r1 修订）
- `docs/designs/2026-04-19-...md`（design r1）
- `docs/tasks/2026-04-19-...md`（tasks plan）
- `docs/guides/garage-os-user-guide.md`（新增 "Active recall and knowledge graph" 段）
- `README.md` / `README.zh-CN.md`（CLI 命令表追加）
- `RELEASE_NOTES.md`（F006 cycle 段）
- 7 个 reviews（spec r1 + r2、design、tasks、test、code、traceability）
- 3 个 approvals（spec、design、tasks）
- 1 个 regression gate + 1 个 completion gate + 本 closeout pack

## Verification

```
$ pytest tests/ -q
============================= 496 passed in 25.71s =============================
```

零回归；F005 baseline 451 → F006 终态 496，新增 45 个测试。

## Workflow Closeout 决议

按 `hf-finalize` § 3A：本会话是 `auto` mode，按项目 auto 规则在写完 closeout pack 后即把 workflow 视为已关闭。Current Stage 设为 `closed`，Next Action 设为 `null`。
