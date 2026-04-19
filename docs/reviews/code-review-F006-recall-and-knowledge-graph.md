# Code Review — F006 Garage Recall & Knowledge Graph

- 评审对象（实现交接块）:
  - `src/garage_os/cli.py` 行 64-83（F006 模块顶层常量段，含 `CLI_SOURCE_KNOWLEDGE_LINK` / `RECOMMEND_NO_RESULTS_FMT` / `KNOWLEDGE_LINKED_FMT` / `KNOWLEDGE_LINK_ALREADY_FMT` / `ERR_LINK_FROM_AMBIGUOUS_FMT` / `GRAPH_OUTGOING_HEADER` / `GRAPH_INCOMING_HEADER` / `GRAPH_EDGE_NONE`）
  - `src/garage_os/cli.py` 行 1007-1282（F006 handler / helper 段：`_resolve_knowledge_entry_unique`、`_recommend_experience`、`_print_recommendation_block`、`_recommend`、`_knowledge_link`、`_knowledge_graph`）
  - `src/garage_os/cli.py` `build_parser()` 行 1323-1494（新增 `recommend` 顶级 + `knowledge link` / `knowledge graph` 二级 sub-parsers）+ `main()` 行 1641-1700（dispatch）
  - `src/garage_os/memory/recommendation_service.py` 行 44-84（`RecommendationContextBuilder.build_from_query`，唯一新增方法）
  - 文档同步: `docs/guides/garage-os-user-guide.md` 行 409-489、`README.md` 行 49、`README.zh-CN.md` 行 49
- 上游规格: `docs/features/F006-garage-recall-and-knowledge-graph.md`（已批准 r1）
- 上游设计: `docs/designs/2026-04-19-garage-recall-and-knowledge-graph-design.md`（已批准 r1）
- 上游 tasks: `docs/tasks/2026-04-19-garage-recall-and-knowledge-graph-tasks.md`（已批准）
- 上游 test review: `docs/reviews/test-review-F006-recall-and-knowledge-graph.md`（通过；3 minor LLM-FIXABLE 已在 commit `82d91fc` 吸收 → 当前 496 passed）
- Workflow: profile=`standard`, mode=`auto`, branch=`cursor/f006-recommend-and-link-177b`
- Reviewer: `hf-code-review` subagent
- Date: 2026-04-19

---

## Precheck

| 项 | 结果 |
|----|------|
| 实现交接块稳定可定位 | ✅ helper / handler / 常量集中在 `cli.py` 行号锚点稳定；`build_from_query` 集中在 `recommendation_service.py` 单方法 |
| 测试通过证据新鲜 | ✅ 当次会话 `python -m pytest tests/ -q` `496 passed in 25.97s`（F005 baseline 451 + F006 新增 45） |
| route / stage / profile 一致 | ✅ test-review 通过 + auto-mode approval；task-progress 显示 implementation 完成 |
| AGENTS.md 编码约定 | ✅ 模块路径、Python 3.11+、不引入新依赖、文件即契约 |

Precheck 通过，进入正式审查。

---

## 多维评分（每维 0-10）

