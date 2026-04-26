# F014: Workflow Recall — hf-workflow-router 从历史路径主动建议下一节点

- **状态**: 草稿 r1 (待 hf-spec-review)
- **主题**: F004 ExperienceIndex 已积累每次 cycle 的 task_type / skill_ids / problem_domain / lessons_learned 等数据, 但 hf-workflow-router 当前仅按 "工件状态 + 用户意图" 做静态决策, 不消费这些历史数据. F014 加 **Workflow Recall**: router 在 step 4 / 6 决策时, 查 ExperienceIndex 找过去同类型 task 走过的路径 (例 "上次 problem_domain=cli-design 的 cycle 跑了 hf-specify→hf-design→hf-tasks→T1-T5"), 在 handoff 块输出"基于历史经验建议: 下一节点 X (依据 N 次同类 cycle)" — 半自动编排. 用户仍可改, 但默认建议在握.
- **日期**: 2026-04-26
- **关联**:
  - vision-gap 答疑 (上一对话): § 6 P1-2 "工作流半自动编排" 单一最优 F014 候选
  - growth-strategy.md § Stage 3 第 68 行 "工作流编排从手动变成半自动" — 当前唯一未交付项 (Stage 3 ~85% → 推到 ~95%)
  - F004 — `ExperienceIndex.list_records()` + `search(task_type, skill_ids, domain, key_patterns)`
  - F006 — `garage recommend` 已有 cross-domain active recall (但仅作用于 knowledge + experience 内容; 不路由 workflow)
  - F011 — production agents (`code-review-agent` / `blog-writing-agent`); 本 cycle 不动 agent 自动组装 (留 F015+)
  - F013-A — skill mining push (本 cycle 复用 SkillSuggestion pattern: workflow-recall 是 ExperienceRecord 上的另一种 push 信号)
  - manifesto 信念 B4 "人机共生"; user-pact (4) 透明可审计 + (5) 你做主
  - 调研锚点 (基于 main `f5950b4` 实际代码):
    - hf-workflow-router skill: `packs/coding/skills/hf-workflow-router/SKILL.md` (24 个 hf-* skill 的 runtime authority)
    - F004 ExperienceIndex: `src/garage_os/knowledge/experience_index.py` `list_records()` (L160) / `search(task_type=None, skill_ids=None, domain=None, key_patterns=None)` (L77)
    - F004 ExperienceRecord schema: `src/garage_os/types/__init__.py:124-147` 含 `task_type: str` + `skill_ids: list[str]` + `problem_domain: str` + `key_patterns: list[str]` + `lessons_learned: list[str]` + `created_at: datetime`
    - F006 graph: `garage recommend` CLI (cli.py L2080+); 仅 ranked recall, 不 emit workflow path
    - F003 candidate model: `src/garage_os/memory/candidate_store.py`; F014 不动 candidate, 是另一类 sibling 推荐

## 1. 背景与问题陈述

post-F013-A vision-gap 分析显示, growth-strategy.md § Stage 3 健康表现 5 项里, 第 4 项 "系统能指出 pattern → skill" 已被 F013-A 闭合. 但 § Stage 3 工匠核心新增的第 3 行 (§ 56-69 行) **"工作流编排从手动变成半自动"** 仍未交付:

> 核心新增:
> - ✅ 重复模式自动识别并建议为 skill 模板 (F013-A)
> - ⚠️ Skills 可组合成专用 agents (F011 半交付; agent.md 仍手写, 无 compose 路径)
> - ❌ **工作流编排从手动变成半自动** ← F014 目标

### 1.1 当前断点 (post-F013-A)

```
用户说 "继续推进" / "推 F014" → hf-workflow-router 看工件状态 → handoff 到 leaf skill
                                  ↑
                                  纯静态决策: 用户意图 + 工件状态; 不读 .garage/experience/
```

ExperienceIndex 里已经有 13 个 cycle (F001-F013-A) 的 ExperienceRecord (假设用户开了 extraction_enabled), 每条带:
- `task_type` (例 "review", "implement", "specify")
- `skill_ids` (例 ["hf-specify", "hf-spec-review"])
- `problem_domain` (例 "cli-design", "review-verdict")
- `key_patterns` (例 ["5-section-verdict-format"])
- `lessons_learned` (例 ["先 read spec 再 design"])

