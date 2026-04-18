# 实现交接块 — F003 code-review r1 回流修订

- 关联任务: F003（T1-T9 全量批次的代码质量回流修订）
- 回流来源: `docs/reviews/code-review-F003-garage-memory-auto-extraction.md`（code review r1，结论 = 需修改）
- Workspace Isolation / Worktree Path / Worktree Branch: `in-place` / `N/A` / `cursor/f003-quality-chain-3d5f`
- 测试设计确认证据: auto-mode 下沿用 `docs/approvals/F003-tasks-approval.md`；本轮回流仅修补 LLM-FIXABLE finding，不引入新行为契约（仅显式化 FR-302b/FR-304/§11.6 的硬约束面），无需新 test-design-approval。

## 触碰工件

源码：

- `src/garage_os/memory/extraction_orchestrator.py`：候选必带 `source_evidence_anchors`；`experience_summary` 候选补齐 publisher 必须字段；`_generate_candidates` 异常时归一化为 `extraction_failed` batch 持久化（FR-307 文件级证据）。
- `src/garage_os/memory/publisher.py`：`publish_candidate` 新增 `conflict_strategy` 参数，命中相似条目必须显式传 `coexist|supersede|abandon`；`_to_experience_record` / `_to_knowledge_entry` 用 `.get()` + 默认值取代裸下标，避免 `KeyError`。
- `src/garage_os/cli.py`：`garage memory review` `--action` 加入 `abandon`；新增 `--strategy` 参数；`accept`/`edit_accept` 命中相似条目时强制要求 `--strategy`；`abandon` 走 publisher.abandon 早返回并把候选状态置为 `abandoned`。
- `src/garage_os/runtime/session_manager.py`：删除 `update_session` 中重复且不可达的第二个 `context_metadata` 分支（finding 4）。

测试：

- `tests/memory/test_extraction_orchestrator.py`：+ `test_extract_attaches_source_evidence_anchors`（finding 2） + `test_extract_emits_complete_experience_summary_candidate`（finding 1） + `test_extraction_failure_writes_error_batch`（finding 6）
- `tests/memory/test_publisher.py`：+ `test_publish_orchestrator_output_end_to_end`（finding 1/2 contract test：用 orchestrator 真实输出喂 publisher） + `test_publish_requires_explicit_strategy_when_conflict_detected`（finding 3） + `test_publish_coexist_does_not_record_supersede_relation`（finding 3） + 调整 `test_publish_supersede_records_relation_to_existing_entries` 显式传 `conflict_strategy="supersede"`
- `tests/test_cli.py`：+ `TestMemoryReviewCommand::test_memory_review_accept_requires_strategy_when_conflict_exists`（finding 3） + `TestMemoryReviewCommand::test_memory_review_abandon_skips_publication`（finding 3 + abandon 入面）

## RED 证据

命令：`pytest tests/memory/test_extraction_orchestrator.py tests/memory/test_publisher.py tests/test_cli.py::TestMemoryReviewCommand -v`

首次失败摘要（节选）：

- `test_extract_attaches_source_evidence_anchors` → `AssertionError: candidate ... is missing source_evidence_anchors`
- `test_extract_emits_complete_experience_summary_candidate` → `AssertionError: experience_summary candidate missing field 'task_type'`
- `test_extraction_failure_writes_error_batch` → `RuntimeError: synthetic extraction failure`（异常未被 orchestrator 吸收）
- `test_publish_orchestrator_output_end_to_end` → `KeyError: 'task_type'`
- `test_publish_requires_explicit_strategy_when_conflict_detected` → `Failed: DID NOT RAISE <class 'ValueError'>`
- `test_publish_supersede_records_relation_to_existing_entries`、`test_publish_coexist_does_not_record_supersede_relation` → `TypeError: KnowledgePublisher.publish_candidate() got an unexpected keyword argument 'conflict_strategy'`
- `test_memory_review_accept_requires_strategy_when_conflict_exists` → `assert 0 == 1`（旧实现静默 supersede）
- `test_memory_review_abandon_skips_publication` → `SystemExit: 2`（CLI 不接受 `--action abandon`）

