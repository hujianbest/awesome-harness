# Traceability Review — F006 Garage Recall & Knowledge Graph

- 评审范围: F006 完整证据链 spec → design → tasks → impl → test/verification → status
- 上游评审: `docs/reviews/code-review-F006-recall-and-knowledge-graph.md`（verdict `通过`）
- Reviewer: `hf-traceability-review` subagent
- Workflow: profile=`standard`, mode=`auto`, isolation=`in-place`, branch=`cursor/f006-recommend-and-link-177b`
- Date: 2026-04-19

---

## 评审范围

- **topic / 任务**: F006 — Garage Recall & Knowledge Graph（`garage recommend` / `garage knowledge link` / `garage knowledge graph` 三个 CLI 子命令）
- **相关需求 (spec)**: `docs/features/F006-garage-recall-and-knowledge-graph.md`（已批准 r2，359 行）
  - FR-601～608、NFR-601～605、CON-601～606、ADR/OQ-601～607、ASM-601～605
- **相关设计**: `docs/designs/2026-04-19-garage-recall-and-knowledge-graph-design.md`（已批准 r1，433 行）
  - §3 需求覆盖与追溯表 / §6-§8 ADR-601~603 / §9 CLI surface / §10 数据流 / §13 测试策略
- **相关任务**: `docs/tasks/2026-04-19-garage-recall-and-knowledge-graph-tasks.md`（已批准，T1-T5）
- **相关实现**:
  - `src/garage_os/cli.py` 行 64-84（F006 模块顶层常量段）
  - `src/garage_os/cli.py` 行 1007-1283（F006 helper / handler 段）
  - `src/garage_os/cli.py` 行 1324-1495（`build_parser` F006 sub-parsers）
  - `src/garage_os/cli.py` 行 1644-1701（`main` dispatch）
  - `src/garage_os/memory/recommendation_service.py` 行 44-84（`build_from_query`，唯一新增方法）
  - `docs/guides/garage-os-user-guide.md` 行 409-489
  - `README.md` 行 49 / `README.zh-CN.md` 行 49
- **相关测试 / 验证**:
  - `tests/test_cli.py` 行 2117-2941（F006 段：`TestResolveKnowledgeEntryUnique` / `TestRecommendExperienceHelper` / `TestRecommend` / `TestKnowledgeLink` / `TestKnowledgeGraph` / `TestRecallAndGraphCrossCutting`）
  - `tests/test_documentation.py` 行 109-140（F006 doc grep）
  - 全 suite GREEN 证据：本会话 `python -m pytest tests/ -q` → `496 passed in 25.88s`

---

## Precheck

| 项 | 结果 |
|----|------|
| 上游 spec/design/tasks 审批记录可定位且通过 | ✅ `F006-spec-approval.md` (round-2 通过) / `F006-design-approval.md` (r1 通过 + 3 minor 已 inline 收敛) / `F006-tasks-approval.md` (5 minor LLM-FIXABLE 留 dev 阶段吸收) |
| 上游 review 链完整 | ✅ spec-review (r1 + r2) → design-review → tasks-review → test-review → code-review 五层全在 `docs/reviews/`，verdict 终态均为 `通过` |
| 实现交接块稳定可定位 | ✅ helper / handler 集中在 `cli.py` 单文件区段（行 1007-1283），`build_from_query` 集中在 `recommendation_service.py` 单方法 |
| route / stage / profile 一致 | ✅ `task-progress.md` 仍标 `Current Stage: hf-test-driven-dev` 但实际链路已推进到 code-review；这是 task-progress 状态机回写延迟（不影响追溯链本身一致性，见 §"需要回写或同步的工件"） |
| 全 suite GREEN 新鲜证据 | ✅ 当次会话 `496 passed in 25.88s`（baseline 451 + F006 新增 45） |
| AGENTS.md 编码约定 | ✅ 模块路径、Python 3.11+、`tmp_path` 隔离、不引入新依赖（NFR-602 已 byte-level 验证） |

Precheck 通过，进入正式审查。

---

## 多维评分（每维 0-10）

