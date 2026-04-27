# Regression Gate — F016 r1 (Memory Activation)

- **日期**: 2026-04-27
- **审阅人**: Cursor Agent (auto-streamlined per F011-F015 mode)

## Verdict: PASS

## 测试基线

| 阶段 | passed | 增量 |
|---|---|---|
| F015 finalize 后 (cursor/f015-agent-compose-bf33) | 1103 | baseline |
| F016 T1 (templates + types) | 1113 | +10 |
| F016 T2 (ingest 3 paths + dedup) | 1131 | +18 |
| F016 T3 (CLI memory + init prompt + status) | 1145 | +14 |
| F016 T4 (sentinel + AGENTS / RELEASE_NOTES + smoke) | **1151** | +6 |

**总增量: +48 测试; 0 regression**

## Sentinel 测试

```
$ pytest tests/sync/test_baseline_no_regression.py -v
PASSED [100%]  (1 passed in 89.45s)
```

## ruff baseline

- F015 完成时: 0 increment from F012 478 baseline
- F016 T4 完成时: **0 increment**

## 依赖变更

```
$ git diff main..HEAD -- pyproject.toml uv.lock
(empty)
```

**CON-1602 守门: 0 字节依赖变更.**

## INV / CON sentinels

```
$ pytest tests/memory_activation/test_init_yes_does_not_enable_memory.py -v   # Cr-1 r2 critical
PASSED

$ pytest tests/memory_activation/test_no_pipeline_changes.py -v                # CON-1601 + INV-F16-1
PASSED (3 tests)

$ pytest tests/adapter/installer/test_dogfood_layout.py::TestDogfoodLayout -v  # F015 + F016 module sentinels
PASSED (10 tests)
```

## 文件清单

### 新增 (3 src + 7 test + 3 templates + 6 docs)
- `src/garage_os/memory_activation/{__init__,types,templates,ingest}.py` (4 文件)
- `tests/memory_activation/{__init__,test_templates,test_ingest,test_cli,test_no_pipeline_changes,test_init_yes_does_not_enable_memory}.py` (6 文件)
- `packs/garage/templates/style-templates/{python,typescript,markdown}.md`
- `docs/manual-smoke/F016-walkthrough.md`
- 6 个 review/approval/spec/design/tasks 文档

### 修改 (1 src + 2 test + 2 docs)
- `src/garage_os/cli.py` (+180 LOC; memory subparser + init prompt + status 集成 + 5 handler)
- `tests/test_documentation.py` (+18 LOC; F016 sentinel)
- `tests/adapter/installer/test_dogfood_layout.py` (+10 LOC; F016 module sentinel)
- `AGENTS.md` (+90 LOC; Memory Activation (F016) section)
- `RELEASE_NOTES.md` (+85 LOC; F016 cycle entry)

## Manual Smoke Walkthrough

`docs/manual-smoke/F016-walkthrough.md` — 4 tracks 全绿:
- Track 1: `garage init --no-memory` + status 显 disabled (Im-1 r2 跨 No data)
- Track 2: `garage memory enable` + status 显 enabled
- Track 3: `garage memory ingest --from-reviews` → 2 ExperienceRecord
- Track 4: `garage memory ingest --style-template python` → 7 KnowledgeEntry STYLE

## 通过条件

✅ regression gate PASS, 进入 completion gate.
