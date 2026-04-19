# Test Review — F006 Garage Recall & Knowledge Graph

- 评审对象:
  - `tests/test_cli.py` 中位于注释 `F006 — Recall & Knowledge Graph` 之下的 5 个 test class
    （`TestResolveKnowledgeEntryUnique` / `TestRecommendExperienceHelper` /
    `TestRecommend` / `TestKnowledgeLink` / `TestKnowledgeGraph` /
    `TestRecallAndGraphCrossCutting`，共 ~32 个 testcase）
  - `tests/test_documentation.py::test_user_guide_documents_recall_and_knowledge_graph`
    与 `::test_readmes_list_f006_cli_subcommands`
- 实现交接块: `src/garage_os/cli.py`（F006 helper / handler 段，行 ~1007-1282）
  + `src/garage_os/memory/recommendation_service.py`（新增 `build_from_query`，行 44-84）
- 上游规格: `docs/features/F006-garage-recall-and-knowledge-graph.md`（已批准）
- 上游设计: `docs/designs/2026-04-19-garage-recall-and-knowledge-graph-design.md`（已批准 r1）
- 上游 tasks: `docs/tasks/2026-04-19-garage-recall-and-knowledge-graph-tasks.md`（已批准）
- 上游 tasks-review: `docs/reviews/tasks-review-F006-recall-and-knowledge-graph.md`（通过 + 5 minor LLM-FIXABLE 留 hf-test-driven-dev 吸收）
- Workflow: profile=`standard`, mode=`auto`, branch=`cursor/f006-recommend-and-link-177b`
- Reviewer: `hf-test-review` subagent
- Date: 2026-04-19

---

## Precheck

| 项 | 结果 |
|----|------|
| 实现交接块稳定可定位 | ✅ helper/handler/常量集中在 `cli.py` 顶部常量段 + 行 ~1007-1282；`build_from_query` 集中在 `recommendation_service.py` 单方法 |
| 测试资产可定位 | ✅ `tests/test_cli.py` 行 2117-2865（F006 段） + `tests/test_documentation.py` 行 113-140 两条新增 |
| route/stage/profile 与上游 evidence 一致 | ✅ tasks-review 通过 + auto-mode approval 已落 `docs/approvals/F006-tasks-approval.md`，task-progress 显示 implementation 完成 |
| baseline 数字 | ✅ F005 baseline 451 → F006 新增 42 → 493 total，`pytest tests/ -q` 实测 `493 passed in 25.73s` |
| 新鲜 GREEN 证据 | ✅ 当次会话 `python -m pytest tests/test_cli.py tests/test_documentation.py -q` `112 passed in 1.37s`；`python -m pytest tests/ -q` `493 passed` |

Precheck 通过，进入正式审查。

---

## 多维评分（每维 0-10）

| ID | 维度 | 分 | 关键依据 |
|---|---|---|---|
| TT1 | fail-first 有效性 | 8 | 测试断言精度高（`version == 2/3`、`related_decisions == ['B']`、`source_artifact == CLI_SOURCE_KNOWLEDGE_LINK`、`out.count("[DECISION]") == 2` 等），断言形状 + 字段值，born-green 概率低；fail-first ledger 未在测试文件内显式留痕，但实现交接块 + 行号映射可冷读 |
| TT2 | 行为 / 验收映射 | 9 | 设计 §13.2 用例 1-26 覆盖（明细见下表）；FR-601~608 / NFR-601/603/604/605 / CON-602/603/604 / ADR-601/602/603 全部至少 1 条 testcase 命中；helper 单测把 FR-602 6 条规则逐条断言 |
| TT3 | 风险覆盖 | 7 | error/边界覆盖丰富（mutex `--from missing` / ambiguous / 重复 link / 零结果 2 路 / `--to` 接受外部 ID / 孤立节点 / 多 type 命中）；2 处 minor 缺口：(a) `Source: <session>` 行未单列断言（OQ-607）；(b) `skill_name_only` fallback 路径（design §10.1 mermaid Note）未单列 happy 用例 |
| TT4 | 测试设计质量 | 9 | 全部使用 `tmp_path` per-test 隔离，符合 AGENTS.md 项目约定；零 mock，全部走真实 `KnowledgeStore` / `ExperienceIndex` / `FileStorage` / `argparse`；`TestRecommendExperienceHelper` 单测纯函数，与 FS 解耦；命名清晰（`test_<behavior>_<expectation>`） |
| TT5 | 新鲜证据完整性 | 9 | 当次会话 fresh GREEN 已核实；测试覆盖与代码 1:1 cross-reference 可冷读 |
| TT6 | 下游就绪度 | 9 | 测试质量足以支撑 hf-code-review 判断；2 处 minor 缺口属增量补强，不污染 code-review 主流程；F005 既有 451 测试零回归保持 |

无任何关键维度 < 6。综合通过线已满足。