| ID | 维度 | 分 | 关键依据 |
|---|---|---|---|
| `TZ1` 规格 → 设计追溯 | 10 | design §3 表把 FR-601~608 / NFR-601~605 / CON-601~606 / ADR-601~603 1:1 映射到落点；ADR-601 显式承接 spec CON-601 "recommend 顶级是有意偏离"；ADR-602 显式承接 CON-605；ADR-603 承接 OQ-603 + FR-605。无规格条目"漂为孤儿"。 |
| `TZ2` 设计 → 任务追溯 | 10 | tasks §4 trace 表覆盖全部设计章节（§3 / §10 / §13.2 用例 1-26）；T1-T5 各 task 都标注 spec 锚点 + 设计锚点；T2/T3/T4 → T1 依赖与 design §14 完全一致。无设计决策"任务空洞"。 |
| `TZ3` 任务 → 实现追溯 | 9 | T1/T2/T3/T4/T5 全部产物存在且行号清晰；触碰文件与 tasks §3.1/3.2/3.3 完全一致（仅 `cli.py` + `recommendation_service.py` + 文档 + 测试）；T4 任务计划提到的 `KNOWLEDGE_GRAPH_NODE_FMT` 节点头常量在 follow-up commit `49064f4` 中补齐落地（行 84），任务计划与最终实现 1:1。 |
| `TZ4` 实现 → 验证追溯 | 9 | 设计 §13.2 用例 1-26 全部至少 1 条 testcase 命中（test-review 已建覆盖矩阵）；test-review 3 条 minor LLM-FIXABLE（`Source:` 行、`skill_name_only` fallback、CON-605 spot-check）已在 commit `82d91fc` 显式吸收；code-review 3 条 minor 中 CR-1 / CR-2 已在 commit `49064f4` 吸收（节点头常量化 + helper 类型签名）；CR-3 在 spec 措辞歧义内可接受。 |
| `TZ5` 漂移与回写义务 | 8 | 1 处需回写：`task-progress.md` 仍标 stage = `hf-test-driven-dev` / Active Task = T1，与实际推进到 code-review 通过的状态不一致——属 status 工件回写义务，不影响 spec→design→tasks→impl 主链一致性，但需要在进入 regression-gate 前由 `hf-finalize` / `hf-regression-gate` 同步。无 undocumented behavior、无 orphan code。 |
| `TZ6` 整体链路闭合 | 9 | spec→design→tasks→impl→test/verification 链路在所有 8 条 FR + 5 条 NFR + 6 条 CON + 3 条 ADR 上闭合；批准记录覆盖 spec / design / tasks 三个正式 gate；test-review + code-review 两个 review gate 通过；唯一未闭合环节 = task-progress 状态回写（已在 §"需要回写或同步的工件" 列出，下游 regression-gate 自然吸收）。 |

无任一关键维度 < 6/10。综合通过线已满足。

---

## 链接矩阵

### A. Spec → Design 追溯

| Spec 锚点 | Design 锚点 | 评 |
|---|---|---|
| FR-601 recommend knowledge 半边 | §3 行 67 / §10.1 序列图 / §6 ADR-601 / §9.2 参数表 | ✅ |
| FR-602 recommend experience 半边（CLI-internal scorer） | §3 行 68 / §7 ADR-602 / §10.1 序列图 | ✅ |
| FR-603 recommend 零结果归口 | §3 行 69 / §10.1 alt-empty 分支 | ✅ |
| FR-604 link 写入 + version+=1 | §3 行 70 / §10.2 序列图 / §9.3 参数表 | ✅ |
| FR-605 多 type 命中显式拒绝 | §3 行 71 / §8 ADR-603 / §10.2 alt-types_hit>1 | ✅ |
| FR-606 graph 节点 + 出边 + 入边 | §3 行 72 / §10.3 序列图 / §9.4 参数表 | ✅ |
| FR-607 cli:knowledge-link 命名空间 | §3 行 73 / §9.5 常量表 | ✅ |
| FR-608 help 自描述 + F005 8 sub | §3 行 74 / §9.1 子命令树 | ✅ |
| NFR-601~605 | §3 行 75-79 / §11 NFR mapping 表 | ✅ |
| CON-601 (recommend 顶级偏离) | §3 行 80 / ADR-601 候选拒绝栏 | ✅ |
| CON-602 (不改既有公开 API) | §3 行 81 / §2.4 设计目标 | ✅ |
| CON-603 (`version+=1` 保持) | §3 行 82 / §10.2 序列图 update 节点 | ✅ |
| CON-604 (cli: 命名空间不冲突) | §3 行 83 / §9.5 常量表 | ✅ |
| CON-605 (不动 recommend 算法) | §3 行 84 / §7 ADR-602 决策栏 | ✅ |
| CON-606 (recommend / graph read-only) | §3 行 85 / §10.1 / §10.3 数据流（无 update / store / delete） | ✅ |