| ID | 维度 | 分 | 关键依据 |
|---|---|---|---|
| `CR1` 正确性 | 9 | FR-601~608 行为与设计 §10.1/10.2/10.3 数据流逐条对应；`_resolve_knowledge_entry_unique` 顺序遵守 `KnowledgeType` 枚举（设计承诺）；`_knowledge_link` 去重用 `if dst not in target_field` 保序而非 `set()`（T3 风险点）；`_knowledge_graph` 入边扫描以 `other.id != entry.id` 过滤自引用并按 `list_entries()` 自然序输出（T4 risk note "ordering 稳定"） |
| `CR2` 设计一致性 | 8 | ADR-601（`recommend` 顶级）/ ADR-602（experience scorer 在 cli.py 独立函数）/ ADR-603（多 type 命中显式拒绝 + 共用 `ERR_LINK_FROM_AMBIGUOUS_FMT`）全部如设计落地；CON-602 / CON-603 / CON-605 / CON-606 严格遵守。1 处轻微偏离：T4 任务计划提到的 `KNOWLEDGE_GRAPH_NODE_FMT` 节点头常量未实现，节点头改用 inline f-string（详见 finding F006-CR-1） |
| `CR3` 状态 / 错误 / 安全 | 9 | 错误路径完备：`--from`/`--id` not-found → exit 1 + `KNOWLEDGE_NOT_FOUND_FMT`；ambiguous → exit 1 + `ERR_LINK_FROM_AMBIGUOUS_FMT`；`ERR_NO_GARAGE` 兜底（与 F005 一致）；`assert entry is not None` 守护 `len(types_hit)==1` 后的代码路径；`KnowledgeStore.list_entries()` 损坏文件已由 store 层 try/except 兜底，graph handler 不重复发明（设计 §12 显式声明） |
| `CR4` 可读性 / 可维护性 | 9 | 命名清晰（`_resolve_knowledge_entry_unique` / `_recommend_experience` / `_print_recommendation_block` 单一职责）；helper-vs-handler 边界明确；3 个 helper 与 3 个 handler 各自不超过 ~70 行；`_print_recommendation_block` 拆出避免在 handler 内嵌打印逻辑；docstring 在被测试导入的 helper（`_resolve_knowledge_entry_unique` / `_recommend_experience`）上完整解释 contract（含返回元组语义、score 权重来源） |
| `CR5` 范围守卫 | 10 | 无超范围实现：handler 严格围绕 FR-601~608；未引入 `unlink` / 多跳遍历 / experience link / 跨类型 link / JSON 输出 等 spec § 5 deferred 项；未对 `RecommendationService.recommend()` 做任何修改（`git diff` 显示 `recommendation_service.py` 唯一变化是新增 `build_from_query`，CON-605 字节级满足）；NFR-602 `pyproject.toml` `git diff` 空 |
| `CR6` 下游追溯就绪度 | 9 | 实现交接块行号清晰；常量名与 spec / design § 9.5 1:1；测试覆盖 § 13.2 用例 1-26 全清；下游 `hf-traceability-review` 可直接 1:1 把 FR / NFR / CON / ADR 对到 cli.py 行号 |

无任一关键维度 < 6。综合通过线已满足。

---

## 实施 vs 关键约束逐项核对

| 约束 / ADR | 期望 | 现况 | 评 |
|------------|------|------|---|
| **CON-602** 不改既有公开 API | 仅在 `RecommendationContextBuilder` 上 non-breaking 加方法 | `git diff origin/main..HEAD -- recommendation_service.py` 唯一变化是新增 `build_from_query`；`build()` 与 `recommend()` 字节未动 | ✅ |
| **CON-603** `version+=1` 保持 | `link` 路径调 `KnowledgeStore.update()` | 实现行 1220 `knowledge_store.update(entry)`；测试 `test_link_happy_appends_and_bumps_version` 断言 `version == 2`、重复 link `version == 3` | ✅ |
| **CON-605** `RecommendationService.recommend` byte-equal | 不动 `recommend()` 的 ranking / score / reasons | 同 CON-602 git diff 证据；本会话 commit `82d91fc` 显式补了 byte-level spot-check | ✅ |
| **CON-606** `recommend` / `graph` read-only | handler 仅调 `retrieve` / `list_entries` / `list_records` | `_recommend` 行 1152-1163 / `_knowledge_graph` 行 1236-1281 全程无 `store` / `update` / `delete` 调用 | ✅ |
| **NFR-602** 零外部依赖 | 仅 stdlib + `garage_os.*` | `cli.py` import 闭包 = `argparse` / `hashlib` / `json` / `sys` / `time` / `datetime` / `pathlib` / `typing` + `garage_os.*`；`recommendation_service.py` import 闭包 = `dataclasses` / `typing` + `garage_os.*`；`pyproject.toml` `git diff` 空 | ✅ |
| **NFR-604** stdout 常量化 | 所有 success/failure 文案走顶层常量 | `grep "Linked '" cli.py` 仅命中常量定义行 75；`Already linked` / `No matching` / `is ambiguous` 同模式；`Outgoing edges:` / `Incoming edges:` / `(none)` 已常量化 | ✅ |
| **ADR-601** `recommend` 顶级 | 与 init/status/run/knowledge/experience/memory 并列 | `build_parser()` 行 1324 `subparsers.add_parser("recommend", ...)`；不挂在 knowledge / memory 子树 | ✅ |
| **ADR-602** experience scorer 独立 in cli.py | `_recommend_experience` 不进 RecommendationService | helper 居于 `cli.py:1040-1120`；零基类抽象 | ✅ |
| **ADR-603** 多 type 命中显式拒绝 | resolver 返回 types_hit；handler 报 `ERR_LINK_FROM_AMBIGUOUS_FMT` | `_resolve_knowledge_entry_unique` 行 1029-1037 收集所有命中 type；`_knowledge_link` 行 1199-1204 与 `_knowledge_graph` 行 1243-1248 均按 len > 1 报错 | ✅ |
| **FR-607** `cli:knowledge-link` 命名空间 | 强制覆写 `source_artifact` | 行 1219 `entry.source_artifact = CLI_SOURCE_KNOWLEDGE_LINK`；即使 `already_linked == True` 也会覆写（注释 1216-1218 显式说明 audit grep 语义） | ✅ |
| **FR-608** help 自描述 + F005 子命令保留 | 8 个 knowledge sub + recommend 顶级 | 既有 search / list / add / edit / show / delete 6 个保持原状；新增 link / graph 并列；error 文案行 1701-1705 同步更新到 8 sub 列表 | ✅ |

