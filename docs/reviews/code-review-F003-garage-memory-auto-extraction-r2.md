# Code Review (r2) — F003 Garage Memory 自动知识提取与经验推荐

- 评审范围: F003 代码层 r1 → r2 回流修订（关闭 r1 标注的 3 项 important + 3 项 minor，含 anchors / 冲突策略 / abandon / FR-307 batch / dead code）
- Review skill: `hf-code-review`
- Review 轮次: r2（r1 verdict = 需修改）
- 评审者: cursor cloud agent (auto mode, reviewer subagent)
- 日期: 2026-04-18
- Worktree branch: `cursor/f003-quality-chain-3d5f`
- Workspace isolation: `in-place`
- 上游已通过:
  - `docs/reviews/test-review-F003-garage-memory-auto-extraction-r3.md`（test review r3 = 通过；针对 +8 fresh-evidence 测试与 r2 基线复检）
  - `docs/reviews/test-review-F003-garage-memory-auto-extraction-r2.md`（r2 基线快照）
- 上游 r1 review: `docs/reviews/code-review-F003-garage-memory-auto-extraction.md`（结论 = 需修改）
- 实现交接块:
  - `docs/verification/F003-code-review-r1-handoff.md`（r1 → r2 回修主交接块；同时声明 finding 5 显式延后）
  - `docs/verification/F003-test-review-r1-handoff.md`（test review r1 后的合并批次基线）
  - `docs/verification/F003-T1-implementation-handoff.md`（T1）
- 关联工件:
  - 规格 `docs/features/F003-garage-memory-auto-extraction.md`
  - 设计 `docs/designs/2026-04-18-garage-memory-auto-extraction-design.md`
  - 任务计划 `docs/tasks/2026-04-18-garage-memory-auto-extraction-tasks.md`
  - 上游 approvals `docs/approvals/F003-spec-approval.md` / `F003-design-approval.md` / `F003-tasks-approval.md`
  - 进度 `task-progress.md`
  - 平台默认配置 `.garage/config/platform.json`
- 评审实现资产:
  - `src/garage_os/memory/__init__.py`
  - `src/garage_os/memory/types.py`
  - `src/garage_os/memory/candidate_store.py`
  - `src/garage_os/memory/extraction_orchestrator.py`
  - `src/garage_os/memory/publisher.py`
  - `src/garage_os/memory/conflict_detector.py`
  - `src/garage_os/memory/recommendation_service.py`
  - `src/garage_os/runtime/session_manager.py`
  - `src/garage_os/runtime/skill_executor.py`
  - `src/garage_os/cli.py`
  - `src/garage_os/knowledge/knowledge_store.py`
  - `src/garage_os/knowledge/experience_index.py`
  - `src/garage_os/types/__init__.py`
- 当次回归证据（reviewer 独立复跑）: `pytest tests/ -q` → `384 passed in 24.63s`（与 r1 follow-up 交接块 GREEN 摘要一致，零回归）
- 当次手工探针:
  - 端到端 archive → orchestrator → publisher：`decision / pattern / experience_summary` 三类候选都成功落库；`source_evidence_anchor`（`artifact_excerpt` / `session_metadata`）非 None；`experience_records/*.json` 含完整 `task_type / source_evidence_anchors`；publisher 命中相似条目时未传 `conflict_strategy` 抛 `ValueError("...FR-304 requires explicit user choice...")`，传 `coexist` 后正常发布
  - FR-307 异常路径：`monkeypatch _generate_candidates → RuntimeError`，磁盘 `memory/candidates/batches/batch-...json` 写入 `evaluation_summary=extraction_failed` 与 `metadata.error="RuntimeError: boom"`
  - `SessionManager.update_session` 中 `context_metadata` 分支只剩 1 条（line 136），dead code 已清理

## 结论

**通过**

r1 标注的 3 项 important + 3 项 minor 全部按交接块 `docs/verification/F003-code-review-r1-handoff.md` 的承诺定向闭合：

