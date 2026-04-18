# Code Review — F003 Garage Memory 自动知识提取与经验推荐

- 评审范围: F003 全量实现（T1-T9）+ test-review r1 回流修订后的实现代码
- Review skill: `hf-code-review`
- Review 轮次: r1
- 评审者: cursor cloud agent (auto mode, reviewer subagent)
- 日期: 2026-04-18
- Worktree branch: `cursor/f003-quality-chain-3d5f`
- Workspace isolation: `in-place`
- 上游已通过: `docs/reviews/test-review-F003-garage-memory-auto-extraction-r2.md`（test review r2 = 通过）
- 实现交接块:
  - `docs/verification/F003-T1-implementation-handoff.md`（T1）
  - `docs/verification/F003-test-review-r1-handoff.md`（合并批次 + r1 回流修订）
- 关联工件:
  - 规格 `docs/features/F003-garage-memory-auto-extraction.md`
  - 设计 `docs/designs/2026-04-18-garage-memory-auto-extraction-design.md`
  - 任务计划 `docs/tasks/2026-04-18-garage-memory-auto-extraction-tasks.md`
  - 上游 approvals `docs/approvals/F003-spec-approval.md` / `F003-design-approval.md` / `F003-tasks-approval.md` / `F003-T1-test-design-approval.md`
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
- 当次回归证据: `pytest tests/ -q` → `376 passed in 24.60s`

## 结论

**需修改**

测试套件全绿，r1 回流修订（关闭分支、supersede/abandon、truncation、FR-302b 校验）已落到位，模块边界与目录契约也基本贴合设计。但本次手工探针发现了三条 important 级缺陷，全部位于设计 §11.4 / §11.6 / §9.4 / FR-302b / FR-304 的硬约束面上，单元测试因 fixture 形状特殊未触发。具体见下文 finding 1/2/3。这些缺陷可在 1-2 轮 `hf-test-driven-dev` 内定向修补（补 fail-first 测试 + 最小实现），不属于需要重新编排的 router blocker，因此走 `需修改` 而不是 `阻塞`。

## 多维评分（0-10）

| 维度 | 评分 | 说明 |
|------|------|------|
| `CR1` 正确性 | 6 | T1-T9 主链单测全绿；但 `KnowledgePublisher` 在自动提取产出的 `experience_summary` 候选上实测会抛 `KeyError: 'task_type'`（finding 1），核心闭环对四类候选并非全部安全 |
| `CR2` 设计一致性 | 5 | 自动提取候选未携带 `source_evidence_anchors`，导致已发布 `KnowledgeEntry.source_evidence_anchor=None`（finding 2），违反设计 §11.6 不变量与 FR-302b；CLI accept 路径不向用户暴露冲突选择，违反 FR-304 与设计 §9.4（finding 3） |
| `CR3` 状态 / 错误 / 安全 | 7 | `_trigger_memory_extraction` 用 `try/except + logger.warning` 兜底，FR-307 降级正确；但 finding 1 暴露 publisher 在真实归档证据上会以未捕获异常向上抛，CLI `_memory_review` accept 分支会让用户看到 traceback |
| `CR4` 可读性与可维护性 | 7 | 大多数模块命名清晰、职责单一；`SessionManager.update_session` 有重复且不可达的第二个 `elif key == "context_metadata"` 分支（finding 4） |
| `CR5` 范围守卫 | 9 | 没有顺手引入超出规格/设计的能力；CLI 命令面就是设计 §9.8 描述的 canonical surface |
| `CR6` 下游追溯就绪度 | 7 | 交接块齐全可冷读，回归基线明确；但 finding 1/2 让 traceability review 无法对"已发布数据可被回读到原 session/anchor"这一硬条款给出 unconditional 通过 |

> 关键维度 `CR2`=5 < 6，按 checklist 评分辅助规则不得返回 `通过`。

## 发现项

### Finding 1 — `experience_summary` 自动提取候选发布时抛 `KeyError`

