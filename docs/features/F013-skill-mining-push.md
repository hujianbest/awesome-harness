# F013-A: Skill Mining Push 信号 — 系统主动建议 "pattern → skill"

- **状态**: 草稿 r1 (待 hf-spec-review)
- **主题**: F003-F006 投入了完整的 memory 提取管道 (signals → candidates → review queue → KnowledgeStore), 但只有 **pull 端** (用户主动 `knowledge search` / `recall`). F013-A 加 **push 端**: 当系统在 N 次会话里看见同一类 problem_domain + tag 组合反复出现时, 主动建议 "这个模式可以变成 skill", 半自动产 SKILL.md 草稿, 嵌 hf-test-driven-dev 走完 promote 流程.
- **日期**: 2026-04-25
- **关联**:
  - vision-gap planning artifact `docs/planning/2026-04-25-post-f012-next-cycle-plan.md` § 3 (F013-A Path A 单一最优)
  - F003 — `memory` 模块 (CandidateStore + ExtractionOrchestrator + 候选生命周期)
  - F004 — ExperienceIndex + ExperienceRecord (索引 + 检索)
  - F005 — `garage knowledge add` CLI (promote 的写出端)
  - F006 — knowledge graph + `garage recommend` (候选证据链关联)
  - F008 — `packs/<pack-id>/skills/<skill>/SKILL.md` 目录契约 (promote 的目标)
  - F011 — `hf-test-driven-dev` skill (promote 后 skill writing 入口) + KnowledgeType.STYLE (candidate 标签维度)
  - F012-D — anonymize 规则 (promote 前可复用脱敏)
  - manifesto 信念 B4 "人机共生" + Stage 3 "工匠" (重复模式自动识别并建议为 skill 模板)
  - growth-strategy.md § 1.3 触发信号 第 4 行 "系统能指出 pattern → skill" — 当前唯一未达成项
  - user-pact "你做主": 所有自动化都有开关, 关键决策由用户做
  - 调研锚点:
    - F003 candidate 模型: `src/garage_os/memory/candidate_store.py` `store_candidate(candidate: dict[str, Any])` + `list_candidates_by_status(status)` (lines 39-86)
    - F003 extraction trigger: `ExtractionOrchestrator.extract_for_archived_session_id(session_id)` (在 `extraction_orchestrator.py`)
    - F004 experience: `ExperienceRecord` + `ExperienceIndex.search(skill_ids, key_patterns, tags)` (`experience_index.py:77`)
    - F006 graph: `KnowledgeStore.list_entries()` 返回 `KnowledgeEntry` 含 `tags / problem_domain / source_session`
    - F008 skill anatomy: `docs/principles/skill-anatomy.md` (frontmatter + Workflow + Output Contract + Red Flags + Verification 5 段)
    - F011 hf-test-driven-dev: `packs/coding/skills/hf-test-driven-dev/SKILL.md` (skill writing 入口 — promote 后跳转)

## 1. 背景与问题陈述

F012 把 garage 的 **能力分发链路** 闭环 (install ↔ uninstall ↔ update ↔ publish + 脱敏 export); F010 把 **memory 飞轮** 闭环 (sync 推 ↔ ingest 拉). 但 garage 整个 vision 还有一个仍未达成的关键能力, 直接对应 `growth-strategy.md` 第 1.3 节 Stage 3 健康表现的第 4 行:

> **系统能指出 "这个模式可以变成 skill"** — ❌ 未实现

### 1.1 当前断点 (post-F012)

```
session ─┐
         ├→ archive_session ──→ ExtractionOrchestrator ──→ candidates ──→ review queue
session ─┤    (F010 ingest)        (F003)                    (F003)         (F003)
         │                                                       │
session ─┘                                                       ↓
                                                          KnowledgeStore (F004)
                                                                 │
                                                       ┌─────────┼─────────┐
                                                       ↓         ↓         ↓
                                              recall (F006)  search    sync (F010)
                                                                 ↓
                                                       host context surface
```

**现状**: 整条管道只有"用户主动拉"出口 (recall / search / sync 都是 pull); **缺"系统主动推"出口** — 系统对积累的 KnowledgeEntry + ExperienceRecord 没有任何"模式扫描" 行为, 所以 33 个 skill 不会因为用户使用而长成 34 个.

### 1.2 真实摩擦量化

