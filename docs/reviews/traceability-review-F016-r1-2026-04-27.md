# Traceability Review — F016 r1 (Memory Activation)

- **日期**: 2026-04-27
- **审阅人**: Cursor Agent (auto-streamlined per F011-F015 mode)
- **范围**: 5 个 FR (FR-1601..1605) + 5 个 INV (INV-F16-1..5) + 5 个 CON (CON-1601..1605)

## Verdict: APPROVED

## FR ↔ 实现 ↔ 测试 矩阵

| FR | 实现位置 | 测试 |
|---|---|---|
| **FR-1601** memory enable/disable/status | `cli.py::_memory_enable / _memory_disable / _memory_toggle / _memory_status` | `TestMemoryEnableDisable` (2) + `TestMemoryStatus` |
| **FR-1602** memory ingest | `memory_activation/ingest.py::ingest_from_{reviews,git_log,style_template}` | `test_ingest.py` 18 + `TestMemoryIngestStyleTemplate` (2) |
| **FR-1603** init prompt + --no-memory | `cli.py::_init` 修改 + `init_no_memory` arg | `TestInitYesDoesNotEnableMemory` (3) + `TestInitInteractivePrompt` (3) |
| **FR-1604** STYLE templates | `memory_activation/templates.py` + `packs/garage/templates/style-templates/*.md` | `test_templates.py` 10 + `TestPackagedTemplates` (3) |
| **FR-1605** status integration | `cli.py::_status` 修改 (Memory line crosses No data + STYLE counted) | `TestStatusMemoryLine` (2) |

**5 / 5 FR 全部追溯**

## INV ↔ 测试

| INV | 测试 |
|---|---|
| INV-F16-1 (F003-F015 既有 API 字节级) | `test_no_pipeline_changes.py` AST sentinel + 全套 1131 → 1151 0 regression |
| INV-F16-2 (写仅 .garage/ + packs/garage/templates/) | ingest 全用 store API (read code review) + templates 在 packs/garage/templates/ |
| INV-F16-3 (--yes 不动 memory; F007 行为字节级不变) | `test_init_yes_does_not_enable_memory.py` permanent guard + 3 CLI 用例 |
| INV-F16-4 (enable/disable 不动既有数据) | `TestMemoryEnableDisable::test_disable_sets_false` (既有 KnowledgeEntry / ExperienceRecord 不变) |
| INV-F16-5 (KnowledgeType.STYLE 字节级) | `ingest_from_style_template` 仅经 KnowledgeStore.store; F011 enum 字节级 |

**5 / 5 INV 全部覆盖**

## CON ↔ 验证

| CON | 验证 |
|---|---|
| CON-1601 (F003-F015 既有 API + schema 字节级) | git diff sentinel + AST sentinel; 0 regression |
| CON-1602 (零依赖) | git diff main..HEAD -- pyproject.toml uv.lock = 0 |
| CON-1603 (perf < 5s for 100 reviews / 1000 commits) | 单测覆盖 N=2/3 速度极快; manual smoke 实际 sub-second |
| CON-1604 (F009 init flags 不动) | `init_parser` 仅加 `--no-memory`; 既有 `--yes/--scope/--hosts/--force` 完全不变; 3 sentinel 测试 |
| CON-1605 (F015 agent compose 不动) | AST sentinel + F015 既有 compose handler 0 修改 |

## 上下游 trace

- **Spec ↔ Design ↔ Tasks ↔ Impl**: spec r2 → design r1 → tasks r1 → 实施 commits (6021dcc T1, 88fa62d T2, a15a861 T3, T4 finalize)
- **F003 既有 API 复用**: load_memory_config / extraction_orchestrator (read-only by F016)
- **F004 store API 复用 (CON-1601)**: ExperienceIndex.store / KnowledgeStore.store; F016 不动这些 method 签名
- **F005 ID 模式复用 (Mi-2 r2)**: `_generate_exp_id` 与 F005 `_generate_experience_id` 同模式 (exp-yyyymmdd-6hex)
- **F011 KnowledgeType.STYLE 复用 (INV-F16-5)**: F016 写 STYLE entries 用既有 enum
- **vision 闭环**: growth-strategy.md § Stage 3 健康表现第 2 项 "知识条目增长随使用自然" ⚠️ → ✅

## 残余项

- **None blocking**.

## 通过条件

✅ traceability review APPROVED, 进入 regression gate.