- **severity**: important
- **classification**: LLM-FIXABLE
- **rule_id**: CR1（正确性）/ CR3（状态-安全）
- **位置**: `src/garage_os/memory/publisher.py:128-155` `_to_experience_record` ↔ `src/garage_os/memory/extraction_orchestrator.py:179-239` `_generate_candidates`
- **现象**:
  - `MemoryExtractionOrchestrator._generate_candidates` 在 `signal["kind"] == "problem_domain"` 时把候选 `candidate_type` 设为 `experience_summary`，但生成的 candidate dict 只有 `candidate_id / candidate_type / session_id / source_artifacts / match_reasons / status / priority_score / title / summary / content / tags / schema_version`。
  - `KnowledgePublisher._to_experience_record` 直接用 `payload["task_type"]` / `payload["domain"]` / `payload["problem_domain"]` / `payload["outcome"]` / `payload["duration_seconds"]` 等键。
  - 一次端到端试跑（archive → orchestrator → CLI accept → publish）会在 publisher 处抛 `KeyError: 'task_type'`：

    ```text
    chosen candidate_type: experience_summary
    PUBLISH FAILED: KeyError 'task_type'
    ```

- **为什么单测没抓到**: `tests/memory/test_publisher.py::experience_summary_candidate` 是一个手工补齐了 `task_type / skill_ids / domain / problem_domain / outcome / duration_seconds / complexity / recommendations` 的 fixture；`tests/integration/test_e2e_workflow.py::test_memory_pipeline_e2e_flow` 的 archived session 不带 `problem_domain`，因此根本不会落到 `experience_summary` 分支。两个测试都没有覆盖"orchestrator 自动产出的 `experience_summary` 候选 → publisher 接受 → 写入 experience"这条真实路径。
- **风险**: 直接破坏 F003 主闭环对 FR-302a 第四类候选的契约，并让 CLI `garage memory review --action accept` 在用户面前抛栈。属于 publisher 与 orchestrator 之间的字段契约漂移。
- **建议修法（不在本次评审改）**:
  1. 在 orchestrator 端补齐 `experience_summary` 候选所需的最小字段（`task_type` / `domain` / `problem_domain` / `outcome` / `duration_seconds` 等），可以从 archived session metadata + experience_records 推导；
  2. 在 publisher 端用 `payload.get(...)` + 显式 default + 友好的 `ValueError` 取代裸下标，避免暴露 `KeyError` 给上层；
  3. 加 fail-first 测试：用 orchestrator 自身产出的 candidate dict 直接喂给 publisher，断言落入 `ExperienceIndex` 的记录字段完整。

### Finding 2 — 自动提取 → 发布后 `source_evidence_anchor` 为 `None`，违反设计 §11.6 不变量

- **severity**: important
- **classification**: LLM-FIXABLE
- **rule_id**: CR2（设计一致性）
- **位置**: `src/garage_os/memory/extraction_orchestrator.py:218-233` `_generate_candidates` ↔ `src/garage_os/memory/publisher.py:106-126` `_to_knowledge_entry`
- **现象**:
  - orchestrator 生成的候选 dict 不写 `source_evidence_anchors` 字段。
  - `_to_knowledge_entry` 用 `payload.get("source_evidence_anchors", [{}])[0] if payload.get("source_evidence_anchors") else None`，自动提取分支必然落到 `None`。
  - 实测 archive → orchestrator → publisher accept 后：

    ```text
    chosen candidate_type: decision
    source_evidence_anchor: None
    confirmation_ref: ref
    source_artifact: a.md
    ```

- **违约**:
  - 设计 §11.6 关键不变量第 6 条："已发布正式数据必须包含 `confirmation_ref` 与至少一个 `source_evidence_anchor`"。
  - 规格 FR-302b："候选必须包含…至少一个来源锚点"，并且要在发布后保留可回读。
  - 设计 §11.4 `KnowledgeEntry` 扩展字段示例直接列出了 `source_evidence_anchor: kind=artifact_excerpt …`。