- 当前 garage 仓库自身 dogfood 中, 有效 KnowledgeEntry 数量: 待标定 (取 `.garage/knowledge/` 文件夹下 `.md` count)
- 当前 ExperienceRecord 数量: 待标定 (取 `.garage/experience/` count)
- F011/F012 cycle 中累计了 ~50 次 review verdict 写入 (test-review/code-review/traceability/regression/completion), 但 **没有一次** 触发 "这个模式 (例 'review verdict 5 段格式') 可以提到 skill"
- F008 + F011 + F012 三次 cycle 的 hf-test-driven-dev 反复迭代了 "实施 → review → 修正 → 再 review" 节奏, 但这个节奏没有从 candidate 提炼过 (用户全靠手动 commit pattern)

→ **F013-A 的核心承诺**: 当 ExperienceIndex / KnowledgeStore 里同一 problem_domain + tag 组合在 ≥ N 次 session 出现时, 系统在 `garage status` 显示 "💡 X 个候选模式可考虑提为 skill" + 提供 `garage skill suggest` 列表 + `garage skill promote` 半自动转换路径.

### 1.3 与 user-pact "你做主" 的边界

F013-A 不会:
- 自动 commit 任何 SKILL.md 到 packs/ (B5 user-pact 红线)
- 自动改 packs/<pack-id>/pack.json (skills[] 列表) 而不经用户确认
- 删除候选记录 (即便用户 reject, 也仅标 `status: rejected` 不物理删, 30 天后 audit decay)

F013-A 只会:
- 扫描 + 评分 + 显示候选 (read-only)
- 在用户显式 `--yes` / interactive 同意时, 把候选转成 SKILL.md 草稿 + 触发 hf-test-driven-dev 路径 (skill writing 仍由用户主导, garage 只生成骨架)

## 2. 目标与成功标准

### 2.1 范围

**A1. Pattern Detection** (FR-1301):
- 在既有 F003 `ExtractionOrchestrator` 完成后, 异步扫描 `KnowledgeStore.list_entries()` + `ExperienceIndex.list_records()`, 按 (problem_domain, tag-bucket) 维度聚类
- 发现某 (domain, tag) 组合在 ≥ N 次 session 出现且当前未对应任何已有 SKILL.md 时, 生成 SkillSuggestion 写到 `.garage/skill-suggestions/`
- 阈值 N 默认 = 5, 通过 `~/.garage/skill-mining-config.json` 用户可调
- SkillSuggestion = `{id, suggested_name, suggested_description, problem_domain, tags[], evidence_entries[], evidence_records[], suggested_pack, score, status, created_at, expires_at}`
- status enum: `proposed | accepted | rejected | promoted | expired`

**A2. `garage skill suggest` CLI** (FR-1302):
- `garage skill suggest` (无参数): 列所有 status=proposed 的候选, 按 score 降序, 显示 id / name / N evidence / pack
- `garage skill suggest --id <suggestion-id>`: 显示某候选的详情 — 命中证据链 (knowledge entry id 列表 + experience record id 列表) + 估计的 SKILL.md 模板 preview
- `garage skill suggest --status all`: 列含 rejected/promoted/expired 状态的全部候选
- `garage skill suggest --threshold N`: 临时降低 / 升高阈值重扫一次 (不修改 config, 仅本次)

**A3. Skill Template Generator** (FR-1303):
- 输入: 一个 SkillSuggestion + 一个目标 pack-id (默认 `garage`)
- 输出: SKILL.md 草稿, 严格遵 `docs/principles/skill-anatomy.md` 7 原则:
  - frontmatter 含 `name` (来自 suggested_name) + `description` (来自 suggested_description, 包含 "适用 / 不适用" 两段)
  - Workflow section 骨架 (从 evidence experience records 的 phase 字段抽 phase 序列)
  - Output Contract section 骨架 (从 evidence knowledge entries 的 type 字段抽出)
  - Red Flags section 骨架 (留 placeholder, 用户填)
  - Verification section 骨架 (从 evidence 中 commit_sha / test_count 字段抽)
- 不写任何 placeholder 到 packs/ 之外的位置; 不会 commit
- 模板写到临时目录, 由 promote 命令决定是否落到 packs/

**A4. `garage skill promote` 半自动流程** (FR-1304):
- `garage skill promote <suggestion-id>`: prompt 用户确认 — 显示 SKILL.md preview + 候选 pack-id + 名字; 用户 `y` 后:
  1. 创建 `packs/<pack-id>/skills/<suggested-name>/SKILL.md` (使用 A3 生成的草稿)
  2. 把 SkillSuggestion status 改为 `promoted` + 记录 `promoted_to_path`
  3. 提示用户 "Now run `garage run hf-test-driven-dev --skill <name>` to refine the draft" (B5: 不自动跳, 给路径)
  4. 不动 packs/<pack-id>/pack.json (skills[] 自动加是过度自动化; 用户用 hf-test-driven-dev 路径自己加)