### B. Design → Tasks 追溯

| Design 锚点 | Tasks 锚点 | 评 |
|---|---|---|
| §3 / §10.1 recommend 数据流 | T2 (handler + sub-parser + `build_from_query`) | ✅ |
| §3 / §10.2 link 数据流 | T3 (handler + sub-parser) | ✅ |
| §3 / §10.3 graph 数据流 | T4 (handler + sub-parser) | ✅ |
| ADR-601 recommend 顶级 | T2 acceptance 行 130 顶级 sub-parser | ✅ |
| ADR-602 experience scorer 独立函数 | T1 (`_recommend_experience` helper) | ✅ |
| ADR-603 多 type 命中显式拒绝 | T1 (resolver) + T3/T4 (handler 报错) | ✅ |
| §9.5 常量集 | T2/T3/T4 各引入对应 FMT 常量 + T5 grep 断言 | ✅ |
| §13.2 用例 1-26 | T1-T5 全覆盖（tasks §4 trace 表显式列出） | ✅ |
| §14 task readiness 提示 (T1-T5 拆分 + 依赖) | tasks §5 一一对应；§6 queue projection + selection priority | ✅ |

### C. Tasks → Impl 追溯

| Task | 实现产物 | 评 |
|---|---|---|
| T1 `_resolve_knowledge_entry_unique` + `_recommend_experience` | `cli.py:1013-1038` + `cli.py:1041-1121` | ✅ |
| T2 `_recommend` handler + sub-parser + `build_from_query` | `cli.py:1139-1177` + `cli.py:1324-1353` + `recommendation_service.py:44-84` | ✅ |
| T3 `_knowledge_link` handler + sub-parser + 4 个常量 | `cli.py:1180-1227` + `cli.py:1460-1483` + 行 67 / 75-77 常量 | ✅ |
| T4 `_knowledge_graph` handler + sub-parser + 段标题常量 | `cli.py:1230-1283` + `cli.py:1485-1495` + 行 81-84 常量 | ✅ |
| T5 文档同步 + cross-cutting | `docs/guides/garage-os-user-guide.md:409-489` + `README.md:49` + `README.zh-CN.md:49` + `tests/test_documentation.py:109-140` + `tests/test_cli.py:2800-2941` | ✅ |

### D. Impl → Test / Verification 追溯

| 实现路径 | 测试覆盖 | 评 |
|---|---|---|
| `_resolve_knowledge_entry_unique` (`cli.py:1013-1038`) | `TestResolveKnowledgeEntryUnique` 3 testcases (`tests/test_cli.py:2165-2202`) | ✅ |
| `_recommend_experience` (`cli.py:1041-1121`) | `TestRecommendExperienceHelper` 8+ testcases (`tests/test_cli.py:2204-2319`) | ✅ |
| `_recommend` (`cli.py:1139-1177`) | `TestRecommend` happy/zero/no-garage/top/tag/domain（设计 §13.2 用例 1-7） + `Source:` 行（OQ-607, `cli.py:2846-2890`） + `skill_name_only` fallback（`cli.py:2892-2915`）| ✅ |
| `build_from_query` (`recommendation_service.py:44-84`) | `TestRecommend` 内 builder unit test（设计 §13.2 用例 4 + tasks T2 acceptance 行 139） + CON-605 byte-level spot check（`cli.py:2917-2941`） | ✅ |
| `_knowledge_link` (`cli.py:1180-1227`) | `TestKnowledgeLink` 7 testcases (`tests/test_cli.py:2513-2713`)，含 happy / 重复（`version==3`）/ related-task / missing / 外部 ID / ambiguous / publisher 元数据保护 | ✅ |
| `_knowledge_graph` (`cli.py:1230-1283`) | `TestKnowledgeGraph` 4 testcases (`tests/test_cli.py:2715-2798`)，含 happy / 孤立节点 / not-found / ambiguous | ✅ |
| `build_parser` F006 sub-parsers (`cli.py:1324-1495`) | `TestRecallAndGraphCrossCutting` help 5 用例（`recommend --help` / `link --help` / `graph --help` / `garage --help` / `garage knowledge --help` 量化 8 sub）+ source-marker `cli:` 前缀断言 + smoke < 1.5s | ✅ |
| 文档 (`user-guide` + 双 README) | `tests/test_documentation.py:113-140` 7 token grep + 双 README 3 token grep | ✅ |

