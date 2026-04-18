# Test Review (r2) — F003 Garage Memory 自动知识提取与经验推荐

- 评审范围: F003 全量实现批次 + r1 回流修订（关闭分支、supersede/abandon、truncation、FR-302b 校验）的测试质量
- Review skill: `hf-test-review`
- Review 轮次: r2（r1 = 需修改）
- 评审者: cursor cloud agent (auto mode)
- 日期: 2026-04-18
- Worktree branch: `cursor/f003-quality-chain-3d5f`
- Workspace isolation: `in-place`
- 关联工件:
  - 上一轮 review: `docs/reviews/test-review-F003-garage-memory-auto-extraction.md`
  - r1 回流交接块: `docs/verification/F003-test-review-r1-handoff.md`
  - T1 实现交接块: `docs/verification/F003-T1-implementation-handoff.md`
  - 任务计划: `docs/tasks/2026-04-18-garage-memory-auto-extraction-tasks.md`
  - 设计: `docs/designs/2026-04-18-garage-memory-auto-extraction-design.md`
  - 规格: `docs/features/F003-garage-memory-auto-extraction.md`
  - 上游 approvals: `docs/approvals/F003-spec-approval.md` / `F003-design-approval.md` / `F003-tasks-approval.md` / `F003-T1-test-design-approval.md`
- 评审测试资产:
  - `tests/memory/test_candidate_store.py`
  - `tests/memory/test_extraction_orchestrator.py`
  - `tests/memory/test_publisher.py`
  - `tests/memory/test_recommendation_service.py`
  - `tests/runtime/test_session_manager.py`
  - `tests/runtime/test_skill_executor.py`
  - `tests/integration/test_e2e_workflow.py`
  - `tests/test_cli.py`
  - `tests/knowledge/test_knowledge_store.py`
  - `tests/knowledge/test_experience_index.py`
  - `tests/knowledge/test_integration.py`
- 评审实现资产:
  - `src/garage_os/memory/candidate_store.py`
  - `src/garage_os/memory/extraction_orchestrator.py`
  - `src/garage_os/memory/publisher.py`
- 当次 GREEN 证据: `pytest tests/ -q` → `376 passed in 24.62s`（与父会话承诺基线一致；r1 基线 369 → r2 基线 376，+7 新测试，全套零回归）

## 结论

通过

r1 列出的 1 项 critical + 4 项 important findings 在 r2 这轮全部以"新 fail-first 测试 + 最小生产代码闭环"的方式回写到位，且回流交接块 `docs/verification/F003-test-review-r1-handoff.md` 提供了可冷读的 RED 首次失败摘要、GREEN 通过摘要、与 task-plan seed 的差异说明。3 项关键维度（TT1/TT3/TT5）均已抬到 ≥7/10，6 维度全部 ≥7/10，`pytest tests/ -q` 全套 376 passed，可放行进入 `hf-code-review`。r1 中标注的 2 项 minor（关键测试 docstring 缺 trace anchor、`test_execute_skill_uses_recommendation_service_when_available` 嵌套 Mock）在本轮按 r1 reviewer 的明确说明未阻塞 r2，沿用为后续 hotfix/小幅改善候选。

## 多维评分（0-10，括号内为 r1 → r2 变化）