- `garage skill promote <suggestion-id> --reject`: status=rejected + reason prompt
- `--yes`: 跳过 confirmation prompt
- `--dry-run`: 显示将创建什么但不写
- `--target-pack <pack-id>`: 覆盖 default `garage` (例如 promote 到 packs/coding/)

**A5. Audit / Decay** (FR-1305):
- 每次 `garage status` 检查 `.garage/skill-suggestions/` 目录, 显示 "💡 N proposed / M expired" 摘要
- proposed status 默认 30 天 expiry (`expires_at` 字段); 过期自动归 expired (不删, 用户可 `garage skill suggest --status expired` 看)
- rejected status 永久保留 (供未来 audit "为什么这个 reject"), 但不再扫到同 (domain, tag) 组合 — `_recompute_evidence` 跳过 rejected suggestion 已 cover 的 (domain, tag)
- 用户可显式 `garage skill suggest --purge-expired` 物理删 expired 记录

### 2.2 范围内变化

- 新模块 `src/garage_os/skill_mining/`:
  - `types.py`: `SkillSuggestion` dataclass + status enum
  - `pattern_detector.py`: 聚类 + 评分 + 写 suggestion
  - `template_generator.py`: SKILL.md 草稿生成 (A3)
  - `suggestion_store.py`: `.garage/skill-suggestions/` 文件 CRUD
  - `pipeline.py`: 端到端 (扫 → 写 → CLI 出口)
- 新 CLI subcommand: `garage skill suggest` + `garage skill promote`
- `garage status` 加 skill-mining 段 (proposed / expired 摘要)
- `~/.garage/skill-mining-config.json` 加 schema (threshold, exclude_domains, expiry_days)
- 新 .garage 目录: `.garage/skill-suggestions/{proposed/, rejected/, promoted/, expired/}/<suggestion-id>.json`
- `RELEASE_NOTES.md` + `AGENTS.md` 同步

### 2.3 范围外 (Out of scope)

- 不做"自动 commit SKILL.md 到 packs/"(B5 user-pact 红线)
- 不做"自动 publish suggestion 到中央 registry"(F013-J 候选, 推到 F014+)
- 不做"experience export 反向 import"(F013-D 候选, 推到 F014+)
- 不做 NLP-based 模式相似度检测 (P1 启发式: 同 problem_domain + 至少 2 共享 tag = 一类; 复杂度留给 F014+)
- 不做"系统看着用户 review 你的 commit 习惯, 反向产 style skill"(KnowledgeType.STYLE 既有, 不重做)

## 3. 功能需求 (FR)

### FR-1301: Pattern Detection

| 字段 | 值 |
|---|---|
| **触发** | 每次 `ExtractionOrchestrator.extract_for_archived_session_id` 完成后 hook 调用 + `garage skill suggest --rescan` 显式触发 |
| **输入** | `KnowledgeStore.list_entries()` 全部 + `ExperienceIndex.list_records()` 全部 |
| **聚类规则** | 按 (problem_domain, frozenset(tags 中前 2 个 alpha-sorted tag)) 组合分组; 同组内成员 ≥ N (default 5) 即触发 SkillSuggestion |
| **去重** | 若已有 status ∈ {proposed, promoted, rejected} 的 suggestion 覆盖同组合, 不重复生成; 仅扫到 expired 时允许重生 |
| **评分** | `score = log10(N+1) + 0.3 × (unique_session_count) + 0.5 × (max(timestamp).days_since_epoch / 1000)` (近期权重 + session 多样性) |
| **输出** | `.garage/skill-suggestions/proposed/<id>.json` (id = `sg-<yyyymmdd>-<6 hex>`) |
| **BDD** | Given: 5 个 KnowledgeEntry domain="cli-design" + 共享 tag "command-author"; When: trigger; Then: 生成 1 个 SkillSuggestion; And: 同组合再加 1 个 entry, 不再生成新 suggestion (status=proposed 已存在) |
| **Edge** | 0 entry / 全 promoted-pack-skill 已 cover (检测 `packs/*/skills/*/SKILL.md` description 中 problem_domain mention) → 跳过 |

