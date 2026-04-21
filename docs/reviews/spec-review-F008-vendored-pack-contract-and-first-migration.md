# Spec Review — F008 Vendored Pack 契约与首批迁移

- 评审对象: `docs/features/F008-vendored-pack-contract-and-first-migration.md`
- 评审 skill: `hf-spec-review`
- 评审者: reviewer subagent（独立 fresh context）
- 日期: 2026-04-21
- 当前 profile: `full`
- 执行模式: `interactive`

## Precheck

- 稳定规格草稿存在 ✅（492 行，10 FR + 7 NFR + 5 CON + 4 ASM + 4 OQ）
- route/stage/profile 一致 ✅（`task-progress.md` 显示 hf-specify 已完成、待派发 spec-review）
- 上游证据一致 ✅（F007 已批准、F001 CON-002 修订已显式声明）
- 派发请求合法 ✅
- precheck 通过，进入正式 rubric

## 结构契约对齐

`AGENTS.md` 未硬编码 spec 模板，但 F001-F007 已建立的事实模板（背景 → 目标与成功标准 → 角色场景 → 范围 → FR/NFR/CON/ASM/IFR/OQ → 术语）本 spec 全部遵循；章节齐整、FR/NFR 全部带 ID + Statement + Acceptance + Priority + Source；Given/When/Then 形式验收占主导。

## 结论

需修改

判断依据：spec 结构成熟、范围清楚、来源锚点齐全，但**存在 1 条 critical 阻塞性架构不自洽**（vendored 字节零修改 vs F007 `pack_discovery` 强契约 vs F007 Python 零修改三者两两冲突，spec 未给出闭环），以及 4-5 条 important 一致性 / 数量 / 法务问题需要在 1-2 轮定向回修内解决。`G3` Repairable scope 满足，可定向回修，不到"阻塞"程度。

## 发现项

### Critical

- **[critical][USER-INPUT][C2/C7][A6] F-1: vendored pack 字节零修改 vs F007 `pack_discovery` 契约 vs F007 Python 零修改 三者两两冲突，spec 未给出闭环。** 这是本 spec 最大的内在不自洽。
  - F007 既有契约（`src/garage_os/adapter/installer/pack_discovery.py` 已落盘代码）：每个 pack 必须以 `pack_root / "skills" / <skill-id> / "SKILL.md"` 路径暴露 skill；`pack.json.skills[]` 必须 `sorted(declared_skills) == sorted(disk_skills)`，否则抛 `PackManifestMismatchError`（hard error，不是 warning）。
  - 当前 vendored pack 实际 layout（`ls .agents/skills/<pack>/`）：
    - `architecture-designer/SKILL.md`（SKILL.md 在 pack 根，**没有** `skills/` 中间层）
    - `ui-ux-pro-max/SKILL.md`（同上）
    - `writing-skills/SKILL.md`（同上）
    - `write-blog/<skill-id>/SKILL.md`（在 pack 根直接挂 4 个子 skill 目录，**没有** `skills/` 中间层）
    - 只有 `harness-flow/skills/<skill-id>/SKILL.md` 与 F007 契约对齐
  - FR-803 声称"整体 `git mv` 从 `.agents/skills/<name>/` → `packs/<name>/`"。按字面执行后，4/5 个 vendored pack 的 SKILL.md 仍位于 pack 根或 pack 根下一层，与 F007 `_scan_disk_skills` 寻找 `skills/<id>/SKILL.md` 的逻辑不匹配。
  - 后果：FR-805 验收 #1（`.claude/skills/` 下出现 30 个子目录）+ #3（`installed_packs[] = 6`）+ FR-806 验收 #1（30 unique skill name）**全部不可达**，因为 4 个 vendored pack 会被 `pack_discovery` 解析为含 0 个 skill（或抛 `PackManifestMismatchError` 直接退出），最终 `installed_packs` 实质只包含 `garage` + `harness-flow`，`files[]` 远少于 30。
  - 三选一不可同时成立：
    - (a) 真正"整体 git mv 字节零修改" → 违反 F007 契约 → `pack_discovery` 失败或漏载
    - (b) 在 vendored pack 内插入 `skills/<id>/` 中间层目录（即把 `architecture-designer/SKILL.md` 移到 `architecture-designer/skills/architecture-designer/SKILL.md`）→ 违反 NFR-804 vendored 字节零修改（路径重排即使内容字节相同，也是结构修改）
    - (c) 修改 F007 `pack_discovery._scan_disk_skills` 接受新形态 → 违反 NFR-803 / CON-803 不动 F007 Python 代码
  - spec 没有任何段落识别这条冲突，也没有给出选择路径或开放问题。这是一条阻塞性业务事实裁决（用户必须在 (a)(b)(c) 之间选；任何一种选择会改变 NFR-803/804 当前措辞与 FR-803 实施步骤），属于 USER-INPUT。
  - 修复建议：由父会话向用户提一个最小定向问题——"4 个 vendored pack 的 SKILL.md 不在 `pack/skills/<id>/` 而在 pack 根或 pack 根下一层，与 F007 `pack_discovery` 契约不符。可选 (a) 在 pack 根新建 `skills/` 子目录、把 vendored 子树作为 `skills/<pack-id>/` 内容（只重排、不改字节但改路径，需放宽 NFR-804 措辞）；(b) 按 vendored 原 layout 保留、在 design 阶段最小修改 `pack_discovery` 接受 `pack/SKILL.md` + `pack/<id>/SKILL.md` 两种 fallback 形态（违反 CON-803）；(c) 把这 4 个 pack 重新归类为非可分发 fixture，本 cycle 仅 dogfood symlink、不进 `garage init` 管道。" 用户拍板后回 `hf-specify` 改 FR-803 / NFR-803 / NFR-804 / CON-802 / CON-803 三处协调。