- **风险**: traceability review 与 NFR-301 全链路可追溯性失去机器可校验的锚点；只剩 `source_artifact` 单一路径串。
- **为什么单测没抓到**: `tests/memory/test_publisher.py` 全部 fixture 都人工塞了 `source_evidence_anchors`，没有一条用例验证"orchestrator 实际产出 → publisher 落库"后的字段完整性。
- **建议修法**:
  1. 在 `_generate_candidates` 里以"signal kind + 路径"构造最小 anchor，例如 `{"kind": signal["kind"], "ref": signal["value"]}`；如有 artifact path，落 `kind=artifact_excerpt`。
  2. 在 publisher 端如果 anchors 仍为空，则按设计 §11.6 直接拒绝发布并写入 batch 错误摘要，避免破坏不变量。
  3. 加 fail-first 测试：用 orchestrator 产物 publish 后断言 `entry.source_evidence_anchor is not None` 且 `entry.front_matter["source_evidence_anchor"]["ref"]` 可解析回原 archived session 的 artifact / metadata。

### Finding 3 — CLI accept 路径绕过 FR-304"用户显式选择 coexist/supersede/abandon"

- **severity**: important
- **classification**: LLM-FIXABLE
- **rule_id**: CR2（设计一致性）/ CR3（状态-安全）
- **位置**: `src/garage_os/cli.py:466-510` `_memory_review` ↔ `src/garage_os/memory/publisher.py:58-76` accept 分支
- **现象**:
  - CLI `--action` 限制在 `{accept, edit_accept, reject, batch_reject, defer, show-conflicts}`，**没有 `abandon`**；用户拿到 `show-conflicts` 输出后唯一能做的写入动作就是 `accept`/`edit_accept`/`reject`。
  - publisher 的 `accept`/`edit_accept` 分支调用 `ConflictDetector.detect`，如果返回 `supersede` 就**自动**把旧条目 ID 写进 `entry.related_decisions` 与 `front_matter["supersedes"]`，用户没有"我只想 coexist"或"我想 abandon"的入口。
  - publisher 内部支持 `action="abandon"`，但 CLI canonical surface 并未把它接出来，等价于"代码会做、但用户面不允许选"。
- **违约**:
  - 规格 FR-304："系统必须显式提示用户处理该关系，而不能静默覆盖已有知识"，并要求"提供至少'并存''替换/更新''放弃发布'三类处理结果中的可选项"。
  - 设计 §9.4 `ConflictDetector` 职责："生成冲突建议：coexist / supersede / abandon"——当前实现只生成 `coexist | supersede` 两类，且 CLI 把建议直接当成执行而不是建议。
- **风险**:
  - 静默覆盖：用户接受候选时，只要标题或任一标签与历史条目重叠，就会自动写 supersede；用户既不知道也无法选择 coexist。
  - canonical surface 与底层 publisher 行为不一致：`abandon` 仅有单测覆盖，没有 CLI / 用户路径。
- **为什么单测没抓到**: 当前 `test_publisher.py` 只验证"如果 action=abandon 则不发布""如果 supersede 则写关系"，没有断言"用户必须能在 surface 上选择三选一"。CLI 测试也没有覆盖冲突时的交互。
- **建议修法**:
  1. 在 `ConflictDetector` 输出里同时暴露 `coexist / supersede / abandon` 候选项，并附 `recommended_strategy`；
  2. 在 CLI `--action` 里把 `abandon` 加进允许集合，并在 `accept`/`edit_accept` 命中相似条目时强制要求显式 `--strategy=coexist|supersede|abandon`；
  3. publisher 里把"是否写 supersede 关系"参数化，由 CLI/上层决定，不在 publisher 隐式生效；
  4. 补 fail-first 测试：相似条目存在时 `garage memory review --action accept` 不带 `--strategy` 应当报错而不是静默 supersede。

### Finding 4 — `SessionManager.update_session` 有重复且不可达的 `context_metadata` 分支