---

## 发现项

- [minor][LLM-FIXABLE][CR2 / CR4] **F006-CR-1 — `KNOWLEDGE_GRAPH_NODE_FMT` 节点头常量未抽出**
  - 位置：`src/garage_os/cli.py:1251-1252` 节点头使用 inline f-string `f"[{entry.type.value.upper()}] {entry.topic}"` + `f"ID: {entry.id}"`
  - 任务计划 T4（`docs/tasks/2026-04-19-garage-recall-and-knowledge-graph-tasks.md` 第 175 行）显式提到 "新增模块常量 `KNOWLEDGE_GRAPH_NODE_FMT`（节点头格式）+ 段标题字符串（`Outgoing edges:` / `Incoming edges:` / `(none)` 也走常量化）"。当前段标题三常量 `GRAPH_OUTGOING_HEADER` / `GRAPH_INCOMING_HEADER` / `GRAPH_EDGE_NONE` 已落，但节点头部两行未常量化。
  - 影响：spec NFR-604 验收门"`grep \"Linked '\" cli.py` 仅命中常量定义"是 success/failure 文案语义，节点头属"display structure"——严格读 spec NFR-604 不算违反；但任务计划字面承诺未兑现，未来若节点头格式需要变更，无法靠 grep 常量名一处改。
  - 建议：抽出 `KNOWLEDGE_GRAPH_NODE_HEADER_FMT = "[{type}] {topic}"` + `KNOWLEDGE_GRAPH_NODE_ID_FMT = "ID: {id}"`；属轻量补强，不阻塞当前 verdict。

- [minor][LLM-FIXABLE][CR4] **F006-CR-2 — `_recommend_experience` 函数签名类型偏弱**
  - 位置：`src/garage_os/cli.py:1040-1043` `def _recommend_experience(records: list, context: dict) -> list[dict]:`
  - 现状：`records` 缺 `list[ExperienceRecord]`、`context` 缺 `dict[str, Any]`、返回 `list[dict[str, Any]]`。同文件 `_resolve_knowledge_entry_unique` 已使用 `tuple[Optional[KnowledgeEntry], list[str]]` 精确签名，对比之下本 helper 的类型清晰度不一致。
  - 影响：此 helper 被测试 `from garage_os.cli import _recommend_experience` 直接 import 调用，作为半公开 contract 入口，类型清晰度对 IDE 自动补全 / future maintainer 阅读有价值。
  - 建议：补 `records: list[ExperienceRecord]`、`context: dict[str, Any]`、`-> list[dict[str, Any]]`；属轻量类型补强，不影响行为。
  - 注：cli.py baseline 整体存在 `Optional[X]` 样式 UP045 警告（与 F003/F004/F005 一致），按本次 review 预设不阻；本条仅针对**新增** helper 类型清晰度。