### Important

- **[important][USER-INPUT][Q3/C2] F-2: 30 SKILL.md 数量在多处重复，但实测计数 ≠ 30。** 成功标准 #1 / #2、§ 2.1 目标段、FR-804/805/806/807 验收、NFR-801 验收均使用"30 SKILL.md"作为关键数字。实测：
  - harness-flow 内 21 个 hf-* + 1 个 using-hf-workflow = **22** 个 SKILL.md（spec 多处写"22 hf-* + using-hf-workflow"应为"21 hf-* + using-hf-workflow = 22 skills"）
  - architecture-designer = 1，ui-ux-pro-max = 1，writing-skills = 1，write-blog = 4（4 子 skill）= 7
  - garage 扩张后 = 4（garage-hello + find-skills + vision-obey + writing-docs）
  - **总计 = 22 + 7 + 4 = 33 个 SKILL.md**，不是 30
  - "30 个 top-level 入口"是当前 `.agents/skills/` 顶层 entry 数（8 dir + 22 symlink），与"安装到下游的 unique SKILL.md 数"不是同一概念
  - 后果：FR-805 验收 marker `Installed 30 skills, 1 agents into hosts: claude` 是不可达字面值（实际安装应为 33）；FR-807 验收 #3 "Inventory 表 6 行的 skill 数 列加总 = 30" 也不可达
  - 属 USER-INPUT，因为牵涉用户对"是否将 write-blog 4 子 skill 与 vendored 单 skill pack 都计入下游分发清单"的范围裁决——若用户同意 33 → spec 数字全替换 + FR-804 顶层 symlink 数量也要重核（顶层 30 + 3 新 symlink = 33？还是只让 22 个 hf-* + using-hf-workflow + 8 个非 hf 顶层 = 30 不变，write-blog 子 skill 不挂顶层符号？需明示）；若用户希望保持 30 上限 → 必须显式声明哪 3 个 SKILL.md 不参与下游分发（违背 manifesto"几秒变成你的 Agent"承诺力度）

- **[important][USER-INPUT][C7][A5] F-3: pack.json `upstream.source` 必填 vs OQ-801 / OQ-804 中 `null` / `"unknown"` 取值不一致，且 LICENSE 合规问题被错误归为非阻塞。** FR-801 字段定义为 `upstream: { source: string, rev: string, sync_method?: string }`（string 暗示非空），但 § 4.1 与 OQ-801 允许 `source` 取 `null` / `"unknown"`，与 FR-801 schema 字面冲突。更关键：OQ-804（vendored LICENSE attribution）被标"非阻塞"。现实：`packs/write-blog/LICENSE` 是 MIT，其条款明文要求 `The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software`。F007 安装管道仅复制 SKILL.md / agent.md，不复制 LICENSE，下游 `.claude/skills/blog-writing/SKILL.md` 因此构成"分发副本却不携带 license"。这是真实法务约束（MIT / Anthropic 文档版权 / `architecture-designer` license），**应作为本 cycle 阻塞性 OQ 而不是 deferred**。属 USER-INPUT：用户需明示 (a) `pack.json.upstream.source` schema 是否允许 null（影响 FR-801 wording 与 ASM 增补），(b) 是否本 cycle 增加最小 license attribution 机制（如 SKILL.md front matter 注入 `license: ...`、`upstream_url: ...` + 用户文档段说明 license 文件分发策略），还是接受现状的法务风险并明文记录该选择。