| 维度 | r2 评分 | 说明 |
|------|---------|------|
| `TT1` fail-first 有效性 | 7 (5 → 7) | 4 项 r1 important 缺口的回流测试在交接块中均给出当次会话内可冷读的首次失败摘要（`AssertionError: assert 'existing-001' in []` / `assert 'candidate-002' is None` / `assert 0 >= 1` / `Failed: DID NOT RAISE`），GREEN 摘要为 `19 passed in 0.24s`。off-switch 两条新测试虽是"补漏型"测试（生产代码事先已有 short-circuit 分支），但交接块明确说明该分支此前零测试覆盖、本轮直接以 fresh GREEN 锁定 acceptance，符合 TT1 对当次会话证据的最低要求 |
| `TT2` 行为/验收映射 | 7 (7 → 7) | 新测试均能回指到 T1 FR-302b、T2 truncation/FR-303a、T4 关闭分支、T6 supersede/abandon 验收口径；测试 docstring 已显式标注"T4 acceptance" / "T6 acceptance" / "FR-302b" / "FR-303a"，比 r1 阶段更可追溯。其余存量测试 docstring 缺 trace anchor 仍是 r1 minor，未影响 verdict |
| `TT3` 风险覆盖 | 8 (5 → 8) | r1 列出的 4 个 important 风险覆盖缺口（关闭分支、supersede 关系回写、abandon 双类型早返回、truncation/`truncated_count`、FR-302b 必填校验）全部以 negative + happy 双向覆盖闭合 |
| `TT4` 测试设计质量 | 8 (8 → 8) | 新测试沿用真 `FileStorage` + `tmp_path`，复用既有 fixtures，断言落在行为结果（持久化的 `front_matter["supersedes"]`、`KnowledgeEntry.related_decisions`、`batch.truncated_count`、`store_candidate` ValueError）而非 mock 调用细节；唯一新增 mock（`MockRecommendationService.assert_not_called()`）用于断言"关闭分支下不应实例化"，属于 mock 在真实边界上的合理使用 |
| `TT5` 新鲜证据完整性 | 7 (5 → 7) | r1 回流交接块对 4 个 LLM-FIXABLE finding 提供了首次失败摘要、首次通过摘要、与 task-plan seed 的差异、剩余风险/未覆盖项；零测试覆盖的 off-switch 分支以"加测即转绿"形式锁定 acceptance，符合 TT5 对"当次可核实证据"的目标态。注：T5/T7/T8/T9 的存量 happy-path 测试本轮未再独立回 RED，但其结果在本轮 `pytest tests/` 全套 376 passed 中可重现，且 r1 reviewer 已在原文中将"为 T2-T9 补 fresh RED/GREEN 证据"的整改路径明确为"在 implementation-handoff 中给出可冷读的会话内证据"，r2 的合并交接块以 LLM-FIXABLE 焦点交付即视为达成 |
| `TT6` 下游就绪度 | 8 (7 → 8) | 关闭分支、supersede/abandon、truncation、FR-302b 四个 code-review 最容易追问的 acceptance 锚点都已就位；E2E 闭环 + 全套 376 passed 已足以让 `hf-code-review` 做可信判断 |

> 关键维度 TT1/TT3/TT5 均已 ≥6/10，按 `references/review-checklist.md` 评分辅助规则可返回 `通过`。

## r1 → r2 finding 闭合矩阵

| r1 finding | severity / rule_id | r2 验证结论 | 关键证据 |
|------------|--------------------|-------------|----------|
| T2-T9 缺 fresh RED/GREEN evidence | critical / TT5 | **关闭（合并交接块策略）** | `docs/verification/F003-test-review-r1-handoff.md` 给出 4 项回流测试的首次失败摘要 + `19 passed` 通过摘要 + 与 task-plan 第 5/8 节 seed 的差异；off-switch 两条测试以"加测即锁定 acceptance"取代回 RED；`pytest tests/ -q` → `376 passed`。残留：T5/T7/T8/T9 的存量 happy-path 测试本轮未再独立回 RED，但 r1 reviewer 已认可 implementation-handoff 形式的可冷读证据等价于 fresh evidence；不构成阻塞 |
| T4 配置开关关闭分支零覆盖 | important / TT3 | **关闭** | 新增 `tests/runtime/test_session_manager.py::test_archive_session_skips_memory_when_extraction_disabled`（写入 `extraction_enabled=False` 的 `.garage/config/platform.json`，断言 archive 后 `memory/candidates/batches/` 为空）；新增 `tests/test_cli.py::TestRunCommand::test_run_skips_recommendation_when_disabled`（断言 `Recommendations:` 不出现且 `MockRecommendationService.assert_not_called()`）|
| T6 冲突仅测 strategy 判定，缺 supersede 关系回写与 abandon 发布跳过 | important / TT3 | **关闭** | 新增 `test_publish_supersede_records_relation_to_existing_entries`（断言 `published.related_decisions` 含旧条目 ID）；新增 `test_publish_abandon_skips_publication`（断言 `knowledge_store.list_entries() == []`）；新增 `test_publish_abandon_skips_experience_summary`（断言 `experience_index.list_records() == []`）。`src/garage_os/memory/publisher.py` accept 路径写入 `entry.related_decisions` + `front_matter["supersedes"]`；`abandon` 在方法入口早返回，覆盖所有候选类型 |
| orchestrator 候选 truncation 与 `truncated_count` 字段无任何断言 | important / TT3 | **关闭** | 新增 `test_extract_truncates_to_max_pending_and_records_truncated_count`（构造 8 个 artifacts → 8+ signals，断言 `len(candidate_ids) == 5` 且 `summary["truncated_count"] >= 1`，并校验磁盘 `stored_batch["truncated_count"]` 一致）；`_generate_candidates` 现返回 `(candidates, truncated_count)`，`_build_summary` 接受并持久化 `truncated_count` |
| FR-302b 候选必填元信息缺 negative 校验测试 | important / TT3 | **关闭** | 新增 `test_reject_candidate_missing_required_metadata`（缺 `session_id` 或空 `source_artifacts` 时 `pytest.raises(ValueError)` 命中）；`candidate_store.store_candidate` 在 `ALLOWED_CANDIDATE_TYPES` 校验后增加 `candidate_id` / `session_id` / `title` / `source_artifacts` 必填校验 |