---

## 设计 §13.2 用例 1-26 覆盖矩阵

| # | 用例 | 测试函数 | 状态 |
|---|------|---------|------|
| 1 | recommend happy knowledge-only | `TestRecommend::test_recommend_knowledge_only_happy` | ✅ |
| 2 | recommend happy experience-only | `TestRecommend::test_recommend_experience_only` | ✅ |
| 3 | recommend mixed knowledge + experience | `TestRecommend::test_recommend_mixed_sorted_by_score` | ✅（断言两个 label 共存） |
| 4 | `--tag`/`--domain`/`--top` 全生效 | `test_recommend_top_limits_results` + `test_recommend_tag_and_domain_passed_through` | ✅ |
| 5 | 零结果（empty `.garage/`） | `test_recommend_zero_results_on_empty_garage` | ✅ |
| 6 | N entry 但 query 不命中 | `test_recommend_zero_results_with_entries_but_no_match` | ✅（用 3 entry 替代 5+5；语义等价） |
| 7 | 无 `.garage/` | `test_recommend_no_garage_dir` | ✅ |
| 8 | link happy（version=2 / source_artifact） | `TestKnowledgeLink::test_link_happy_appends_and_bumps_version` | ✅ |
| 9 | link 重复（去重 + already 文案） | `test_link_repeated_is_idempotent_in_field`（断言 `version == 3`） | ✅ |
| 10 | link `--kind related-task` | `test_link_related_task_writes_separate_field` | ✅ |
| 11 | link `--from missing` | `test_link_from_not_found` | ✅ |
| 12 | link `--to` 外部 ID | `test_link_to_unvalidated_external_id` | ✅ |
| 13 | link 多 type 命中 | `test_link_ambiguous_from_id`（断言 stderr 含 `decision` + `pattern`） | ✅ |
| 14 | link 不污染 publisher 元数据 | `test_link_does_not_pollute_publisher_metadata`（断言 `published_from_candidate == "cand-x"` 保持） | ✅ |
| 15 | graph 节点 + 出 + 入边 | `TestKnowledgeGraph::test_graph_node_with_outgoing_and_incoming` | ✅ |
| 16 | graph 孤立节点 | `test_graph_isolated_node_shows_none`（`out.count(GRAPH_EDGE_NONE) == 2`） | ✅ |
| 17 | graph `--id missing` | `test_graph_not_found` | ✅ |
| 18 | graph `--id` 多 type 命中 | `test_graph_ambiguous_id` | ✅ |
| 19 | recommend `--help` 全参数 | `test_recommend_help_lists_all_args` | ✅ |
| 20 | link `--help` 全参数 | `test_link_help_lists_all_args` | ✅ |
| 21 | graph `--help` 全参数 | `test_graph_help_lists_all_args` | ✅ |
| 22 | `garage --help` 含 `recommend` | `test_top_level_help_lists_recommend` | ✅ |
| 23 | `garage knowledge --help` 含 8 个 sub | `test_knowledge_help_lists_all_8_subcommands` | ✅（量化 8 个 token） |
| 24 | recommend smoke < 1.5s | `test_recommend_smoke_under_one_and_a_half_seconds` | ✅ |
| 25 | CLI source markers `cli:` | `test_link_source_marker_uses_cli_namespace` + 既有 `test_cli_source_markers_use_cli_namespace` | ✅ |
| 26 | F005 add/edit 行为不变 | NFR-601 全 suite 回归（493 passed = 451 + 42） | ✅ |

---

## 上游 tasks-review 5 minor LLM-FIXABLE 吸收回访

| 上游编号 | 描述 | 当前状态 | 证据 |
|---------|------|---------|------|
| F-1 | recommend 输出 `Source:` 行 acceptance | 部分开放（生产代码已实现 `_print_recommendation_block` 行 1132-1134；测试无显式断言） | `cli.py` 行 1132-1134 有 `if source_session: print(f"  Source: {source_session}")`；`tests/test_cli.py` 全文 `Source:` 0 命中 |
| F-2 | 重复 link 路径 source_artifact 仍覆写 | ✅ 已吸收 | `test_link_repeated_is_idempotent_in_field`（行 2568）`assert entry.source_artifact == CLI_SOURCE_KNOWLEDGE_LINK` |
| F-3 | `_recommend_experience` 返回项 `source_session` 字段 | ✅ 已吸收 | `test_returned_shape_matches_recommendation_service`（行 2299-2310）`assert item["source_session"] == "sess-1"` |
| F-4 | `skill_name_only` fallback 统一打印 | 开放 | `recommendation_service.py:159-176` 的 fallback 路径返回 `match_reasons=["skill_name_only"]` + `score=0.1`；F006 测试无任何用例触发 / 断言 CLI 把这条路径正确打印为 `Match: skill_name_only` 块 |
| F-5 | NFR-602 git diff 锚点 | 不在测试范围 | 该 finding 是 verify 步骤的命令选择，非测试层；F006 cycle 完成后由人工 / Cursor cloud 自动核 `pyproject.toml` 无新增 |