但 router **从来不查这些数据**. 用户每次都从零开始决策路径, 即便上次刚跑过完全相同类型的 cycle.

### 1.2 真实摩擦量化

- F011 / F012 / F013-A 三次 cycle 都用了 `full profile + auto-streamlined review chain` 同样的路径; 用户每次都手动选 (router 不主动建议)
- F012 / F013-A 都遇到 "spec r1 → r2 → APPROVED" 同样的迭代节奏, router 不会说 "上次 spec r1 平均 12 finding, r2 平均 0; 建议 r1 后直接进 reviewer"
- 用户跨多个 problem_domain 切换 (cli-design / review-verdict / pack-lifecycle / skill-mining) 时, router 不会建议 "你上次做 review-verdict 时 hf-test-driven-dev 卡在 perf gate, 这次提前考虑 perf budget"

→ **F014 的核心承诺**: 当 router 在 step 4 / 6 决策时, 查 ExperienceIndex 找过去同 (task_type | problem_domain) 的 N 条 ExperienceRecord, 提取它们走过的 skill 序列, 输出 handoff 块附带"基于 N 次同类经验建议路径 X" 提示.

### 1.3 与 user-pact "你做主" 的边界

F014 不会:
- 自动跳到建议节点 (B5 user-pact 红线)
- 改 hf-workflow-router 的 authoritative routing 决策权 (router 仍是最终节点, F014 只是数据补给)
- 写任何文件到 packs/ 之外 (除 .garage/workflow-recall/ 自己拥有的目录)
- 删除 ExperienceRecord (read-only on F004)

F014 只会:
- 读 ExperienceIndex (read-only)
- 计算 (task_type, problem_domain) bucket 内的 skill_ids 序列频率
- 在 handoff 块附带 advisory 文字 (不是 directive)
- 在 `garage recall` (新 subcommand) 输出可查的 historical-path 数据

## 2. 目标与成功标准

### 2.1 范围

**A. Path Recall Engine** (FR-1401):
- 在 `src/garage_os/workflow_recall/` 顶级包内实现 `PathRecaller`
- 输入: 当前 task hint (含可选的 task_type / problem_domain / skill_id) + ExperienceIndex
- 输出: `RecallResult` 含 top-K 历史 skill 序列 + N 计数 + 平均耗时 + lessons_learned 摘要
- 聚类规则: 按 (task_type, problem_domain) 配对; 同 bucket 内按 created_at desc 取最近 N (默认 10) 条; 提取 skill_ids 序列频率 (前缀树或 Counter)
- 阈值: bucket 内至少 3 条记录才输出建议; 否则返回空 (避免噪声)

**B. `garage recall workflow` CLI** (FR-1402):
- `garage recall workflow [--task-type X] [--problem-domain Y] [--skill-id Z] [--top-k 3]`
- 输出表格: skill_id 序列 + N 命中 + 平均耗时 + 关键 lessons_learned (按频率排前 3)
- `--json` flag 输出机器可读 (供 hf-workflow-router 调用)
- 与 F006 `garage recommend` 区分: recommend 推内容 (knowledge entry); recall workflow 推路径 (skill_id 序列)

**C. hf-workflow-router 集成** (FR-1403):
- 修改 `packs/coding/skills/hf-workflow-router/SKILL.md`: 在 step 4 (Workflow Profile 决策) 前加 step 3.5 "查历史路径", 描述如何调用 `garage recall workflow --json` (或者直接读 `.garage/workflow-recall/` cache, 见 D)
- handoff 块附加 `Historical advisory` 段 (可选; 阈值不足时省略); 显式标 "advisory only — 用户可改"
- **router 文档化更新, 不改代码**: hf-workflow-router 是 markdown skill, F014 只改 SKILL.md 描述 + 加 `references/recall-integration.md`; 实际调用方是 agent (例 Cursor / Claude Code), 它读 SKILL.md 执行