1. `experience_summary` 候选契约漂移（CR1/CR3）：orchestrator 在 `_generate_candidates` 里为该候选补齐 `task_type / skill_ids / tech_stack / domain / problem_domain / outcome / duration_seconds / complexity / recommendations`；publisher `_to_experience_record` 与 `_to_knowledge_entry` 全面改用 `payload.get(...)` + 显式默认值，裸下标 `KeyError` 路径已消除。手工探针 + contract 单测共同确认四类候选闭环。
2. 自动提取候选缺 `source_evidence_anchors`（CR2）：`_generate_candidates` 为每条 signal 调用 `_build_anchor`，按 `artifact / metadata_tags / problem_domain / 其它 session metadata` 构造自描述锚点；publisher 落库后 `KnowledgeEntry.source_evidence_anchor` 与 `ExperienceRecord.source_evidence_anchors` 均非空且 `ref` 可解析回 `sessions/archived/<id>/session.json#<field>`，对齐设计 §11.6 不变量与 FR-302b。
3. CLI accept 路径绕过 FR-304（CR2/CR3）：`KnowledgePublisher.publish_candidate` 新增 `conflict_strategy` 参数，命中 `similar_entries` 时未显式传值即抛 `ValueError`；CLI `--strategy=coexist|supersede|abandon` 与 `--action=abandon` 全部接出，`abandon` 走 publisher 早返回路径并把候选状态置 `abandoned`。canonical surface 与底层行为对齐，静默 supersede 路径已封堵。
4. `SessionManager.update_session` dead code（CR4/CA5）：第二条不可达 `elif key == "context_metadata"` 已移除，仅保留单条合并语义分支。
5. FR-307 错误未持久化（CR3）：orchestrator 在 `_generate_candidates` 抛错时归一化为 `evaluation_summary=extraction_failed` batch 写盘，`metadata.error` 含异常类型 + 消息，FR-307 第 2/3 条在文件层有可机器读取证据。
6. publisher 用 `candidate_id` 当 `KnowledgeEntry.id`（CR2/CR4，r1 finding 5）：r1 follow-up handoff 显式延后，理由是修复需要 `KnowledgeStore` 引入独立 ID 体系，超出 1-2 轮可消化范围。reviewer 接受该延后判断（详见下文"finding 5 延后接受度"）。

6 维度评分全部 ≥7/10，关键维度 CR1/CR2/CR3 全部 ≥7/10，384 个测试全绿无回归，可放行进入 `hf-traceability-review`。

## 多维评分（0-10，括号内为 r1 → r2 变化）

| 维度 | r2 评分 | 说明 |
|------|---------|------|
| `CR1` 正确性 | 9 (6 → 9) | 端到端探针证实 `decision / pattern / solution / experience_summary` 四类候选全部可落库；`experience_summary` 候选不再抛 `KeyError`；orchestrator + publisher 之间的字段契约由 `test_publish_orchestrator_output_end_to_end` contract test 锁住 |
| `CR2` 设计一致性 | 9 (5 → 9) | 自动提取候选必带 `source_evidence_anchors`（设计 §11.6 / FR-302b）；CLI / publisher 显式暴露三选一 + `abandon`（设计 §9.4 / FR-304）；CLI canonical surface 与 publisher 行为对齐。仅剩 `candidate_id` 复用作 `KnowledgeEntry.id` 的弱设计耦合（finding 5）显式延后 |
| `CR3` 状态 / 错误 / 安全 | 8 (7 → 8) | publisher 不再抛裸 `KeyError`；冲突未给策略时显式 `ValueError`；orchestrator 异常→ `extraction_failed` batch 持久化；session 侧 `_trigger_memory_extraction` 仍 logger.warning（可接受，FR-307 文件级证据已由 orchestrator 提供） |
| `CR4` 可读性与可维护性 | 8 (7 → 8) | dead code 清理；publisher / orchestrator 字段命名清晰；仅留两个非阻塞 stale：`extraction_orchestrator.py:68` 的 `# pragma: no cover` 已被 `test_extraction_failure_writes_error_batch` 稳定覆盖，注释成 stale |
| `CR5` 范围守卫 | 9 (9 → 9) | 仍未引入超出规格 / 设计的能力；CLI 命令面只新增 r1 交接块声明的 `--strategy` 与 `--action=abandon`，对齐设计 §9.8 |
| `CR6` 下游追溯就绪度 | 9 (7 → 9) | r1 follow-up 交接块齐全可冷读；公开锚点能反向解析回 archived session；publisher / orchestrator 契约面有合约级测试。`hf-traceability-review` 可对"已发布数据可被回读到原 session/anchor"给出 unconditional 通过 |