- **severity**: minor
- **classification**: LLM-FIXABLE
- **rule_id**: CR4（可读性）/ CA5（dead code）
- **位置**: `src/garage_os/runtime/session_manager.py:136-150`
- **现象**: 第 136-143 行已经处理了 `key == "context_metadata"`，但 146-150 行又写了一遍同名 `elif`，因 Python 短路永不可达。两段逻辑也不完全一致（前者用 `existing_metadata = context.get("metadata", {})`，后者用 `metadata = context.setdefault("metadata", {})`）。
- **风险**: 维护时容易误以为后者生效；如果将来有人改其中一段，行为会脱节。
- **建议修法**: 删除 146-150 的重复分支；如有需要差异化合并语义，再以一个明确的 `key` 区分。

### Finding 5 — `KnowledgePublisher` 用 `candidate_id` 当 `KnowledgeEntry.id`，重复 accept 会静默覆盖

- **severity**: minor
- **classification**: LLM-FIXABLE
- **rule_id**: CR2（设计一致性，弱）/ CR4（可维护性）
- **位置**: `src/garage_os/memory/publisher.py:113-125`
- **现象**: `entry.id = payload["candidate_id"]`，文件名 `decision-<candidate_id>.md`。同一个 `candidate_id` 触发两次 `accept`/`edit_accept`（例如先 accept 后 edit_accept），后者会原地覆盖前者，且 `KnowledgeStore.update()` 的 `version+=1` 链路并不会被走到。
- **风险**: F003 第一版用户量小，但与设计 §11.4 / NFR-301 的"已发布条目状态变化可回读"目标弱耦合。当前 CLI 也允许重复 `accept` 同一 candidate。
- **建议修法**: publisher 在已有同名 entry 时改走 `KnowledgeStore.update`（或显式 reject 重复 publish），并把 `published_id` 与 `candidate_id` 解耦（带版本后缀或独立 ID）。

### Finding 6 — `_trigger_memory_extraction` 仅写 logger.warning，未把失败摘要回写到 batch / session

- **severity**: minor
- **classification**: LLM-FIXABLE
- **rule_id**: CR3（错误处理）
- **位置**: `src/garage_os/runtime/session_manager.py:233-241`
- **现象**: 异常被 `logger.warning(..., exc_info=True)` 吞掉，但设计 §14.2 与 FR-307 验收标准第 2 条要求"系统保存错误摘要、时间和关联 session"。当前没有 `batch.json` 或 `session.json` 上的痕迹，仅留在标准 logger（不一定持久化）。
- **风险**: 用户从 `.garage/` 工件无法独立还原"提取失败发生过"。FR-307 第 3 条"用户能明确区分 session 成功与提取失败"在文件层面失证。
- **建议修法**: 在 `except` 分支里补一条 `candidate_store.store_batch({... "evaluation_summary": "extraction_failed", "metadata": {"error": str(exc), "occurred_at": ...}})`，或把错误写进 `sessions/archived/<id>/memory-extraction-error.json`。

## 代码风险与薄弱项

- F003 实测 happy path 在 4 类候选中只有 `decision / pattern / solution` 跑得通；`experience_summary` 真实分支会抛 `KeyError`，traceability review 不可基于现有证据宣称"四类候选闭环"。
- 自动提取产出的所有候选目前都丢失 `source_evidence_anchors`，使 NFR-301 与设计 §11.6 不变量在工件层失守；后续推荐基于已发布条目的来源回溯能力被削弱。
- CLI 是设计 §9.8 指定的 canonical surface，但当前 `garage memory review` 的 accept 路径无法暴露设计 §9.4 的三类策略，FR-304 用户主导精神被弱化。
- 上述三处缺陷的共同根因是"`tests/memory/` 的 fixture 与 `orchestrator` 的真实输出形状分叉"——publisher 与 orchestrator 间没有契约级合约测试。建议在回修时为 publisher 增加一组 contract test，专门用 orchestrator 的真实产物作为输入。
- 次要项：`SessionManager.update_session` 重复分支、publisher 的 candidate_id 复用 entry id、`_trigger_memory_extraction` 失败仅 logger 化，都属于"现在不阻塞但容易被未来需求放大"的小坑。