- **[important][LLM-FIXABLE][A2/G2] F-4: FR-803 把"5 个 vendored pack 整体 `git mv` + 各自新建 `pack.json` + 各自新建 `README.md`"打包为 1 条 FR，命中 GS2/GS4。** 5 个 pack 的迁移在 (a) 是否需要插入 `skills/` 中间层（架构）、(b) 是否含 LICENSE（法务）、(c) upstream URL 是否已知（事实）三个维度上行为各异。建议拆为：FR-803a（vendored pack `git mv` 落地）+ FR-803b（每个 vendored pack 新建 `pack.json` 含 upstream + license）+ FR-803c（每个 vendored pack 新建 `README.md`），让 task 拆分时 traceability 更准。LLM-FIXABLE：拆分不会改变范围 / 优先级 / 边界。

- **[important][LLM-FIXABLE][C2/C5] F-5: CON-805 "F001 CON-002 修订" 把动作落到"本 cycle finalize 阶段"，但 finalize 节点按 hf-finalize 是状态收尾，不是 spec 修订。** 修订一份已批准 spec 的标准动作是 `hf-increment` 或在本 cycle 内显式产出 F001 patch artifact。spec 应明示 (a) F001 CON-002 修订在本 cycle 哪一阶段产出、产物路径在哪（如 `docs/features/F001-...md` 直接 in-place 修订、或 `docs/decisions/F008-supersedes-F001-CON002.md` 这样的 ADR），(b) 是否需要 F001 spec re-approval。LLM-FIXABLE：选择落点 + 改 1 段 wording。

### Minor

- **[minor][LLM-FIXABLE][Q2/A1] F-6: § 4.1 表"`pack.json.upstream.source` 暂填 `null` 或 `"unknown"`，附 `note` 字段说明"中 `note` 字段在 FR-801 schema 中未定义。** 要么把 `note` 也加入 FR-801 schema 字段表（可选 string），要么改用现有可选 `description` 字段承载备注。

- **[minor][LLM-FIXABLE][A6] F-7: FR-804 验收缺"symlink target 实际可解析"的负路径覆盖。** 当前验收只覆盖 `mode == 120000` 与 follow 后内容字节一致；建议增加 `Given 任意 .agents/skills/<id>，When 通过 readlink 解析其 target，Then target 必须是合法相对路径且对应 packs/ 路径下文件实际存在`（防止 dangling symlink 通过 git ls-tree 检查但 cursor 加载失败）。

- **[minor][LLM-FIXABLE][C7] F-8: ASM-803 (cursor 跟随 symlink) 是 dogfood 是否成立的关键假设，但失效缓解只说"hf-test-driven-dev 阶段端到端验证"。** 应再补一条 design 阶段先做的最小实证（如：在 author 的本机 cursor 内手工创建 1 个 symlink → SKILL.md 验证 cursor 索引行为），把假设失效风险尽早暴露，否则等到 hf-test-driven-dev 才发现 cursor 不 follow 会导致整个 NFR-801 / CON-804 推倒重来。

- **[minor][LLM-FIXABLE][Q3] F-9: harness-flow 内 `docs/` `templates/` 子目录、write-blog `prompts/`、ui-ux-pro-max `data/` `scripts/`、writing-skills `examples/` `render-graphs.js` `anthropic-best-practices.md` 等 vendored 内非 SKILL.md 资产，spec 没有显式声明 "随 pack 落 packs/ 但不被 garage init 物化到下游"。** 建议在 § 4.2 增 1 行边界 / 或在 NFR-804 增 1 句"vendored 内非 SKILL.md / agent.md 资产作为 pack-internal 资产保留在仓库内，但 F007 安装管道按既有契约只物化 SKILL.md + agent.md，不物化这些资产"，避免 design / tasks 阶段误认为要扩 F007 安装管道。

- **[minor][LLM-FIXABLE][C2] F-10: § 2.2 成功标准 #2 中 "`files[]` 长度必须 = 30 SKILL.md + 1 sample agent + 任何被 install 的 pack-internal 资产"和 F-9 互相牵扯。** 由于 F007 安装管道不物化 pack-internal 资产（FR-704 明确仅 skill+agent surface），"+ 任何被 install 的 pack-internal 资产" 这条加法项要么删除、要么明确为 0。

## 缺失或薄弱项