### FR-1302: `garage skill suggest` CLI

| Sub-command | 行为 |
|---|---|
| `garage skill suggest` | 列 status=proposed 候选, 按 score desc, table 含 id / name / N-evidence / score / pack |
| `garage skill suggest --id <sg-id>` | 显示该候选完整 detail: name + description + evidence_entries + evidence_records + 模板 preview (A3 生成) |
| `garage skill suggest --status {proposed,promoted,rejected,expired,all}` | filter 状态 |
| `garage skill suggest --rescan` | 触发 FR-1301 重新扫 (manual) |
| `garage skill suggest --threshold N` | 临时阈值 (本次 list 用) |
| `garage skill suggest --purge-expired` | 物理删 expired 记录 (interactive prompt unless `--yes`) |

| BDD | Given: 3 proposed + 1 promoted; When: `garage skill suggest`; Then: 仅显示 3 行; And: `--status all` 显示 4 行 |
| Edge | empty proposed → "No skill suggestions yet (threshold N=5; try --threshold 3 to lower)"; --id 不存在 → exit 1 + stderr |

### FR-1303: Skill Template Generator

| 输入 | suggestion-id + target-pack-id (default "garage") |
| 输出 | string (SKILL.md draft) — 不写文件 |
| 模板骨架 (skill-anatomy 7 段) | <li>frontmatter (name, description: "适用…不适用…") <li>Workflow (从 evidence experience phase 字段) <li>Output Contract (从 evidence knowledge entry type 字段) <li>Red Flags (placeholder) <li>Verification (placeholder, 提示用户填 commit_sha / test_count) |
| 显式约束 | description ≥ 50 字 (skill-anatomy 7 原则之一); 主文件不超 300 行 (生成的草稿仅 100-150 行) |

| BDD | Given: SkillSuggestion (5 evidence in cli-design domain, tag "command-author"); When: generate template; Then: SKILL.md 草稿含 name="command-author" / description "适用 CLI 命令..." / Workflow 5 phase / Verification placeholder |
| Edge | suggestion 无 evidence → 不应到这步 (FR-1301 ≥ N 守门); 但 generator robust handle: 输出 minimal 模板 + warning |

### FR-1304: `garage skill promote` 半自动

| Flow | 1. Read suggestion + generate template (A3) <li>2. Show preview + target_path; prompt `[y/N]` (除非 --yes) <li>3. y → write `packs/<target-pack>/skills/<suggested-name>/SKILL.md` + suggestion status=promoted <li>4. Echo "Run `garage run hf-test-driven-dev --skill <name>` to refine" (不自动跳) <li>5. n → suggestion 状态不变 (仍 proposed); 用户可下次再 promote |
| `--reject` | status=rejected + 提示输入 reason (record 在 suggestion 文件) |
| `--yes` | 跳 prompt |
| `--dry-run` | 仅显示 preview + target_path, 不写 |
| `--target-pack <id>` | 覆盖 default "garage" |

| BDD | Given: proposed sg-001; When: `promote sg-001 --yes`; Then: `packs/garage/skills/command-author/SKILL.md` 创建 + suggestion status=promoted + stdout "Created skill at ... — Run hf-test-driven-dev to refine"; And: `packs/garage/pack.json` skills[] 不变 (用户自己 run hf-test-driven-dev 后加) |
| Edge | target pack 不存在 → exit 1 + "pack 'X' not installed"; 同名 skill 已存在于 packs/<target>/skills/ → prompt overwrite y/N (B5) |

### FR-1305: Audit / Decay

| Trigger | 每次 `garage status` 调用; 后台 daily expire scan (后续可加, F013-A 仅 manual) |
| Expiry | proposed → expired after `expires_at` (default created_at + 30 days) |
| Status 转换 | proposed → promoted / rejected / expired; rejected 永久; promoted 永久; expired 可被 purge |
| `garage status` 显示 | "💡 N proposed / M expired skill suggestions" 摘要行 (proposed > 0 才显) |
| `garage skill suggest --purge-expired` | 物理删 expired 记录 (prompt unless --yes) |

| BDD | Given: 3 proposed (1 expires today); When: `garage status` 调用; Then: 输出含 "💡 3 proposed (1 expired today) skill suggestions" |
| Edge | 用户改系统时钟 → expiry 仍按文件 mtime 兜底 |

## 4. 不变量 (INV)