**D. Cache 层** (FR-1404):
- `garage recall workflow --rebuild-cache` 主动重算 + 写 `.garage/workflow-recall/cache.json`
- cache 含 (task_type, problem_domain) → ranked sequences, 增量扫: 只处理 created_at > last_indexed 的新 ExperienceRecord
- 每次 ExperienceIndex 写新 record 后由 SessionManager._trigger_memory_extraction 末尾自动 invalidate cache (与 F013-A SkillMiningHook 同 pattern, 但是单独 hook)
- 失效后 lazy 重建: 下次 `garage recall workflow` 触发

**E. Audit & Sentinels** (FR-1405):
- `garage status` 加 workflow-recall 段: "Workflow recall: scanned X records / Y buckets / Z advisories cached"
- INV-F14-1 sentinel: F014 是 read-only 在 ExperienceIndex; 不写不删既有 record
- INV-F14-5 sentinel: hf-workflow-router 既有 SKILL.md byte hash 守门 (改动需明确; 不漂移)

### 2.2 范围内变化

- 新模块 `src/garage_os/workflow_recall/`:
  - `types.py`: `RecallResult` + `WorkflowAdvisory` dataclass
  - `path_recaller.py`: 主聚类 + 序列频率计算
  - `cache.py`: `.garage/workflow-recall/cache.json` CRUD + 增量索引
  - `pipeline.py`: 端到端 (cache invalidation hook + status summary)
- 新 CLI subcommand: `garage recall workflow` (注: F006 `garage recommend` 不变; F014 是 sibling)
- `garage status` 加 workflow-recall 段
- `packs/coding/skills/hf-workflow-router/SKILL.md` 加 step 3.5 + handoff 块 advisory 描述
- `packs/coding/skills/hf-workflow-router/references/recall-integration.md` 新文件
- 新 .garage 目录: `.garage/workflow-recall/{cache.json, last-indexed.json}`
- platform.json schema: `workflow_recall.enabled: bool` (默认 true; fallback gate)

### 2.3 范围外 (Out of scope)

- 不做 agent 自动组装 (`garage agent compose`) — F015+ 候选
- 不做 NLP-based skill_ids 序列相似度 (启发式: prefix 匹配 + Counter 频率)
- 不做 router 自动跳转 (B5 user-pact 红线; 仅 advisory)
- 不做跨用户经验聚合 (user-pact 不承诺多用户)
- 不修改 ExperienceRecord schema (CON-1401 字节级不变)
- 不动 F003 候选 / F004 KnowledgeStore / F006 recommend / F010 sync / F011 STYLE / F012 lifecycle / F013-A skill mining 既有 API

## 3. 功能需求 (FR)

### FR-1401: Path Recall Engine (Ubiquitous)

| 字段 | 值 |
|---|---|
| **触发** | (a) `garage recall workflow` CLI 调用; (b) `garage recall workflow --rebuild-cache` 强制重算 |
| **输入** | task hint = `{task_type?, problem_domain?, skill_id?}` (至少一项非空); ExperienceIndex 全量 |
| **聚类规则** | 按 (task_type, problem_domain) 配对分桶; 同桶内按 created_at desc 取最近 N (默认 10) 条 |
| **序列提取** | 每条 record 的 `skill_ids` 是有序 list, 直接用作序列; 桶内同序列 Counter; 输出 top-K (默认 3) 序列 + 命中次数 |
| **平均耗时** | 桶内所有 record 的 `duration_seconds` 平均 (秒) |
| **lessons_learned** | 桶内 lessons_learned 全部展平 + 频率 Counter, 取 top 3 |
| **阈值** | 桶内 record 数 < 3 → 不输出 advisory (返回空 RecallResult) |
| **输出** | `RecallResult(advisories: list[WorkflowAdvisory], scanned_count: int)` |
| **BDD** | Given: 5 record problem_domain="cli-design", task_type="implement", skill_ids 序列各 ["hf-specify","hf-design","hf-tasks","hf-test-driven-dev"]; When: `recall workflow --problem-domain cli-design`; Then: 输出 1 个 advisory, sequence 命中 5 次, 平均耗时 = mean(durations) |
| **Edge** | 0 record / 不足 3 record → 空 RecallResult; task_type 与 problem_domain 都为空 → 报错 "至少一项非空" |

### FR-1402: `garage recall workflow` CLI (Event-driven)