为什么预期失败：reviewer r1 标注的 3 项 important + 2 项 minor 缺陷直接对应"orchestrator 输出与 publisher 契约漂移"、"FR-304 静默 supersede"、"FR-307 错误未持久化"等行为缺口，必然先红。

## GREEN 证据

命令：`pytest tests/memory/test_extraction_orchestrator.py tests/memory/test_publisher.py tests/test_cli.py::TestMemoryReviewCommand -v`

通过摘要：`23 passed in 0.35s`

关键结果：

- orchestrator 自动产出的候选必带 `source_evidence_anchors`（artifact / session_metadata 两类锚点），decision/pattern/solution/experience_summary 四类候选 contract test 通过 publisher 全链路落库，`source_evidence_anchor` 与 `confirmation_ref` 不再为 None。
- `experience_summary` 候选自动携带 `task_type` / `domain` / `problem_domain` / `outcome` / `duration_seconds` 等 publisher 必须字段。
- `_generate_candidates` 抛出异常时 orchestrator 写入 `evaluation_summary=extraction_failed` 的 batch（含 `metadata.error`），FR-307 错误摘要在文件层有证据。
- publisher accept/edit_accept 命中相似条目时若未传 `conflict_strategy` 抛 `ValueError`；coexist/supersede/abandon 行为分别对应"不写关系/写关系/不发布"。
- CLI `garage memory review --action abandon` 直接将候选置 `abandoned` 且不写正式 knowledge；`accept` 命中冲突时打印强制 `--strategy` 提示并以 exit 1 中止，避免静默 supersede。

回归证据：`pytest tests/ -q` → `384 passed in 24.62s`（基线 376，本轮 +8 fresh-evidence 测试，零回归）。

## 与任务计划测试种子的差异

- T2/T6（orchestrator + publisher）：在原种子之上新增 contract 级测试（用 orchestrator 真实输出喂 publisher），覆盖 FR-302a/FR-302b/§11.6 的"四类候选闭环 + 锚点不丢失"硬约束。
- T6 + T7（CLI）：新增 `abandon` 入面测试与 `accept` 冲突强制 `--strategy` 测试，对齐 FR-304 与设计 §9.4。
- T3（FR-307）：新增 orchestrator 异常 → `extraction_failed` batch 测试，对齐 FR-307 第 2/3 条 acceptance 在文件层的可回读约束。
- 其余原 T1-T9 测试种子保持不变。

## 剩余风险 / 未覆盖项

- **finding 5（minor）未处理**：publisher 仍以 `candidate_id` 作为 `KnowledgeEntry.id`。修复需要 `KnowledgeStore` 引入显式 ID 体系（带版本后缀或独立 ID），属于设计层而非 1-2 轮可消化的实现层修补。建议作为后续 hotfix 或在 T9 之后单独立 task 推进；本轮已在 review 记录中标注，r2 时若仍判为可接受可升级为 USER-INPUT。
- CLI `abandon` 与 `accept --strategy=abandon` 在语义上重叠（前者无视冲突探测、后者仅在冲突时生效）。当前都把候选置 `abandoned` 且不发布；后续若设计层要进一步区分"用户主动放弃整条候选" vs "因相似条目放弃发布"，再独立任务推进。
- orchestrator 失败分支目前用 `extraction_failed` batch 表达；session 侧仍只走 `logger.warning`。设计 §14.2 第 2/3 条已在文件层有证据，未额外往 `sessions/archived/<id>/memory-extraction-error.json` 双写，避免重复落盘。

## Pending Reviews And Gates

- `hf-test-review`（增量轮，验证本轮 +8 fresh evidence 与契约测试）
- `hf-code-review` r2
- `hf-traceability-review`
- `hf-regression-gate`
- `hf-completion-gate`

## Next Action Or Recommended Skill

- `hf-test-review`（增量轮）：先复审本轮新增测试质量与 fail-first 证据；通过后回 `hf-code-review` r2 复审实现修订。