| ID | 描述 |
|---|---|
| **INV-F13-1** | F013-A 不写任何文件到 packs/ 之外的"用户拥有 path" (除 .garage/skill-suggestions/ 自己拥有的目录) |
| **INV-F13-2** | promote 必须 opt-in: 默认 prompt; --yes 跳 prompt; --dry-run 不写 (B5 user-pact) |
| **INV-F13-3** | pattern_detector 是 read-only 在 KnowledgeStore + ExperienceIndex 上 (不写不删原数据; 只追加 SkillSuggestion) |
| **INV-F13-4** | Skill template 必须遵 docs/principles/skill-anatomy.md 7 原则 (description 是分类器; 主文件 ≤ 300 行; 边界显式) |
| **INV-F13-5** | F003-F006 既有 API 字节级不变 (CON-1301 守门): 既有 candidate / KnowledgeEntry / ExperienceRecord 数据结构不动, F013-A 仅扩 read 端 + 新增 SkillSuggestion 类型 |

## 5. 约束 (CON)

| ID | 描述 |
|---|---|
| **CON-1301** | F003-F006 + F010 + F011 既有 API + 数据 schema 字节级不变 (新增 SkillSuggestion 是 sibling type, 不嵌入既有 KnowledgeEntry / Candidate) |
| **CON-1302** | F013-A 不引入新 third-party 依赖 (`pyproject.toml + uv.lock` diff = 0); 全部用 stdlib (json / collections / pathlib / dataclasses / re) |
| **CON-1303** | 性能: 1000 个 KnowledgeEntry + 1000 个 ExperienceRecord 的 pattern_detector 扫一次 ≤ 5 秒 (本地 SSD); 否则 fallback 增量扫 (F014+) |
| **CON-1304** | promote 不动 packs/<pack-id>/pack.json (skills[] 列表); 用户用 hf-test-driven-dev 路径自己加. 这条 deliberate, 防止 F013-A 误碰 F011 既有 invariant |
| **CON-1305** | hf-test-driven-dev 路径在 promote echo 中提示, 但不自动 invoke (B5: 关键决策由用户做) |

## 6. 假设 (HYP)

| ID | 描述 |
|---|---|
| **HYP-1301** | 用户的 .garage/knowledge/ + .garage/experience/ 中确实有重复模式可挖. 若 N=5 阈值在用户首次跑时无候选, 用户会主动 `--threshold 3` 试. UX 给出明确提示 |
| **HYP-1302** | skill-anatomy 7 原则足以指导 SKILL.md 模板生成. 模板生成的 description / Workflow 段质量 ≥ 用户手写 baseline 的 60% (足以省 50% 起步时间) |
| **HYP-1303** | 用户接受"系统建议 + 半自动 promote"模式; 不会因为模板质量不完美而拒绝整个 F013-A |
| **HYP-1304** | promote 后用户会 follow up 跑 hf-test-driven-dev (即接受 echo 提示而非直接 commit). 若用户跳过, F013-A 不阻止 (但 README 应文档化) |
| **HYP-1305** | rejected suggestion 永久保留不会爆量 — 一年内 < 100 条 reject (基于个人使用频率估算) |

## 7. 风险 (RSK)

| ID | 描述 | 缓解 |
|---|---|---|
| **RSK-1301** | pattern_detector 对小 KnowledgeStore (< 10 entry) 永远不触发, 给用户"系统好像没工作"的错觉 | `garage status` 始终显示 "Skill mining: scanned X entries / Y records / Z proposed", 即便 Z=0 也告诉用户管道在工作 |
| **RSK-1302** | 模板生成的 description 不准 (只是 evidence 的浅层拼接), 用户嫌 promote 后还得大改 | A3 生成的草稿明确标 "AI-generated skeleton, refine via hf-test-driven-dev"; 不假装是 production-ready |
| **RSK-1303** | F011 既有 hf-test-driven-dev 入口期望"任务计划获批"前置, F013-A promote 后直接跳过去会断节点 | promote echo 不自动跳, 仅给路径 + 用户自己决定怎么走 (走 hf-workflow-router 重新评估 profile / 直接 hf-test-driven-dev); 文档化在 AGENTS.md |
| **RSK-1304** | 同名 skill 已存在 (用户手动写过同名) | promote 时 prompt overwrite y/N; --dry-run 显示 "would overwrite existing"; B5 user-pact 兜底 |
| **RSK-1305** | rejected reason 字段被滥用作"详细技术评论"导致文件膨胀 | reason 字段限制 ≤ 500 字符; CLI prompt 提示 "brief reason" |