| Sub-command | 行为 |
|---|---|
| `garage recall workflow` | 报错 "at least one of --task-type / --problem-domain / --skill-id required" |
| `garage recall workflow --task-type X` | 列 X 类 task 的 top-K skill_ids 序列 |
| `garage recall workflow --problem-domain Y` | 列 Y domain 的 top-K 序列 |
| `garage recall workflow --skill-id hf-specify` | 列含 hf-specify 的 task 的 top-K 后续序列 |
| `garage recall workflow --top-k N` | 覆盖默认 3 |
| `garage recall workflow --json` | 输出 JSON (供 router 调用 / 自动化) |
| `garage recall workflow --rebuild-cache` | 强制重算缓存; 默认 lazy 走 cache |

| BDD | Given: 5 record problem_domain="cli-design"; When: `garage recall workflow --problem-domain cli-design`; Then: stdout table 含 1 行 sequence "hf-specify → hf-design → hf-tasks → hf-test-driven-dev" + "5 hits" + "avg 3600s" + lessons_learned 列表 |
| Edge | 不足 3 record → "No workflow advisory yet (3 records minimum; current N for bucket: 2)"; --json 同 empty 时输出 `{"advisories": [], "scanned_count": ...}` |

### FR-1403: hf-workflow-router 集成 (State-driven)

| 改动 | 内容 |
|---|---|
| `packs/coding/skills/hf-workflow-router/SKILL.md` 加 step 3.5 | "若 ExperienceIndex 里有 ≥ 3 条同 (task_type, problem_domain) record, 调用 `garage recall workflow --task-type ... --problem-domain ... --json` 取 top-1 序列, 在 handoff 块附 `Historical advisory: based on N similar cycles, the typical path is <seq>` 提示" |
| `packs/coding/skills/hf-workflow-router/references/recall-integration.md` (新) | 详细描述 advisory 块格式 + JSON schema + 何时省略 + advisory 与 authoritative routing 的关系 (advisory only) |
| handoff 块 advisory 段 | 显式 prefix `Historical advisory:`; 注 "advisory only — 用户可改"; 阈值不足时省略 |

| BDD | Given: ExperienceIndex 里 5 条 problem_domain="cli-design"; When: router step 3.5 调用; Then: handoff 块含 "Historical advisory: based on 5 similar cycles, the typical path is hf-specify → hf-design → hf-tasks → hf-test-driven-dev" |
| Edge | < 3 record → handoff 块不附 advisory 段 (与 F009 + F010 行为一致); 用户显式 "ignore history" → router 跳过 step 3.5 |

### FR-1404: Cache 层 (Optional)

| Trigger | (a) cache stale (last_indexed < latest record created_at); (b) `--rebuild-cache` flag; (c) `SessionManager._trigger_memory_extraction` 末尾 invalidate hook (lazy: 仅删 `.garage/workflow-recall/last-indexed.json`, 下次 read 时重建) |
| Cache 文件 | `.garage/workflow-recall/cache.json` 含 `{(task_type, problem_domain): {sequences: [{skills, count, avg_duration, lessons}], total_records}}` |
| Index 文件 | `.garage/workflow-recall/last-indexed.json` 含 `{last_indexed_at: ISO ts, scanned_count: int}` |
| 失效语义 | invalidate = 删 last-indexed.json; 下次 read 触发全量重算 (本 cycle 不做增量, 留 F015+) |

| BDD | Given: 5 record + cache built; When: 第 6 条 record 写入后 SessionManager 调 invalidate; Then: last-indexed.json 删除; 下次 `recall workflow` 重算 |

### FR-1405: `garage status` 集成 (State-driven)

`garage status` 末尾加段: "Workflow recall: scanned X records / Y buckets / Z advisories" (与 F010 sync / F013-A skill mining 同 pattern). cache stale 时显示 "(stale, will rebuild on next recall call)".

| BDD | Given: 12 record + 4 buckets + 2 buckets ≥ 3 record; When: `garage status`; Then: stdout 含 "Workflow recall: scanned 12 records / 4 buckets / 2 advisories" |

## 4. 不变量 (INV)