> 关键维度全部 ≥7/10，按 `references/review-checklist.md` 评分辅助规则可返回 `通过`。

## r1 → r2 finding 闭合矩阵

| r1 finding | severity / rule_id | r2 状态 | 闭合证据 |
|------------|--------------------|---------|----------|
| F1 `experience_summary` 候选喂给 publisher 抛 `KeyError: 'task_type'` | important / CR1, CR3 | **关闭** | `extraction_orchestrator.py:260-273` 在 `candidate_type == "experience_summary"` 时补齐 publisher 必须字段；`publisher.py:149-176` `_to_experience_record` 改 `payload.get(...) or default`。手工探针 `experience-summary` 候选成功落库为 `ExperienceRecord(task_type='pack-A', ...)`。覆盖测试：`tests/memory/test_extraction_orchestrator.py::test_extract_emits_complete_experience_summary_candidate` + `tests/memory/test_publisher.py::test_publish_orchestrator_output_end_to_end` |
| F2 自动提取候选缺 `source_evidence_anchors`，发布后 `KnowledgeEntry.source_evidence_anchor=None` | important / CR2 | **关闭** | `extraction_orchestrator.py:244` 调用 `_build_anchor`，每条 signal 都带自描述锚点；`publisher.py:127-133` 把首个 anchor 写入 `entry.source_evidence_anchor` 与 `front_matter`。手工探针落库后 4 条 entry 全部具备非空 anchor（`artifact_excerpt` 或 `session_metadata`）。覆盖测试：`tests/memory/test_extraction_orchestrator.py::test_extract_attaches_source_evidence_anchors` + contract test 中 `entry.source_evidence_anchor is not None` 双断言 |
| F3 CLI accept 路径不暴露 coexist/supersede/abandon 三选一 | important / CR2, CR3 | **关闭** | `publisher.py:29-95` 新增 `VALID_CONFLICT_STRATEGIES` 与 `conflict_strategy` 必传校验；`cli.py:483-492` 在 `accept`/`edit_accept` 命中相似条目时强制 `--strategy`，未传则打印提示并 `return 1`；`cli.py:611-637` 把 `abandon` 加入 `--action`，`--strategy` 暴露三选一；`cli.py:520-521` 处理 `accept --strategy=abandon` 收束到 `abandoned` 状态。覆盖测试：publisher 三向覆盖（`coexist` / `supersede` / `abandon` / 不传抛错）+ CLI `test_memory_review_accept_requires_strategy_when_conflict_exists` + `test_memory_review_abandon_skips_publication` |
| F4 `SessionManager.update_session` 第二个 `context_metadata` 分支不可达 | minor / CR4, CA5 | **关闭** | `runtime/session_manager.py:136-143` 仅保留单条合并语义分支；`grep "context_metadata"` 仅返回 1 处。 |
| F5 publisher 用 `candidate_id` 当 `KnowledgeEntry.id`，重复 accept 静默覆盖 | minor / CR2, CR4 | **延后接受**（见"finding 5 延后接受度"） | r1 follow-up handoff "剩余风险" 已记录，理由：修复需要 `KnowledgeStore` 引入独立 ID 体系（带版本后缀或独立 ID），属于设计层修补，超出 r1→r2 1-2 轮可消化范围。F003 第一版用户量小、单 candidate 重复 accept 不在主使用路径上，r2 可接受现状；需在 traceability review 期间或独立 hotfix 中正式裁决 |
| F6 `_trigger_memory_extraction` 失败仅 `logger.warning`，FR-307 错误未在文件层留痕 | minor / CR3 | **关闭（在 orchestrator 层落盘）** | `extraction_orchestrator.py:64-81` 把 `_generate_candidates` 异常归一化为 `evaluation_summary=extraction_failed` batch 写盘，`metadata.error` 含 `f"{type(exc).__name__}: {exc}"`。手工探针在磁盘上观察到 `batch-...json` 含 `extraction_failed` 与 `error="RuntimeError: boom"`。session 侧仍走 logger.warning，但文件级证据由 orchestrator 提供，FR-307 第 2/3 条满足。覆盖测试：`tests/memory/test_extraction_orchestrator.py::test_extraction_failure_writes_error_batch` |