## 8. 验收 BDD (Acceptance)

### 8.1 Happy Path: 5 evidence → suggest → promote

```
Given:
  .garage/knowledge/decisions/ 含 5 个 entry, 全部 problem_domain="review-verdict",
    tags ⊃ {"verdict-format", "5-section"}
  .garage/experience/records/ 含 3 个 record, 全部 skill_ids 含 "hf-code-review"

When:
  Run `ExtractionOrchestrator.extract_for_archived_session_id(...)` 完成 (任意 session)
  garage status

Then:
  stdout 含 "💡 1 proposed skill suggestion"
  .garage/skill-suggestions/proposed/sg-*.json 出现 1 个

When:
  garage skill suggest

Then:
  stdout table 含 1 行: name "verdict-format" / N=5 evidence / score >0.5

When:
  garage skill suggest --id sg-XXX

Then:
  stdout 含 evidence_entries (5 ID) + evidence_records (3 ID) + SKILL.md preview

When:
  garage skill promote sg-XXX --yes

Then:
  packs/garage/skills/verdict-format/SKILL.md 创建 (含 frontmatter + 5 段)
  .garage/skill-suggestions/promoted/sg-XXX.json 出现 (proposed/ 中删除)
  stdout "Created skill at packs/garage/skills/verdict-format/SKILL.md
          Run `garage run hf-test-driven-dev --skill verdict-format` to refine"
```

### 8.2 Reject path

```
Given: 1 proposed sg-001
When: garage skill promote sg-001 --reject
Then: prompt for reason; user types "naming conflicts with existing pattern"
And: .garage/skill-suggestions/rejected/sg-001.json 出现 (含 reason)
And: 重新扫 (FR-1301) 不会在同 (domain, tag) 上再生成新 suggestion
```

### 8.3 Audit / Decay

```
Given: 3 proposed (1 created 31 days ago)
When: garage status
Then: stdout 含 "💡 2 proposed / 1 expired skill suggestions"
And: expired/ 目录含 1 个 sg-*.json (从 proposed/ 移过去)

When: garage skill suggest --purge-expired --yes
Then: .garage/skill-suggestions/expired/ 清空
```

### 8.4 Dry-run + Custom target pack

```
Given: 1 proposed sg-002 (default target = garage)
When: garage skill promote sg-002 --target-pack coding --dry-run
Then: stdout 含 "DRY RUN: would create packs/coding/skills/<name>/SKILL.md"
And: packs/coding/skills/ 不变
And: suggestion status 仍 proposed
```

## 9. 实施分块预览 (草拟; 真正分块由 hf-design + hf-tasks 决定)

| 任务 | 描述 | 复用 |
|---|---|---|
| **T1** | `skill_mining/{types.py, suggestion_store.py}` (SkillSuggestion + CRUD) + 8 测试 | F005 KnowledgeStore CRUD pattern |
| **T2** | `skill_mining/pattern_detector.py` (FR-1301 聚类 + 评分 + 阈值) + 12 测试 | F003 candidate model + F004 ExperienceIndex.search |
| **T3** | `skill_mining/template_generator.py` (FR-1303 SKILL.md 草稿) + 10 测试 | docs/principles/skill-anatomy.md schema |
| **T4** | `skill_mining/pipeline.py` (端到端 hook + audit/decay) + CLI `skill suggest` + 12 测试 | F003 ExtractionOrchestrator hook + F006 graph |
| **T5** | CLI `skill promote` + `garage status` skill-mining 段 + AGENTS.md / RELEASE_NOTES + manual smoke + 8 测试 | F011 hf-test-driven-dev echo + F012 RELEASE_NOTES pattern |

预估增量测试: ~50 个 (基线 930 → 980 passed). 无新依赖.

## 10. 与 vision 的对照

| 维度 | F013-A 推动后 |
|---|---|
| **Stage 3 工匠** | ~65% → **~85%** (skill mining 信号闭环, growth-strategy 触发信号 4/4 全过) |
| **Stage 4 生态** | 40% (维持; F013-A 不直接动生态层) |
| **B4 人机共生** | 5/5 (维持; F013-A 是 B4 既有 5/5 的具象化) |
| **growth-strategy 健康表现 第 4 行** | ❌ → ✅ (vision 上 F013-A 唯一闭环条目) |

---

> **本文档是 spec r1**, 待 hf-spec-review (subagent 派发). r2 起草由 review verdict 驱动.
