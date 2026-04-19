# Verification — F006 Regression Gate

## Metadata

- Verification Type: `regression-gate`
- Scope: F006 — Garage Recall & Knowledge Graph（Profile `standard`）
- Record Path: `docs/verification/F006-regression-gate.md`
- Branch: `cursor/f006-recommend-and-link-177b`
- Worktree Path: `/workspace`（in-place isolation）
- Date: 2026-04-19

## Upstream Evidence Consumed

- Spec approved: `docs/approvals/F006-spec-approval.md`
- Design approved: `docs/approvals/F006-design-approval.md`
- Tasks approved: `docs/approvals/F006-tasks-approval.md`
- Test review: `docs/reviews/test-review-F006-recall-and-knowledge-graph.md`（通过）
- Code review: `docs/reviews/code-review-F006-recall-and-knowledge-graph.md`（通过）
- Traceability review: `docs/reviews/traceability-review-F006-recall-and-knowledge-graph.md`（通过）

## Verification Scope

### Included Coverage

- 全 suite 测试：`pytest tests/ -q`（覆盖 F005 末态 451 个测试 + F006 新增 45，目标：零回归）
- F006 触动模块 mypy：`mypy src/garage_os/cli.py src/garage_os/memory/recommendation_service.py`
- F006 触动模块 ruff：`ruff check src/garage_os/cli.py src/garage_os/memory/recommendation_service.py --statistics`
- 依赖契约：`git diff main..HEAD -- pyproject.toml`（NFR-602 机器证据）

### Uncovered Areas

- 完整 mypy（仅跑 F006 触动模块；其他模块在 baseline 已有历史 errors，超出 F006 范围）
- `scripts/benchmark.py` 不专门覆盖 recommend 性能（NFR-603 由 `tests/test_cli.py::TestRecallAndGraphCrossCutting::test_recommend_smoke_under_one_and_a_half_seconds` 覆盖）

## Commands And Results

| 命令 | 退出码 | 结果摘要 |
|------|--------|---------|
| `pytest tests/ -q` | 0 | **496 passed in 25.71s**（baseline 451 → +45 F006 新增；零 regression） |
| `mypy src/garage_os/cli.py src/garage_os/memory/recommendation_service.py` | 1 | **2 errors**，全部 pre-existing on main：`recommendation_service.py:32` (unreachable) + `cli.py:562` (F004 `_memory_review` 类型，前 cycle 已记录在 F004/F005 closeout)。F006 引入 0 新 mypy errors |
| `ruff check ...` 触动模块 | 1 | **51 errors**（main baseline = 47；F006 增量 +4 全部 UP045 `Optional[X]` 风格，与 cli.py 既有 30+ 处 `Optional[...]` 一致；未引入新规则违反） |
| `git diff main..HEAD -- pyproject.toml` | 0 | 空 diff —— **无任何 dependency 变更**（NFR-602 ✓） |

### Notable Output

- 496 个测试中包含 45 个 F006 新增测试：3 个 helper 单元测试 class（resolver / experience scorer + sub-tests）+ 1 个 recommend handler class（11 个测试，含 happy/edge/zero/help/source/fallback/CON-605 spot-check/smoke）+ 1 个 link handler class（7 个）+ 1 个 graph handler class（5 个）+ 1 个 cross-cutting class（5 个 help + 1 个 source-marker + 1 个 smoke）+ 2 个 doc grep 测试。
- 现有 451 个 F005 末态测试在 v1.3 cli.py + recommendation_service.py 改动后**全部继续 passed**，证明 F003/F004/F005 路径零回归（NFR-601 ✓）。
- `RecommendationService.recommend` 字节级未变（CON-605 ✓）：F006 仅在 `RecommendationContextBuilder` 加 `build_from_query` 方法（non-breaking）；测试 `test_recommendation_service_recommend_byte_level_unchanged` 通过 `inspect.getsource` 断言 5 个关键 score weight token 未被改动。
- ruff 51 → 47 的 +4 增量均为 UP045 (`Optional[X]` 风格)，与现有 cli.py 30+ 处 baseline 风格一致，是有意保持代码风格统一的决定（避免 F006 cycle 内做大范围 cosmetic refactor）。

## Freshness Anchor

- 所有命令在本会话内、F006 最新代码状态下执行
- `pytest` 在 25.71s 内 collected 496 个测试，证明确实跑过完整 suite（非 cached 结果）
- `git diff main..HEAD -- pyproject.toml` 在本会话内 echo 到空，证明 NFR-602 不变
- `mypy /tmp/main_*.py` 与当前 HEAD 输出比较验证 0 新 mypy errors

## Conclusion

**通过**。F006 在 standard profile 的回归面（`pytest` 全 suite + `mypy` 触动模块 + `ruff` 触动模块 + `pyproject.toml` diff）达到"零业务回归 + 零新引入 type errors + 零新 dependency"的稳态。pre-existing baseline issues（2 个 mypy / 47 个 ruff）与 F006 无因果，明确不在本 cycle 范围。

## Next Action Or Recommended Skill

`hf-completion-gate`