## 发现项

> r2 不再产生 important/critical 级 finding。以下条目均为 r1 review 与 test-review r3 已经标注的低优非阻塞遗留，记录在此供 traceability / completion gate 阶段一并裁决。

- `[minor][USER-INPUT][CR2/CR4]` `KnowledgePublisher` 仍以 `candidate_id` 直接当 `KnowledgeEntry.id`/`ExperienceRecord.record_id`，且 confirmation_ref 也以 `batch_id` 命名。同一 candidate 重复 `accept` / `edit_accept` 会原地覆盖前次发布，`KnowledgeStore.update()` 的 `version+=1` 链路被绕过。r1 follow-up handoff 显式延后，理由是需要 `KnowledgeStore` 引入独立 ID 体系。建议在 `hf-traceability-review` 阶段以 USER-INPUT 形式正式裁决：接受现状作为 F003 v1 行为，或开 hotfix 单独修复。详见 `docs/verification/F003-code-review-r1-handoff.md` "剩余风险 / 未覆盖项"。
- `[minor][LLM-FIXABLE][CR4]` `src/garage_os/memory/extraction_orchestrator.py:68` 的 `# pragma: no cover - defensive: persisted instead of raising` 注释已经 stale：`tests/memory/test_extraction_orchestrator.py::test_extraction_failure_writes_error_batch` 稳定覆盖该 except 分支。建议下次顺手清理该 pragma 注释（可 hotfix，可在下一次顺手 PR 中移除），不阻塞 r2。
- `[minor][LLM-FIXABLE][CR5/CR4]` CLI `--action=abandon` 与 `--action=accept --strategy=abandon` 在效果上重叠（两者都把候选置 `abandoned` 且不发布），区别只在前者无视冲突探测、后者仅在冲突时生效。r1 follow-up handoff 已显式记录该重叠为可接受。如未来产品侧要严格区分"主动放弃整条候选" vs "因冲突放弃发布"，再独立任务推进。当前不阻塞。
- `[minor][LLM-FIXABLE][CR3]` `KnowledgePublisher.publish_candidate` 在 `similar_entries` 为空时若调用方误传 `conflict_strategy="garbage"`，目前不会校验 `VALID_CONFLICT_STRATEGIES`（只在有冲突分支才校验）。建议把 `VALID_CONFLICT_STRATEGIES` 校验提前到入口（无论是否有冲突），让 strict 行为对调用方更可预期。test-review r3 "下一步" 已点名提示。**不阻塞 r2**，可在 traceability/completion 阶段顺手清理。
- `[minor][LLM-FIXABLE][CR3]` `SessionManager._trigger_memory_extraction` 仍走 `logger.warning(..., exc_info=True)` 兜底（line 230-236），未把"session 侧 archive-time 触发提取的失败"再额外写入 `sessions/archived/<id>/memory-extraction-error.json`。设计 §14.2 的"持久化错误摘要"目前由 orchestrator 层 batch 文件承担。reviewer 判断这是合理的单点持久化（避免双写），但若 traceability 要求"session-level 触发证据"也持久化，可顺手补一条 minimal 写盘。**不阻塞 r2**。