## 维持中的 minor findings（不阻塞 r2）

- `[minor][LLM-FIXABLE][TT2][TA4]` 关键 F003 用例 docstring 仍缺显式 FR / 设计章节回指。r1 已明确"日后追溯成本会上升"但不阻塞，r2 沿用该判断。
- `[minor][LLM-FIXABLE][TT4]` `test_execute_skill_uses_recommendation_service_when_available` 嵌套属性 Mock 仍未替换为真 `SessionMetadata` / `SessionContext`。r1 已明确该项不阻塞 r2；建议在后续 hotfix 或下一次涉及该用例的修订中收掉。

## 缺失或薄弱项

- T5（recommendation_service）/ T7（skill_executor recommendation 集成）/ T8（CLI memory review 命令）/ T9（E2E）这 4 个任务的存量测试在 r2 这轮没有再次独立回 RED；其 fresh evidence 依赖于 r1 阶段的本次 `pytest` 全套通过 + E2E 闭环。这一选择与 r1 reviewer 给出的整改路径一致，未构成阻塞，但建议在 `task-progress.md` 的 milestone 总结中保留一条说明，避免后续 traceability review 误读为"完全无证据"。
- `store_candidate` 的必填校验仅覆盖 `candidate_id` / `session_id` / `title` / `source_artifacts`，未对 `match_reasons` 强制非空。r1 回流交接块已显式标注此为 FR-302b 文本未明确的边界，按"最小修复"原则保留；如后续 traceability review 要求完整覆盖 FR-302b 全字段，再独立任务推进。
- supersede 关系仅写在新条目侧（新 → 旧 ID），未在旧条目侧反向写"被 supersede"。r1 回流交接块已声明此为最薄路径下的有意收束；若设计 §11.4 在后续 review 中被解读为双向关系，再独立任务推进。

## 关于路由判断

- 实现交接块（T1 + r1 回流合并交接块）齐全，可冷读
- 任务计划已批准（`docs/approvals/F003-tasks-approval.md`）；本轮回流仅闭合 LLM-FIXABLE finding，未引入新行为契约，不需要新增 `test-design-approval` 或重走 `hf-tasks-review`
- 测试资产齐全、可执行，全套 `pytest tests/ -q` → 376 passed
- profile=full / stage=hf-test-review (r2) 与 `task-progress.md` 状态一致

不构成 stage / route / profile / 上游证据冲突，**不需要 reroute via router**。下一步直接进入 `hf-code-review`。

## 下一步

- `hf-code-review`：评审 F003 回流后的代码质量。重点关注：
  1. `KnowledgePublisher.publish_candidate` 在 supersede 路径下的 `related_decisions` 去重逻辑与 `front_matter` 双键（`related_decisions` + `supersedes`）的语义边界；
  2. `MemoryExtractionOrchestrator._generate_candidates` 返回 tuple 后的调用方完整性与 `truncated_count` 的回写一致性；
  3. `CandidateStore.store_candidate` 的必填校验顺序与错误消息可观测性；
  4. `SessionManager.archive_session` 在 `extraction_enabled=False` 时的 short-circuit 是否影响 archive 主链幂等性。

## 结构化返回（供父会话路由）

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "hf-code-review",
  "record_path": "docs/reviews/test-review-F003-garage-memory-auto-extraction-r2.md",
  "key_findings": [
    "[critical→关闭][TT5] T2-T9 fresh RED/GREEN 通过 r1 回流合并交接块满足，4 项 LLM-FIXABLE 缺口均提供首次失败/通过摘要",
    "[important→关闭][TT3] T4 关闭分支 archive_session_skips_memory_when_extraction_disabled / run_skips_recommendation_when_disabled 已覆盖",
    "[important→关闭][TT3] T6 supersede 关系回写 + abandon 跳过 decision/experience_summary 三条测试已覆盖",
    "[important→关闭][TT3] orchestrator truncation 测试 + truncated_count 持久化已覆盖",
    "[important→关闭][TT3] FR-302b 必填元信息 negative 测试已覆盖",
    "[minor 维持] 测试 docstring trace anchor / 嵌套 Mock 易脆，不阻塞 code review"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "TT2",
      "summary": "F003 关键测试 docstring 缺 FR/设计章节 trace anchor（r1 minor，r2 维持）"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "TT4",
      "summary": "test_execute_skill_uses_recommendation_service_when_available 嵌套属性 Mock 易脆（r1 minor，r2 维持）"
    }
  ]
}
```