### E. 审批记录覆盖

| Gate | 审批记录 | 状态 |
|---|---|---|
| Spec | `docs/approvals/F006-spec-approval.md` | ✅ Approved (auto-mode, round-2) |
| Design | `docs/approvals/F006-design-approval.md` | ✅ Approved (auto-mode, r1, 3 minor inline) |
| Tasks | `docs/approvals/F006-tasks-approval.md` | ✅ Approved (auto-mode, 5 minor → dev 吸收) |
| Test review | `docs/reviews/test-review-F006-recall-and-knowledge-graph.md` | ✅ 通过 (3 minor 已 commit `82d91fc` 吸收) |
| Code review | `docs/reviews/code-review-F006-recall-and-knowledge-graph.md` | ✅ 通过 (3 minor 中 CR-1/CR-2 已 commit `49064f4` 吸收) |

---

## 关键不变量端到端可验证

### Inv-1 — Source-marker `cli:knowledge-link` 命名空间

- **Spec 锚**: FR-607 + CON-604（`cli.py` 模块常量 + 强制覆写 + 与 publisher 路径可分）
- **Design 锚**: §3 行 73 + §9.5 行 241 (`CLI_SOURCE_KNOWLEDGE_LINK = "cli:knowledge-link"`)
- **Tasks 锚**: T3 行 153 (常量) + T5 行 203 (cross-cutting `cli:` 前缀断言)
- **Impl 锚**: `cli.py:67` 常量定义 + `cli.py:1217-1220` 强制覆写（含 already-linked 路径）
- **Test 锚**: `test_link_happy_appends_and_bumps_version`（happy 路径 source_artifact 断言） + `test_link_repeated_is_idempotent_in_field`（重复 link 路径仍覆写） + `test_link_does_not_pollute_publisher_metadata`（publisher 元数据保留 + source_artifact 覆盖） + `test_link_source_marker_uses_cli_namespace`（cross-cutting `cli:` 前缀）
- **结论**: 4 条测试覆盖三种 input shape × 两种输出维度，端到端追溯完整。

### Inv-2 — `KnowledgeStore.update()` `version+=1` 不变量延伸到 link 路径

- **Spec 锚**: CON-603 + FR-604 验收 (`version=2` happy / `version=3` 重复)
- **Design 锚**: §3 CON-603 + §10.2 序列图 update 节点 + §12 失败模式表
- **Tasks 锚**: T3 行 156-157 acceptance（`version == 2` / 重复 `version == 3`）
- **Impl 锚**: `cli.py:1221` `knowledge_store.update(entry)`（无论 already_linked 都走 update）+ `knowledge_store.py:194` `entry.version += 1`
- **Test 锚**: `test_link_happy_appends_and_bumps_version` 断言 `version == 2`；`test_link_repeated_is_idempotent_in_field` 断言重复 link 后 `version == 3`
- **结论**: F004 v1.1 不变量在 link 路径双重锁定（happy + 重复）。

### Inv-3 — Mixed knowledge + experience recall（FR-601 + FR-602）