## 范围守卫与可读性

- `memory/` 子模块边界与 `KnowledgeStore` / `ExperienceIndex` 边界清晰，没有把候选治理塞进现有 KnowledgeIntegration（符合 ADR-001）。
- 候选目录与正式知识目录分离正确（符合 ADR-002）。
- `RecommendationService` 的启发式实现简洁、可读、可关闭（符合 ADR-003 与 FR-305）。
- `extraction_orchestrator` 与 `archive_session` 通过可选注入参数解耦，便于测试（符合 FR-307 防阻塞要求）。
- `cli.py::_run` 在 `recommendation_enabled=False` 时短路，配置开关与运行时一致（符合 T4 验收）。

## 关于路由判断

- 实现交接块（T1 + r1 回流合并交接块）齐全、可冷读，触碰工件可逐行定位
- 测试套件 `pytest tests/ -q` 全套 376 passed，无回归
- 上游 stage / route / profile 一致，test review r2 已通过且推荐 `hf-code-review`
- 本轮三条 important findings 都是代码层缺陷，可在 1-2 轮 `hf-test-driven-dev` 中定向闭环（补 fail-first 测试 + 最小实现修复），不构成 stage / route / profile / 上游证据冲突

不需要 reroute via router。

## 下一步

- `hf-test-driven-dev`：在不重新拆任务的前提下，针对 finding 1/2/3 各补一组 fail-first 测试，再做最小实现修补；finding 4/5/6 视实现成本顺手清理
- 修订完成后回到 `hf-test-review`（增量轮）→ `hf-code-review` r2 → `hf-traceability-review`

## 结构化返回（供父会话路由）

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-test-driven-dev",
  "record_path": "docs/reviews/code-review-F003-garage-memory-auto-extraction.md",
  "key_findings": [
    "[important][LLM-FIXABLE][CR1/CR3] orchestrator 产出的 experience_summary 候选喂给 KnowledgePublisher 时抛 KeyError: 'task_type'，F003 第四类候选闭环不通",
    "[important][LLM-FIXABLE][CR2] 自动提取候选未携带 source_evidence_anchors，发布后 KnowledgeEntry.source_evidence_anchor=None，违反设计 §11.6 与 FR-302b",
    "[important][LLM-FIXABLE][CR2/CR3] CLI garage memory review accept 路径不暴露 coexist/supersede/abandon 三选一，违反 FR-304 与设计 §9.4",
    "[minor][LLM-FIXABLE][CR4/CA5] SessionManager.update_session 有重复且不可达的 context_metadata 分支",
    "[minor][LLM-FIXABLE][CR2/CR4] KnowledgePublisher 用 candidate_id 直接当 KnowledgeEntry.id，重复 accept 会静默覆盖前一次发布",
    "[minor][LLM-FIXABLE][CR3] _trigger_memory_extraction 失败只走 logger.warning，没有把错误摘要回写到 batch/session 工件，FR-307 第 2/3 条在文件层失证"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "CR1",
      "summary": "Publisher 在 orchestrator 产出的 experience_summary 候选上抛 KeyError: 'task_type'"
    },
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "CR2",
      "summary": "自动提取候选缺 source_evidence_anchors，破坏设计 §11.6 不变量"
    },
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "CR2",
      "summary": "CLI accept 路径不向用户暴露 coexist/supersede/abandon 三选一，违反 FR-304"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "CR4",
      "summary": "SessionManager.update_session 第二个 context_metadata 分支不可达，dead code"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "CR2",
      "summary": "Publisher 用 candidate_id 当 KnowledgeEntry.id，重复 accept 静默覆盖历史发布"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "CR3",
      "summary": "_trigger_memory_extraction 失败只 logger.warning，缺工件级错误摘要"
    }
  ]
}
```