## finding 5 延后接受度

按任务指令"判断 finding 5 是否可在 r2 接受为延后"：

- **接受延后**。理由：
  1. r1 review 给出 severity = minor，明确非阻塞
  2. r1 follow-up handoff `docs/verification/F003-code-review-r1-handoff.md` 的"剩余风险 / 未覆盖项"已显式声明延后，并给出技术理由（需要 KnowledgeStore 层引入独立 ID 体系，属于设计层而非实现层 1-2 轮可消化的修补）
  3. F003 第一版主使用路径是"自动提取 → 用户在 CLI accept 一次"，重复 `accept` 同一 candidate 的真实场景极少；CLI 同一 candidate 重复 accept 会被新引入的 conflict 探测在第二次时拦截（同 title/同 tag 触发 similar_entries），需要用户显式选 `--strategy`，已经不再"完全静默"
  4. test-review r3 已把该缺口列入 USER-INPUT minor，建议在 code-review r2 / traceability 期间裁决——本 r2 接受延后，traceability review 可继续以 USER-INPUT 形式留给真人或独立 hotfix 决策
  5. 不引入安全 / 数据丢失风险（旧条目仍可从 git history 恢复，且 `published_from_candidate` 字段保留出处）

如 traceability review 或 completion gate 不接受该延后，可独立开一条 hotfix 任务（"为 KnowledgeEntry 引入与 candidate_id 解耦的发布 ID 体系"），不影响 F003 r2 进入 traceability。

## 代码风险与薄弱项

- F003 v1 单 candidate 重复 accept 仍有"原地覆盖前次发布"的弱耦合，已在 finding 5 延后说明
- `KnowledgePublisher.VALID_CONFLICT_STRATEGIES` 校验只在 `similar_entries` 非空时生效，对调用方误传值的容错度略低（minor，可顺手清理）
- `extraction_orchestrator.py:68` 的 `# pragma: no cover` 注释已 stale，覆盖率统计可能因此漏算 FR-307 异常分支的真实覆盖
- `_trigger_memory_extraction` 单点 logger.warning 兜底，靠 orchestrator 层 batch 文件承担 FR-307 持久化；如 session 侧触发链路本身崩溃（例如 orchestrator 实例化失败），仍只在 logger 留痕。设计 §14.2 第 2/3 条对"session-level 触发证据"的强度可在 traceability 阶段确认

## 范围守卫与可读性

- 没有顺手引入超出规格 / 设计的新能力
- CLI canonical surface 仅新增 `--action=abandon` + `--strategy=coexist|supersede|abandon`，与 r1 follow-up handoff 一致，对齐设计 §9.4 / §9.8 与 FR-304
- `memory/` 子模块仍保持单职责（candidate_store / extraction_orchestrator / publisher / conflict_detector / recommendation_service）
- `_build_anchor` 是干净的 helper，按 signal kind 分发，便于未来扩展新锚点类型
- `_to_knowledge_entry` / `_to_experience_record` 的字段映射全部 `.get()` + default，未来新增可选字段不会再破坏调用方

## 关于路由判断

- 实现交接块（T1 + r1 回流合并 + r1 follow-up）齐全，可冷读，触碰工件可逐行定位
- 测试套件 `pytest tests/ -q` 全套 384 passed，与交接块 GREEN 摘要一致，无回归
- 上游 stage / route / profile 一致；`test-review r3` 已通过且推荐 `hf-code-review`
- r2 review 不再产生 important findings；遗留 minor 全部为已知低优 / USER-INPUT 延后项，不构成 stage / route / profile / 上游证据冲突

不需要 reroute via router。

## 下一步