- [minor][LLM-FIXABLE][CR1] **F006-CR-3 — `_recommend_experience` tech / pattern 规则可对同一 record 重复加分**
  - 位置：`src/garage_os/cli.py:1080-1094`
  - 行为：`task_type` 规则在外层 `for token` 内含 `break`（同 record 至多一次 `task_type:` 命中），但 `tech` / `pattern` / `lesson-text` 规则**没有外层 break**——同一 record 若有多个 token 分别命中不同 tech / pattern / lesson 文本，会累加多次 0.6 / 0.4 + 多个 reason。
  - 例：tags=["sqlite", "indexing"]、record.tech_stack=["sqlite"]、record.key_patterns=["indexing"] → tech +0.6 + pattern +0.6（合理）；但 tags=["sqlite", "sqlite"]、record.tech_stack=["sqlite"] → tech +0.6 两次（虽然 CLI 不会构造重复 token，但是不变量上 fragile）。
  - 影响：FR-602 spec 文字 "任一 token 命中... 任一元素 → +0.6 + reason" 在 task_type 是单次累加，在 tech / pattern 是多次累加——spec 措辞本身就有歧义，本实现的"多次累加"读法可被接受为合理设计选择。**严格意义上不算 bug**；当前测试也未约束此细节。
  - 建议：若希望与 task_type 规则一致改为 "每 record 每规则至多一次"，可在 tech / pattern / lesson 块外层补一个找到首个 reason 后即 `break` 的开关；或在 spec 后续 cycle 显式选边。当前可不修。

---

## 代码风险与薄弱项

- **入边扫描在大库下的性能**：`_knowledge_graph` 行 1271-1279 的入边扫描是 O(N) 全库 list_entries() —— 设计 §12 / OQ-604 已显式声明 N≤100 时 < 1.5s，且本 cycle smoke test 实测通过。N 远大时需要反向索引（属下个 cycle 议题）。
- **`already_linked` 路径下仍调 `update()`**：行 1219-1220 即使无字段变化也走 `update()` → `version += 1`。这是 spec OQ-602 明确接受的"已知可接受行为"，但 git 历史会出现"无实质 diff 的 version bump"，未来 reviewer 看到 entry 反复 +1 时需要 audit grep `cli:knowledge-link` 才能区分 link 操作 vs 真实 edit；这个 audit 路径已被 FR-607 + commit comment 1216-1218 显式打通。
- **F006-CR-1 节点头常量缺失**：未来若调整 graph 节点头展示需手工搜索两处 inline f-string；对 hf-traceability-review 不构成阻塞，对 future change-set readability 有轻微负担。

---

## 下游追溯评审提示

下游 `hf-traceability-review` 可直接按以下 3 个 anchor 复核：

1. **FR-601~608 → cli.py / recommendation_service.py 行号映射**: 已在本 record "实施 vs 关键约束逐项核对" 表中给齐。
2. **CON-602 / CON-605 byte-equal 证据**: `git diff origin/main..HEAD -- src/garage_os/memory/recommendation_service.py` 仅显示 `build_from_query` 新增；`recommend()` / `build()` 字节未动。
3. **NFR-602 零依赖证据**: `git diff origin/main..HEAD -- pyproject.toml` 输出空。

无 spec / design / task → 实现的语义漂移；上述 3 条 minor 均不影响追溯链完整性。

---

## 结论

**通过**

理由：

1. 6 个评审维度均 ≥ 8/10，全部高于通过阈值 6。
2. FR-601~608 / NFR-601~605 / CON-602/603/605/606 / ADR-601/602/603 全部 1:1 落地到 `cli.py` + `recommendation_service.py`；行号 anchor 稳定。
3. 关键不变量（`version+=1` / `cli:knowledge-link` 命名空间 / 多 type 显式拒绝 / read-only 边界）在代码层与测试层双重锁定。
4. 全 suite 当次会话 `496 passed`，零回归；F005 baseline 451 不退绿。
5. `recommendation_service.py` 的 `recommend()` / `build()` 字节未变更，CON-605 / CON-602 byte-level 满足；`pyproject.toml` 零增量，NFR-602 满足。
6. 3 条 finding 全部 minor LLM-FIXABLE，可在后续轻量 PR 中吸收（节点头常量化 + helper 类型清晰度 + 可选规则去重一致性），均不阻塞追溯评审主线。

---

## 下一步

- `hf-traceability-review`

---

## 记录位置

- 本评审记录: `docs/reviews/code-review-F006-recall-and-knowledge-graph.md`