---

## 发现项

- [minor][LLM-FIXABLE][TT3 / TA2] **F006-TR-1 — `Source: <session>` 行无显式断言**
  - 规格 OQ-607 + 设计 §10.1 显式声明 `Source: <session>` 行（仅当非空时）。生产代码 `_print_recommendation_block` 行 1132-1134 已实现，但 F006 测试段全文 `grep "Source:"` 0 命中。
  - 风险：未来若 handler 重构把 `Source:` 行误删，回归测试不会捕获；OQ-607 spec 承诺会静默丢失。
  - 建议补 1 条测试用例：构造 `experience add --session sess-x --id exp-1 ...` 然后 `recommend "..."` 后 `assert "Source: sess-x" in out`，并补 1 条断言 session_id 为空时该行不出现。

- [minor][LLM-FIXABLE][TT3 / TA2] **F006-TR-2 — `skill_name_only` fallback 路径无端到端断言**
  - 设计 §10.1 mermaid Note 明确 `RecommendationService.recommend()` 可能返回 `match_reasons=["skill_name_only"]` + `score=0.1` 的 fallback；CLI 应 "uniformly" 把这条 case 打印为同一 `[TYPE] title / ID / Score: 0.10 / Match: skill_name_only` 块。
  - 风险：当用户 query 完全没有命中 tags / domain / problem_domain 而 `skill_name == tokens[0]` 仅在 entry topic 文本中部分命中时，是否得到统一打印 + score=0.10 没有回归保护。
  - 建议补 1 条测试用例：构造 `(decision, foo)` `topic="some foo here"` `tags=[]` 然后 `recommend "foo"`，断言 stdout 含 `Score: 0.10` 与 `Match: skill_name_only`（注意 `RecommendationService` 当前实现对此 case 返回的实际 score 路径需要 cli-side 实测验证）。

- [minor][LLM-FIXABLE][TT2 / TA4] **F006-TR-3 — CON-605 不修改 `RecommendationService.recommend` 缺 spot-check**
  - tasks-review §4 trace 表明确把 CON-605 列在 T2 责任内；T2 acceptance 第 11 条要求 "`RecommendationService.recommend()` 源码字节级未变更（grep `recommend(` 签名 / score 权重未变）"。F006 测试段无任何对 `recommend()` 公开签名 / 行为不变的 spot-check。
  - 缓解：493 passed 已含 F003 / F004 既有 `RecommendationService` 单测全绿（NFR-601 间接保证），实际 fail surface 极小，标 minor。
  - 建议在 hf-test-driven-dev 后续轮次顺手补 1 条 "调用 `recommend(skill_shaped_context)` 行为与 F003 baseline 一致" 的回归断言（可直接 import 既有 fixtures）。

---

## 缺失或薄弱项

- 上述 3 条 finding 全部 minor LLM-FIXABLE，可在 hf-code-review 之前的轻量 follow-up 或 hf-test-driven-dev 一并吸收，不阻塞当前通过。
- 测试段未显式记录 RED → GREEN ledger，但实现交接块 + 当次 fresh GREEN 证据足以让 reviewer 冷读判断；standard profile 不强制 fail-first ledger 落盘。

---

## 结论

**通过**

理由：

1. 6 个评审维度均 ≥ 7/10，全部高于通过阈值 6。
2. 设计 §13.2 用例 1-26 全部至少 1 条 testcase 覆盖；FR-601~608 / NFR-601/603/604/605 / CON-602/603/604 / ADR-601/602/603 trace 全清。
3. 上游 tasks-review 5 条 minor LLM-FIXABLE 中 F-2 / F-3 已被本批测试直接吸收；F-1 / F-4 / CON-605 spot-check 可在 hf-code-review 前后续轻量补，不影响代码评审主线。
4. v1.1 不变量 `version+=1` 在 link 路径（含 re-link）双重断言（`version == 2` / `version == 3`）。
5. 来源标记 `cli:knowledge-link` 在 happy / 重复 link / publisher pollution 三个路径都断言。
6. CRUD-like loop（link → graph）在 `test_graph_node_with_outgoing_and_incoming` 与 `test_graph_mixed_edge_kinds` 中端到端走通。
7. NFR-603 smoke 通过实测 < 1.5s 阈值。
8. 全 suite 当前会话回归实测 `493 passed`（= F005 baseline 451 + F006 新增 42），零回归。
9. 测试设计零 mock + 全 `tmp_path` 隔离，符合 AGENTS.md 项目约定。

---

## 下一步

- `hf-code-review`

---

## 记录位置

- 本评审记录: `docs/reviews/test-review-F006-recall-and-knowledge-graph.md`