| ID | 描述 |
|---|---|
| **INV-F14-1** | path_recaller / cache 是 read-only 在 ExperienceIndex (KnowledgeStore + 不读不写; 仅 ExperienceRecord) |
| **INV-F14-2** | F014 不写文件到 packs/ 之外用户路径 (除 `.garage/workflow-recall/` 自己拥有的目录) |
| **INV-F14-3** | router advisory 仅是 advisory, 不改 router authoritative routing 决策权 (B5 user-pact 守门) |
| **INV-F14-4** | F004 ExperienceIndex / ExperienceRecord schema + API 字节级不变 (CON-1401) |
| **INV-F14-5** | hf-workflow-router 既有 7 步流程不变, 仅在 step 3 / 4 之间插入 step 3.5 (additive 改动); 既有 BDD 仍过 |

## 5. 约束 (CON)

| ID | 描述 |
|---|---|
| **CON-1401** | F003-F013 既有 API + schema 字节级不变 (新 RecallResult / WorkflowAdvisory 是 sibling type, 不嵌入既有 record) |
| **CON-1402** | 零依赖变更 (`pyproject.toml + uv.lock` diff = 0); 全 stdlib (json / collections / pathlib / dataclasses) |
| **CON-1403** | 性能: 1000 ExperienceRecord 全量重算 ≤ 2s on local SSD (比 F013-A pattern_detector 快, 因为 simpler counter aggregation) |
| **CON-1404** | router 的 markdown 改动不能破坏既有 24 个 hf-* skill 测试 (skill anatomy + neutrality test) |
| **CON-1405** | `garage recall workflow` 与 F006 `garage recommend` 完全独立; recall workflow 推路径, recommend 推内容; 不混入既有 recommend 路径 |

## 6. 假设 (HYP)

| ID | 描述 |
|---|---|
| **HYP-1401** | 用户的 .garage/experience/records/ 中真有可挖的 task_type / problem_domain 重复. 当前 dogfood 仓库为空 (vision-gap § 3 已注), F014 阈值 N ≥ 3 在用户首次跑时无 advisory; 用户用其他项目 dogfood 后会触发 |
| **HYP-1402** | router agent (Cursor / Claude Code) 会读 step 3.5 + 调用 `garage recall workflow --json`. 如果 agent 不调, 退化为纯文档化 advisory 块, 仍有审计价值 |
| **HYP-1403** | top-1 sequence 是用户最可能想走的路径. 若用户 reject 该建议, 不会因为系统 "建议错了" 而拒绝整个 F014 |
| **HYP-1404** | 用户接受 advisory + authoritative routing 的双层模型 (advisory 不绑定决策) |

## 7. 风险 (RSK)

| ID | 描述 | 缓解 |
|---|---|---|
| **RSK-1401** | 小 ExperienceIndex (< 3 record) 永不触发, 给用户 "系统好像没工作" 错觉 | `garage status` 始终显示 "Workflow recall: scanned X / Y / Z" 元数据行 (Z=0 也显, 与 F013-A status 同模式) |
| **RSK-1402** | advisory 序列质量取决于 skill_ids 序列是否本身就是好序列; 若 record 来自坏路径, advisory 也坏 | 阈值 N ≥ 3 + 标 "based on N similar cycles" 让用户自己判断; 不假装权威 |
| **RSK-1403** | router 改动破坏既有 hf-* skill 编排 | INV-F14-5 sentinel + neutrality test + 改动仅 step 3.5 additive |
| **RSK-1404** | cache 与 ExperienceIndex 漂移 (用户手动改了 record 但没 invalidate) | invalidate hook 由 SessionManager 自动调; 用户也可 `--rebuild-cache` 强制重算 |
| **RSK-1405** | 用户在 multi-feature 场景下不希望看 advisory | router step 3.5 描述 "若 ExperienceIndex 不存在或为空, 跳过"; 用户也可显式 `garage recall workflow --json` 自己看 |

## 8. 验收 BDD (Acceptance)

### 8.1 Happy Path: 5 同类 cycle → recall → router 拿 advisory