- `hf-traceability-review`：从规格 → 设计 → 实现 → 测试 → 已发布工件全链路核对锚点；重点确认
  1. F003 四类候选（含 `experience_summary`）的发布产出能反向解析回 `sessions/archived/<id>/session.json` 的 `tags / problem_domain / artifacts`，且 `confirmation_ref` 与 `published_from_candidate` 在 markdown front matter 与 `experience_records/*.json` 中均可读
  2. FR-304 三选一在 CLI / publisher 双层是否各有可机器读取证据
  3. FR-307 错误摘要在 `memory/candidates/batches/*.json` 是否可被独立解读为"提取失败发生过 + session 关联 + 错误类型/消息"
  4. finding 5（candidate_id 复用）按 USER-INPUT 延后处理，必要时升级为独立 hotfix 任务

## 结构化返回（供父会话路由）

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "hf-traceability-review",
  "record_path": "docs/reviews/code-review-F003-garage-memory-auto-extraction-r2.md",
  "key_findings": [
    "[r1→关闭][CR1/CR3] experience_summary 候选 KeyError：orchestrator 补齐 task_type/domain/problem_domain/outcome/duration_seconds 等字段；publisher 改 .get()+default；端到端探针 + contract 单测双重确认四类候选闭环",
    "[r1→关闭][CR2] source_evidence_anchors 缺失：_build_anchor 为每条 signal 构造 artifact_excerpt 或 session_metadata 锚点；落库后 KnowledgeEntry.source_evidence_anchor 与 ExperienceRecord.source_evidence_anchors 均非空且 ref 可解析回 archived session",
    "[r1→关闭][CR2/CR3] FR-304 三选一：publisher 命中相似条目未传 conflict_strategy 抛 ValueError；CLI 暴露 --strategy=coexist|supersede|abandon 与 --action=abandon；canonical surface 与底层行为对齐",
    "[r1→关闭][CR4/CA5] SessionManager.update_session 重复 context_metadata 分支已删除，仅保留单条合并语义分支",
    "[r1→关闭][CR3] FR-307 错误持久化：orchestrator 把 _generate_candidates 异常归一化为 evaluation_summary=extraction_failed batch 写盘，metadata.error 含异常类型+消息",
    "[r1 finding 5 延后接受][minor][USER-INPUT] publisher 用 candidate_id 当 KnowledgeEntry.id 仍未修复，按 r1 follow-up handoff 显式延后；理由：需要 KnowledgeStore 引入独立 ID 体系，属设计层修补；建议 traceability/completion 阶段裁决或开独立 hotfix",
    "[非阻塞 minor 提示] extraction_orchestrator.py:68 # pragma: no cover 已 stale；publisher VALID_CONFLICT_STRATEGIES 仅在 similar_entries 非空时校验；CLI --action=abandon 与 accept --strategy=abandon 语义重叠；session 侧 _trigger_memory_extraction 仍 logger.warning 兜底（可接受，文件级证据由 orchestrator 提供）"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "minor",
      "classification": "USER-INPUT",
      "rule_id": "CR2",
      "summary": "publisher 用 candidate_id 当 KnowledgeEntry.id，重复 accept 静默覆盖；按 r1 follow-up handoff 显式延后到 traceability/独立 hotfix"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "CR4",
      "summary": "extraction_orchestrator.py:68 的 # pragma: no cover 注释已被 test_extraction_failure_writes_error_batch 稳定覆盖，已成 stale"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "CR3",
      "summary": "publisher.publish_candidate 仅在 similar_entries 非空时校验 VALID_CONFLICT_STRATEGIES，建议入口处提前校验"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "CR5",
      "summary": "CLI --action=abandon 与 --action=accept --strategy=abandon 语义重叠，待产品侧确认是否需要差异化"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "CR3",
      "summary": "SessionManager._trigger_memory_extraction 仍走 logger.warning，文件级 FR-307 证据由 orchestrator batch 文件承担；session 触发链路自身失败时只剩 logger"
    }
  ]
}
```