- **Spec 锚**: FR-601 step 4 + FR-602 step 4（合并到同一 list）+ FR-603（合并后零结果归口）
- **Design 锚**: §3 行 67-69 + §10.1 序列图 H 节点合并 / sort by score / take top N + §4 "Composable Recall Pattern"
- **Tasks 锚**: T2 acceptance 行 132（`recommend 同时命中 knowledge + experience，按 score 降序排列`）
- **Impl 锚**: `cli.py:1166-1167` `merged = list(knowledge_results) + list(experience_results); merged.sort(key=lambda item: item["score"], reverse=True)` + `cli.py:1168-1169` top-N 截断
- **Test 锚**: `TestRecommend::test_recommend_mixed_sorted_by_score`（断言两 label 共存 + 按 score 排序）+ `test_recommend_zero_results_with_entries_but_no_match`（5+5 entry 不命中走 FR-603 出口）
- **结论**: spec 两条互补 FR 的合并语义在 design 层、task 层、impl 层、test 层都可机器追溯。

### Inv-4 — CON-605 byte-level（不修改 `RecommendationService.recommend`）

- **Spec 锚**: CON-605 + ADR-602 决策栏
- **Design 锚**: §3 CON-605 + §5 候选 B 拒绝理由 + §11 NFR-602 验证方式
- **Impl 锚**: `git diff origin/main..HEAD -- src/garage_os/memory/recommendation_service.py` 仅显示 +42 行新增 `build_from_query`，`recommend()` / `build()` 字节未动
- **Test 锚**: `test_recommendation_service_recommend_byte_level_unchanged`（断言 `recommend(self, context)` 签名未变 + 5 个 score / fallback 关键 token 全部存在于源码）
- **结论**: byte-level 与 semantic-level 双重护栏；F003 `garage run` 推荐路径行为零变化。

### Inv-5 — `recommend` / `graph` read-only（CON-606）

- **Spec 锚**: CON-606
- **Design 锚**: §3 CON-606 + §10.1 / §10.3 数据流（无 update / store / delete 节点）
- **Impl 锚**: `_recommend` (`cli.py:1139-1177`) 与 `_knowledge_graph` (`cli.py:1230-1283`) 全程仅调 `retrieve` / `list_entries` / `list_records`
- **Test 锚**: `TestRecommend` 全部用例 + `TestKnowledgeGraph` 全部用例的 GREEN（间接）+ NFR-601 全 suite 回归（直接）
- **结论**: read-only 边界在代码层硬约束 + 测试 GREEN 保护。

---

## 发现项

- [minor][LLM-FIXABLE][TZ5] **F006-TR-1 — `task-progress.md` 状态未回写到 code-review 通过态**
  - 位置：`task-progress.md:20` `Current Stage: hf-test-driven-dev` / 行 24 `Current Active Task: T1`
  - 现状：实际链路已推进到 code-review 通过（commit `49064f4`），并准备进入 traceability-review。task-progress 仍停留在 dev 起点。
  - 影响：不影响 spec→design→tasks→impl→test 主链一致性，也不影响 reviewer 冷读路由（本评审已用 commit log + review 文件作为唯一信号源）；但破坏了 status 工件作为 router 兜底信号的准确性。
  - 建议：在 regression-gate / completion-gate 阶段由对应 skill 显式写回 `Current Stage: hf-traceability-review` (或后续) + `Current Active Task: (cycle complete)`，归 `hf-finalize` 责任范围（不阻塞本评审通过）。

- [minor][LLM-FIXABLE][TZ4] **F006-TR-2 — code-review F006-CR-3（experience scorer tech/pattern/lesson 多次累加）尚未在测试层固化判断**
  - 位置：`cli.py:1080-1102` `_recommend_experience` tech / pattern / lesson-text 块均无外层 `break`，与 task_type 块单次累加规则不一致
  - 现状：code-review 已显式定级 minor 且备注 spec 措辞歧义"严格意义上不算 bug"，可不修；但当前测试既未断言"多次累加"也未断言"单次累加"，未来若 spec 后续 cycle 显式选边，测试无法立刻指明回归方向。
  - 影响：不影响 F006 当前追溯链一致性（spec / design / tasks / impl / test 在当前歧义口径下都可解释为合理）；属于"语义可演化但当前测试未对该选择做记号"的轻量缺口。
  - 建议：在下一 cycle spec 增量裁决多次 vs 单次累加后，补 1 条断言；本 cycle 可不动。