```
Given:
  .garage/experience/records/ 含 5 个 ExperienceRecord, 全部:
    task_type="implement", problem_domain="cli-design",
    skill_ids=["hf-specify", "hf-design", "hf-tasks", "hf-test-driven-dev"],
    duration_seconds in [3000, 4000, 3600, 3500, 3800]
    lessons_learned 含 ["先 read spec 再 design", "perf 单测优先"]

When:
  garage recall workflow --problem-domain cli-design

Then:
  stdout table 含 1 行:
    sequence "hf-specify → hf-design → hf-tasks → hf-test-driven-dev"
    hits 5
    avg duration 3580s
    top lessons "先 read spec 再 design (5x)", "perf 单测优先 (5x)"

When:
  garage recall workflow --problem-domain cli-design --json

Then:
  stdout JSON `{"advisories": [{"skills": [...], "count": 5, "avg_duration": 3580.0, "lessons": [...]}], "scanned_count": 5}`
```

### 8.2 Empty path

```
Given: 0 record (空 ExperienceIndex)
When: garage recall workflow --problem-domain cli-design
Then: stdout "No workflow advisory yet (3 records minimum; current N for bucket: 0)"
And: --json 输出 `{"advisories": [], "scanned_count": 0}`
```

### 8.3 Cache invalidation

```
Given: 5 record + cache 已建; last-indexed.json mtime = T1
When: 第 6 条 record 写入触发 SessionManager._trigger_memory_extraction → invalidate hook
Then: .garage/workflow-recall/last-indexed.json 删除
When: garage recall workflow --problem-domain cli-design
Then: cache 重算; stdout 含 6 hits (新 record 计入)
```

### 8.4 router advisory in handoff

```
Given: ExperienceIndex 5 record + router 现在跑到 step 3.5
When: router 按 SKILL.md 调用 `garage recall workflow --task-type implement --problem-domain cli-design --json`
Then: router handoff 块附:
  "Historical advisory: based on 5 similar cycles, the typical path is
   hf-specify → hf-design → hf-tasks → hf-test-driven-dev (avg 3580s).
   Top lessons: 先 read spec 再 design; perf 单测优先.
   advisory only — 用户可改"
```

### 8.5 `garage status` 集成

```
Given: 12 record + 4 (task_type, problem_domain) buckets + 2 buckets ≥ 3 record
When: garage status
Then: stdout 末尾含 "Workflow recall: scanned 12 records / 4 buckets / 2 advisories"
```

## 9. 实施分块预览 (草拟; 真正分块由 hf-tasks 决定)

| 任务 | 描述 | 复用 |
|---|---|---|
| **T1** | `workflow_recall/{__init__, types.py, cache.py}` (RecallResult/WorkflowAdvisory + cache CRUD) + 8 测试 | F013-A SuggestionStore pattern |
| **T2** | `workflow_recall/path_recaller.py` (聚类 + 序列 Counter + 阈值) + 12 测试 | F004 ExperienceIndex.list_records / search |
| **T3** | `workflow_recall/pipeline.py` + invalidate hook + `garage status` 集成 + 6 测试 | F013-A SkillMiningHook pattern |
| **T4** | CLI `garage recall workflow` (含 --task-type / --problem-domain / --skill-id / --top-k / --json / --rebuild-cache) + 8 测试 | F006 garage recommend CLI pattern |
| **T5** | hf-workflow-router SKILL.md step 3.5 + references/recall-integration.md + AGENTS / RELEASE_NOTES + manual smoke + 6 测试 | F012-D RELEASE_NOTES pattern + F013-A AGENTS section pattern |

预估增量测试: ~40 (基线 main `f5950b4` snapshot 后 → +40; 实际基线由 tasks 阶段定). 无新依赖.

## 10. 与 vision 的对照

| 维度 | F014 推动后 |
|---|---|
| **Stage 3 工匠** | ~85% → **~95%** (workflow 半自动编排闭环, growth-strategy.md § Stage 3 第 68 行 ✅) |
| **Stage 4 生态** | ~40% (维持; F014 不动生态) |
| **B4 人机共生** | 5/5 (维持; F014 是 B4 的进一步具象化) |
| **growth-strategy.md § Stage 3 第 68 行** | ❌ → ✅ (vision 上 F014 唯一闭环条目) |

## 11. 测试基线

实施前再核 `uv run pytest tests/ -q` (main `f5950b4` 当前快照应为 989 passed; F013-A 已 merge); F014 实施完成预计 +40 → ~1029 passed.

---

> **本文档是 spec r1**, 待 hf-spec-review (subagent 派发). r2 起草由 review verdict 驱动.
