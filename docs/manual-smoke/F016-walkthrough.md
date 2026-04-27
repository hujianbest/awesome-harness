# F016 Manual Smoke Walkthrough

- **日期**: 2026-04-27
- **执行人**: Cursor Agent (auto mode)
- **PR**: TBD (branch `cursor/f016-memory-activation-bf33`)

## Tracks (4 全绿)

### Track 1 — `garage init --no-memory` + status (FR-1603 + FR-1605 + Im-1 r2)

```
$ garage init --path . --no-memory
Initialized Garage OS in .garage

$ garage status --path .
Memory extraction: disabled — run `garage memory enable` if you want auto-extraction
No data
```

✓ Im-1 r2: Memory extraction 行**跨 No data 早退路径**显示, 即使空 workspace 用户也立即知道 memory 状态.

### Track 2 — `garage memory enable` + status (FR-1601)

```
$ garage memory enable --path .
Memory extraction enabled. Run `garage memory ingest --from-reviews` or `--from-git-log` to backfill historical data.

$ garage memory status --path .
Memory extraction: enabled
KnowledgeEntry: 0
ExperienceRecord: 0
Candidate: 0
Last extraction: never
```

✓ FR-1601 显式 enable 命令 + status 显示零状态.

### Track 3 — `garage memory ingest --from-reviews` (FR-1602)

```
$ ls docs/reviews/
spec-review-f012-r1-2026-04-25.md
design-review-f013-r1-2026-04-26.md

$ garage memory ingest --path . --from-reviews
Ingested 2 new from reviews (0 skipped)

$ garage memory status --path .
Memory extraction: enabled
KnowledgeEntry: 0
ExperienceRecord: 2
Candidate: 0
Last extraction: 2026-04-27 14:54:15
```

✓ 2 ExperienceRecord 写入 (problem_domain ∈ {f012, f013} lowercase Im-3 r2; skill_ids ['hf-spec-review'] / ['hf-design-review']).

### Track 4 — `garage memory ingest --style-template python` (FR-1604)

```
$ garage memory ingest --path . --style-template python
Ingested 7 new from style-template:python (0 skipped)

$ garage memory status --path .
Memory extraction: enabled
KnowledgeEntry: 7
ExperienceRecord: 2
Candidate: 0
Last extraction: 2026-04-27 14:54:15
```

✓ 7 KnowledgeEntry(KnowledgeType.STYLE) 写入 (来自 packs/garage/templates/style-templates/python.md 的 7 条 entries: prefer-functional-python / type-hints-required / f-string-over-percent / pathlib-over-os-path / dataclass-over-tuple / pytest-fixture-naming / no-mutable-default-args).

## 测试基线

- F015 baseline: 1103 passed
- F016 实施完成 T1-T4: **1149 passed** (+46, 0 regressions)
- INV-F16-1..5 全部通过
- CON-1601..1605 全部通过 (含 Cr-1 r2 critical sentinel: --yes 不开 memory)

## Conclusion

✅ F016 4 tracks 全绿. Memory activation 完整: 显式 enable + 历史回填 + STYLE 模板. growth-strategy.md § Stage 3 健康表现第 2 项 "知识条目增长随使用自然" ⚠️ 本仓库 0 → ✅ 用户启动后 ≥ 9 entries (2 ExperienceRecord + 7 KnowledgeEntry STYLE; 真实使用还会更多).

**用户从安装 garage 到看到 push 信号** (F013-A skill suggest / F014 recall / F015 STYLE alignment) 路径从"读 5 份 docs + 编辑 platform.json + 手动 add 14 条 record"缩短到 **3 个 CLI 命令**:
```bash
garage init                                    # interactive prompt enable
garage memory ingest --from-reviews            # 历史回填
garage memory ingest --style-template python   # STYLE 模板
```