- [minor][LLM-FIXABLE][TZ5] **F006-TR-3 — 节点头常量在 commit `49064f4` 后落地，但 `__all__` / 公共 import 表未同步声明**
  - 位置：`cli.py:84` 新增 `KNOWLEDGE_GRAPH_NODE_FMT`；`tests/test_cli.py:2120-2131` F006 import 块未导入此常量
  - 现状：code-review CR-1 通过补常量化解决，但测试层未用 `KNOWLEDGE_GRAPH_NODE_FMT.format(...)` 断言节点头（`tests/test_cli.py` 中相关 graph 测试仍以 `assert "[DECISION]" in out` 子串方式断言），常量名与测试断言之间未直接绑定。
  - 影响：未来若节点头格式调整（例如多语种），常量更名后测试仍以子串通过，无法立刻捕获不一致；属轻微"常量化承诺与测试断言绑定不严"。
  - 建议：在 hf-test-driven-dev 后续轻量轮次，把至少 1 条 graph happy 用例的断言改为 `KNOWLEDGE_GRAPH_NODE_FMT.format(type="DECISION", topic=...) in out`。不阻塞当前评审。

---

## 追溯缺口

- 无 critical / important 追溯断链
- 3 条 minor 缺口均不阻塞链路闭合（详见上节）

---

## 需要回写或同步的工件

- 工件: `task-progress.md`
  - 原因: status 工件未跟随 review 链推进；当前仍标 `Current Stage: hf-test-driven-dev`，与实际推进到 traceability-review 不一致
  - 建议动作: 在 regression-gate 通过后由 `hf-finalize` / `hf-completion-gate` 同步：`Current Stage` → 后续 stage、`Pending Reviews And Gates` 列表移除已通过项、`Current Active Task` 标 cycle 完成
- 无其他工件回写需求；F006 cycle 内的所有 spec/design/tasks/review/approval 工件均最新且互相一致

---

## 整体证据链闭合性陈述

F006 的 8 条 FR + 5 条 NFR + 6 条 CON + 3 条 ADR + 7 条 OQ 全部可通过 spec → design → tasks → impl → test 5 层逐级正向 / 反向追溯。

**正向追溯（spec → impl）样本**：FR-607 `cli:knowledge-link` → design §3 行 73 + §9.5 → tasks T3 行 153 + T5 行 203 → `cli.py:67` (常量定义) + `cli.py:1220` (覆写) → 4 条测试（含 cross-cutting `cli:` 前缀）。

**反向追溯（impl → spec）样本**：`cli.py:1080-1094` 的 experience tech / pattern / lesson-text 评分逻辑 → `cli.py:1041-1056` docstring 标 `(see F006 §6 FR-602)` → spec FR-602 6 条规则 → 设计 §3 行 68 + ADR-602 → 任务 T1 行 109-111 acceptance。

无任何"代码引入未记录的新行为"（ZA3 anti-pattern 未触发）；无"任务无法追溯到规格或设计"（ZA2 未触发）；无"规格已变更但设计/任务仍基于旧版本"（ZA1 未触发，本 cycle spec 自 r2 起未再变更）；测试新鲜 GREEN（ZA4 unsupported completion claim 未触发）。

---

## 结论

**通过**

理由：

1. 6 个评审维度全部 ≥ 8/10，TZ1/TZ2 满分，无任一维度低于通过线 6/10。
2. spec→design→tasks→impl→test/verification 链路在所有规格条目上均闭合，附 link matrix 5 张表证明。
3. 5 条关键不变量（cli:knowledge-link 命名空间 / version+=1 延伸 / mixed recall / CON-605 byte-equal / read-only 边界）端到端可机器追溯。
4. 审批记录覆盖全部 spec / design / tasks 三个正式 gate；test / code 两个 review gate 通过且历史 minor 已 commit 吸收。
5. 全 suite GREEN 新鲜证据（`496 passed in 25.88s`）支撑当前实现的完成性主张，零回归。
6. 3 条 finding 全部 minor LLM-FIXABLE：F006-TR-1 是 status 回写义务（regression-gate / finalize 自然处理），F006-TR-2 / F006-TR-3 是测试断言强度的轻量补强（可在后续 cycle 顺手吸收），均不阻塞链路完整性。

---

## 下一步

- `hf-regression-gate`

---

## 记录位置

- 本评审记录: `docs/reviews/traceability-review-F006-recall-and-knowledge-graph.md`