- F-1 阻塞性架构冲突 spec 未识别，导致整份 spec 内部 F007 契约 / vendored 不变量 / Python 零修改三个 Must 项之间存在不可调和矛盾，必须由用户裁决一种取舍方向后再回写。
- 数量与 wording 一致性（F-2、F-6、F-10）需要全文一次性同步，否则下游 task 拆分会沿用错误数字产生连锁错误。
- 法务 / license 风险（F-3 一部分）spec 选择 deferred 但实际是分发动作触发的当下行为，归类需复议。
- F008 影响 F001 CON-002 的 cross-spec 修订机制（F-5）需要在本 cycle 内闭合，否则两份 spec 间留下"已知矛盾"挂账。

## 下一步

`hf-specify`（按 F-1 用户裁决结果回修 FR-803 / NFR-803 / NFR-804 / CON-802 / CON-803；同步修复 F-2 数量、F-3 schema/license、F-4 拆分、F-5 落点、F-6~F-10 wording）

## 记录位置

`docs/reviews/spec-review-F008-vendored-pack-contract-and-first-migration.md`

## 交接说明

- 结论 `需修改`，**不**进入"规格真人确认"
- F-1 是 USER-INPUT 阻塞，需父会话向用户最小化提问 1 题（vendored pack 内 `skills/` 中间层取舍三选一）
- F-2 是 USER-INPUT，需父会话向用户提问 2 题（unique SKILL.md 总数 33 vs 30 的取舍 + 数字确认）
- F-3 是 USER-INPUT，需父会话向用户提问 1 题（pack.json upstream.source 是否允许 null + 是否本 cycle 处理 license attribution）
- 其余 F-4 ~ F-10 是 LLM-FIXABLE，由 `hf-specify` 直接修订，不应转嫁给用户
- precheck 与正式 rubric 均完成；不需要 reroute via router

## 结构化返回

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-specify",
  "record_path": "docs/reviews/spec-review-F008-vendored-pack-contract-and-first-migration.md",
  "key_findings": [
    "[critical][USER-INPUT][C2] F-1 vendored 字节零修改 / F007 pack_discovery 契约 / F007 Python 零修改 三者冲突，spec 未识别",
    "[important][USER-INPUT][Q3] F-2 30 SKILL.md 数量不符实测（实际 33），多处验收 marker 不可达",
    "[important][USER-INPUT][C7] F-3 pack.json upstream.source 可空与 FR-801 schema 冲突；OQ-804 license 合规被错误归为非阻塞",
    "[important][LLM-FIXABLE][A2] F-4 FR-803 复合需求需拆 a/b/c",
    "[important][LLM-FIXABLE][C2] F-5 CON-805 把 F001 修订落到 finalize 阶段错节点",
    "[minor][LLM-FIXABLE][Q2] F-6 § 4.1 note 字段 schema 未定义",
    "[minor][LLM-FIXABLE][A6] F-7 FR-804 缺 dangling symlink 负路径",
    "[minor][LLM-FIXABLE][C7] F-8 ASM-803 cursor follow symlink 缺 design 阶段最小实证",
    "[minor][LLM-FIXABLE][Q3] F-9 vendored 内非 SKILL.md 资产分发边界未显式声明",
    "[minor][LLM-FIXABLE][C2] F-10 § 2.2 #2 'files[] 长度 + pack-internal 资产' 加法项与 F007 安装语义矛盾"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {"severity": "critical", "classification": "USER-INPUT", "rule_id": "C2", "summary": "vendored 字节零修改 vs F007 pack_discovery 契约 vs F007 Python 零修改 三者冲突 spec 未识别"},
    {"severity": "important", "classification": "USER-INPUT", "rule_id": "Q3", "summary": "30 SKILL.md 数量不符实测（实际 33）"},
    {"severity": "important", "classification": "USER-INPUT", "rule_id": "C7", "summary": "upstream.source 可空 schema 冲突 + license 合规误归为非阻塞"},
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "A2", "summary": "FR-803 复合需求需拆 a/b/c"},
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "C2", "summary": "CON-805 F001 修订落到 finalize 错节点"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "Q2", "summary": "§4.1 note 字段未在 FR-801 schema 定义"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "A6", "summary": "FR-804 缺 dangling symlink 负路径"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "C7", "summary": "ASM-803 缺 design 阶段最小实证"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "Q3", "summary": "vendored 内非 SKILL.md 资产分发边界未声明"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "C2", "summary": "§2.2 #2 files[] 加法项与 F007 安装语义矛盾"}
  ]
}
```
