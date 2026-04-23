# Design Review — F008 Garage Coding Pack 与 Writing Pack

- 评审目标: `docs/designs/2026-04-22-garage-coding-pack-and-writing-pack-design.md`（草稿 r1）
- Reviewer: 独立 reviewer subagent（按 `hf-design-review` skill 执行）
- 评审时间: 2026-04-23
- 上游证据基线:
  - `task-progress.md`（Stage=`hf-design` / Profile=`full` / Mode=`auto` / Workspace=`in-place`）
  - `docs/features/F008-garage-coding-pack-and-writing-pack.md`（已批准 r2）
  - `docs/approvals/F008-spec-approval.md`（auto-mode approval record）
  - `docs/reviews/spec-review-F008-coding-pack-and-writing-pack.md`（r1 需修改 → r2 通过）
  - F007 已批准设计 + 实际管道代码 `src/garage_os/adapter/installer/{pack_discovery,pipeline}.py`
  - 仓库现状：`ls .agents/skills/harness-flow/skills/`、`ls packs/garage/`、`diff docs/principles/skill-anatomy.md .agents/skills/harness-flow/docs/principles/skill-anatomy.md`

## 结论

**需修改**

verdict 理由：D008 草稿基本面扎实——8 项 ADR 全部带候选对比与可逆性评估，§ 2.3 把 spec § 4.2 全部 6 条 "Design Reviewer 可拒红线" 逐条承接，§ 11.1 9 条 INV 不变量全部可被测试或 grep 验证，§ 10.1 五类提交分组对齐 spec NFR-804，§ 14 失败模式 F1-F7 显式枚举。可作为 `hf-tasks` 拆任务的输入方向是清晰的。

但发现 **1 条 important USER-INPUT 级 spec drift 风险（ADR-D8-4 实质性下调 spec 验收口径，需真人在 design 真人确认环节明确签署）** + **3 条 important LLM-FIXABLE 级 design 内部一致性 / readiness 缺口**（§ 13 测试策略与 § 12 NFR 落地行自相矛盾、§ 17 漏列 3 项 spec § 5 deferred、§ 10.1 T1/T4 commit 粒度偏大）+ **4 条 minor LLM-FIXABLE 级 改进点**。这些 finding 不构成 design 内核坍塌，预计 1 轮定向回修可全部闭合，因此判 `需修改` 而非 `阻塞`。

ADR-D8-4 那条 USER-INPUT 是 design 阶段对已批准 spec 硬验收（FR-804 #1 / § 2.2 #2 "装完后引用不 404"）的口径下调——design 已正确识别 CON-801（不动 D7 管道）与该 spec 验收之间不可调和的张力，并把"管道扩展"放到 D9 候选——但 spec 文字未变直接靠 design ADR "重述" acceptance，仍属合规边缘，必须在真人确认环节让用户对该口径下调签字背书。这种"design 主动暴露 spec 漏洞 + 提出 deferred 解法"是允许的，但不能由 design ADR 单方面重定义 spec 已写死的 acceptance 字眼。

## 6 维评分（内部）

| 维度 | 得分 | 主要观察 |
|---|---|---|
| D1 需求覆盖与追溯 | 7/10 | § 3 追溯表覆盖 FR/NFR/CON 全集；ADR-D8-4 对 spec FR-804/§2.2#2 实质性 reinterpretation；§ 17 漏列 spec § 5 deferred 3 项 |
| D2 架构一致性 | 8/10 | § 4 模式选择 / § 8 视图清晰；§ 11 模块边界明确；§ 8.4 端到端管道图 + § 8.4 注脚显式说明 family asset 不被复制是优秀做法 |
| D3 决策质量与 trade-offs | 8/10 | 8 项 ADR 全部带 ≥2 候选对比 + Consequences/Reversibility 段；ADR-D8-3 反向同步方向的"权威源选定"缺 git log 证据 |
| D4 约束与 NFR 适配 | 8/10 | § 12 NFR/CON 落地表完整；§ 11.1 INV 不变量映射到 commit 责任；CON-801 由 INV-5 明确守门 |
| D5 接口与任务规划准备度 | 6/10 | § 10.1 五类提交分组直接对应 NFR-804；T1 单 commit 含 ≥7 类动作（22 skill + 11 family asset + drift 反向同步 + pack.json + README + sentinel test）、T4 单 commit 含 4 类动作（rm -rf + .gitignore + AGENTS.md + 集成测试），与 NFR-804 "任一组改动可被独立 review" 的 spec 意图存在张力，hf-tasks 拿到后需要进一步拆分 |
| D6 测试准备度与隐藏假设 | 6/10 | § 13 测试策略与 § 12 NFR 落地表对"新增测试文件数量"陈述自相矛盾（§13 列 2 个 / §12 列 4 个）；§ 13.3 Walking Skeleton 仅覆盖 Claude Code 一家宿主；§ 18 非阻塞 #3 已识别 dogfood 产物的新贡献者发现性问题但未进入 ADR Consequences |

任一维度未低于 6/10，但 D5/D6 两个维度刚卡 6 分，对应到 important finding。

## 发现项

### Critical

无 critical 级 finding。

### Important

1. **[important][USER-INPUT][D1]** **ADR-D8-4 实质性下调 spec FR-804 验收 #1 / § 2.2 验收 #2 的 acceptance 字面口径**：
   - spec FR-804 验收 #1 明文写："Given F008 实施完成 + 任意一次 `garage init --hosts claude` 成功，When 任意 hf-* SKILL.md 内含 `references/spec-template.md` ... 形式相对引用，**Then 该相对路径在 `.claude/skills/` 加载入口下必须能 resolve 到磁盘存在的真实文件**" — 关键约束是"在 `.claude/skills/` 加载入口下"
   - spec § 2.2 验收 #2 同样明文："**装到 `.claude/skills/` 后**必须仍能 resolve 到磁盘存在的目标文件"
   - 实测 D7 管道 `pipeline._resolve_targets()` 只对 `<pack>/skills/<id>/SKILL.md` 单文件 read→inject→write，不递归 `references/`、`docs/`、`templates/` 任一子目录
   - 实测 hf-specify 等多个 SKILL.md 内大量引用 `references/spec-template.md` / `skills/docs/hf-workflow-shared-conventions.md` / `templates/task-progress-template.md` 等家族内文件 — 在 D7 当前管道下装到 `.claude/skills/hf-specify/` 后，这些引用全部 404
   - design ADR-D8-4 选定"文档级提示" — 把 spec 硬验收口径下调到"下游用户的 Garage 仓库 git checkout 是 references 真源；下游宿主的 SKILL.md 引用是文档级提示，而非加载时硬依赖"
   - design 选择是合理的（CON-801 / 红线 6 严禁动管道 → 短期内别无他法 + D9 候选作为长期解），但**spec 已批准的 acceptance 字眼未变**，由 design ADR 单方面重述硬验收的语义属于 spec drift 风险
   - **修复路径二选一**：
     - (a) 在 design 真人确认环节让用户对"spec FR-804 验收 #1 / § 2.2 验收 #2 的 '装完后不 404' 口径下调到 'packs/ 内不 404 + 下游为文档级提示'" 显式签字背书；ADR-D8-4 文末加一段"本决策需 spec 真人在 design 真人确认时签署 acceptance 重述"
     - (b) 回 `hf-increment` 修订 spec FR-804 验收 #1 / § 2.2 验收 #2 字面口径，删除"在 `.claude/skills/` 加载入口下" 约束，改为"在 packs/ 内可解析 + 下游引用是文档级提示"，spec 重新走 r3 review；这条更干净但显著拉长 cycle
   - **锚点**：design §2.4 (L67-83)、§7 ADR-D8-4 (L227-247)；spec FR-804 验收 #1 (L292)、§2.2 验收 #2 (L106)、§3.2 场景 3 (L155)；管道事实 `src/garage_os/adapter/installer/pipeline.py:252-298`（`_resolve_targets`）+ `pack_discovery.py:62-66`（`skill_source_path`）

2. **[important][LLM-FIXABLE][D6]** **§ 12 NFR-802 落地表与 § 13.1 自动化测试表对"新增测试文件数量"自相矛盾**：
   - § 12 NFR-802 落地行（L520）声明："新增 ≥ 4 个用例（test_full_packs_install / test_skill_anatomy_drift / test_packs_garage_extended / test_dogfood_layout）"，列 **4 个测试文件**
   - § 13.1 自动化测试表（L529-533）只列 **2 个测试文件**（`test_skill_anatomy_drift.py` + `test_full_packs_install.py`）
   - § 12 列出但 § 13 缺席的两个测试文件（`test_packs_garage_extended` / `test_dogfood_layout`）在 design 中无任何"测什么 / 触哪个 INV / 触哪个 spec FR/NFR" 的描述
   - hf-tasks 阶段拿到 design 后无法判断这两个测试究竟该覆盖什么 — 直接掉头回 design 或自由发挥都不优
   - **修复指引**：§ 13.1 表补两行（test_packs_garage_extended 触发 FR-803 验收 + INV-1 / test_dogfood_layout 触发 FR-805 验收 #2 + INV-7），或反向把 § 12 NFR-802 落地行精简到 § 13 的 2 个测试 + 显式说明"hf-tasks 阶段可按需再拆"
   - **锚点**：design § 12 (L520) vs § 13.1 (L529-533)；spec NFR-802 (L350-353)

3. **[important][LLM-FIXABLE][D5]** **§ 10.1 T1 / T4 commit 粒度偏大，不利于 NFR-804 git diff 可审计性的 spec 意图**：
   - T1 (coding) 单 commit 含：(a) 22 skill 子目录 cp -r (b) 4 docs cp -r (c) 5 templates cp -r (d) 2 principles cp -r (e) drift 反向同步覆盖根级 `docs/principles/skill-anatomy.md` (f) 写 `packs/coding/pack.json` (g) 写 `packs/coding/README.md` (h) 新增 `tests/adapter/installer/test_skill_anatomy_drift.py` —— 7+ 类异质动作
   - T4 (layout) 单 commit 含：(a) `rm -rf .agents/skills/`（涉及 28 source SKILL.md + 11 family asset 删除，git diff 行数极大）(b) 改 `.gitignore`（dogfood 产物排除）(c) 改 `AGENTS.md`（局部刷新）(d) 新增 `test_full_packs_install.py` —— 4 类异质动作 + 海量删除噪声
   - spec NFR-804 的 spec 意图（L370-371 注释）："实际允许 1 个或多个 commit/group，本 NFR 不强求数量，强求**可审计性**——任意一组改动可被独立 review"
   - T1 把"内容物搬运"与"drift 收敛"+"sentinel test 新增"合并 — drift 收敛是独立逻辑切片，应可被独立 review；T4 把"删 .agents/skills/" 与"集成测试新增" + "AGENTS.md 文档"合并 — 三者实质独立
   - 这条不阻塞 design 通过 hf-design-review，但应在 design § 10.1 显式注明拆分边界（T1a/T1b/T1c 子提交 + T4a/T4b 子提交），让 hf-tasks 阶段不必从头思考切片
   - **修复指引**：design § 10.1 把 T1 拆成 T1a (22 skill) / T1b (11 family asset + pack.json + README) / T1c (drift 反向同步 + sentinel test)；T4 拆成 T4a (rm -rf .agents/skills/ + .gitignore) / T4b (AGENTS.md 文档刷新) / T4c (test_full_packs_install + test_dogfood_layout)；或在 § 15 任务规划准备度段加一行"hf-tasks 拆分时建议在 T1/T4 内再切 sub-commit"
   - **锚点**：design § 10.1 (L426-460)、§ 15 (L568-575)；spec NFR-804 (L364-371)

4. **[important][LLM-FIXABLE][D1]** **§ 17 排除项漏列 spec § 5 deferred 中 3 项**：
   - spec § 5 共列 **12 项 deferred**（uninstall / update / 全局安装 / 新增宿主 / packs/product-insights / 改写 SKILL.md / 给 packs/coding/ 加新 hf-* skill / pack.json 新字段 / find-skills 真功能 / writing-skills render-graphs.js 可执行 / 多语言 i18n / 反向同步 user→packs）
   - design § 17 复述其中 8 项 + 自加 2 项（D7 管道扩展 / 下游 references 直接打开），合计 10 项；**漏掉 spec § 5 的**：
     - (a) "给 `packs/coding/` family 加新 hf-* skill"（spec § 5 row 7）
     - (b) "多语言 / i18n 版本（write-blog 仅中文）"（spec § 5 row 11）
     - (c) "反向同步：用户在 .claude/skills/ 改了之后回流到 packs/"（spec § 5 row 12）
   - 这 3 项 spec 已显式 deferred，design § 17 不复述会让 finalize 阶段缺归口 / 验证不齐 → spec § 5 与 design § 17 的 backlog 表无法形成完整集合等价
   - **修复指引**：design § 17 补这 3 行；统一标注延后到 D9 / Stage 3 / 单独 cycle
   - **锚点**：design § 17 (L592-606)、spec § 5 (L237-251)

### Minor

5. **[minor][LLM-FIXABLE][D2]** **ADR-D8-2 候选 C "首次 clone 贡献者发现性"风险未进入 ADR Consequences 显式承接**：
   - 候选 C 选定后，新贡献者 `git clone` 后必须先跑 `garage init --hosts cursor,claude` 才能在 IDE 看到 hf-* skill；`.gitignore` 排除 `.cursor/skills/` `.claude/skills/`
   - 实测当前 `.gitignore` 仅 22 行，加入 dogfood 排除后没有任何顶层文档说明"为什么 .cursor/skills/ 在 .gitignore 但 IDE 又依赖它"
   - design § 18 非阻塞 #3 已提及"新贡献者可能困惑，AGENTS.md 段落需明确说明"，但 ADR-D8-2 Consequences 段（L184-190）没把这条作为 trade-off 显式列入风险栏
   - 也未明确"首次 clone 后激活 IDE skill 加载"的指引该落 README.md 顶部、CONTRIBUTING.md、还是 AGENTS.md 哪一处（design 只说"AGENTS.md 增一段说明"）
   - **修复指引**：ADR-D8-2 Consequences 段加一行"⚠️ 新贡献者首次 clone 后 IDE 加载链是空的，必须先跑 `garage init --hosts cursor,claude` 激活；此 onboarding 步骤需落 [README/AGENTS/CONTRIBUTING] 顶部 - 由 hf-tasks T4 commit 选定"
   - **锚点**：design § 7 ADR-D8-2 Consequences (L184-190)、§ 8.2 (L356-361)、§ 18 #3 (L617)

6. **[minor][LLM-FIXABLE][D3]** **ADR-D8-3 把 family 副本（HF 术语）作为"权威源"但缺 git log/blame 证据支撑"更新版"判定**：
   - design § 7 ADR-D8-3 称 "取 family 副本（HF 术语，**更新版**）作为权威源"
   - 实测两份 diff 显示：family 副本（HF 术语）含 `skills/docs/` 旧路径，根级（AHE 术语 + `packs/coding/skills/docs/` 现代路径）反而更"面向 F008 落地后状态"
   - 哪一份是真"更新版"取决于 git log/blame 时间戳，design ADR 内未给证据
   - reverse-sync 方向选错的代价：丢失 `packs/coding/skills/docs/` 这种更准确的路径锚点；最终 sentinel 守门字节相等是干净的，但内容选哪份是实质决策
   - **修复指引**：ADR-D8-3 Compare 表"反向同步" 行内补一句 git log 证据（如 "`git log -1 --format=%aI -- .agents/skills/harness-flow/docs/principles/skill-anatomy.md` vs `git log -1 --format=%aI -- docs/principles/skill-anatomy.md`，前者更新于 YYYY-MM-DD，故选定为权威源"）；或承认两份都"半新半旧"且声明优先采用 HF 术语版的理由（如术语一致性更重要）
   - **锚点**：design § 7 ADR-D8-3 (L194-225)、实测 diff 显示 70 字节差与术语漂移

7. **[minor][LLM-FIXABLE][D5]** **ADR-D8-1 选定的 layout (`packs/coding/skills/{docs,templates}/` + `packs/coding/principles/`) 与 spec § 4.1 候选 A 措辞 (`packs/coding/{docs,templates,principles}/`) 略有偏差，未在 ADR 内显式解释**：
   - spec § 4.1 候选 A 写 "`packs/coding/{docs,templates,principles}/`"（三者并列于 packs/coding 顶层）
   - design 选定 "`packs/coding/skills/{docs,templates}/` + `packs/coding/principles/`"（docs/templates 在 skills/ 子目录、principles 在 packs/coding 顶层）— 是 1:1 对齐现有 `harness-flow/skills/docs/` `harness-flow/skills/templates/` 的合理选择，且与现有 6 处 `skills/docs/<file>` 引用直接对齐（design ADR-D8-1 优点行已提及）
   - 但 design ADR-D8-1 没显式解释"为什么 docs/templates 落 skills/ 子目录而 principles 不落 skills/" 的非对称——两者都是 family-level shared asset，layout 不对称应有理由（猜测：principles 不被任何 hf-* skill 引用，只被 AGENTS.md 引用，所以独立顶层；但 ADR 内未写）
   - hf-tasks 阶段可能因这条非对称重新纠结
   - **修复指引**：ADR-D8-1 Decision 段后补一句"为什么 principles 不落 skills/"
   - **锚点**：spec § 4.1 (L184-185)、design § 7 ADR-D8-1 (L146-169)、§ 8.1 (L313-334)

8. **[minor][LLM-FIXABLE][D5]** **§ 13.3 最薄端到端验证路径仅覆盖 Claude Code 一家宿主**，与 FR-806 / ADR-D8-2 三家宿主全装承诺不对等：
   - FR-806 验收 #2 要求"三家宿主目录下 `*/skills/` 子目录数合计 == `N × 3`"
   - § 13.3 Walking Skeleton 只展示 `源 packs/coding/skills/hf-specify/SKILL.md → install_packs() → .claude/skills/hf-specify/SKILL.md → Claude Code skill loader → invoke`
   - cursor / opencode 两家宿主的端到端路径未在 Walking Skeleton 中展示——dogfood smoke 与 manual smoke 都跑三家，但"最薄验证路径"只展示一家弱化了证据完整性
   - **修复指引**：§ 13.3 补充至少展示 cursor 一家（含 `.cursor/skills/hf-specify/SKILL.md` 加载验证），或在路径末尾注明"同样路径适用于 cursor / opencode 仅 install 路径不同"
   - **锚点**：design § 13.3 (L543-554)、FR-806 验收 #2 (L316)

## 缺失或薄弱项

1. **ADR-D8-4 spec acceptance 口径下调缺真人签署机制**（important #1）。design 已正确识别 spec FR-804 / § 2.2 #2 与 CON-801 不可调和，但单方面 reinterpret 已批准 spec 的 acceptance 字面，需要在 design 真人确认环节明确签署该 reinterpretation。
2. **§ 12 NFR 落地与 § 13 测试策略对"新增测试数量"自相矛盾**（important #2）。两处对 4 vs 2 个测试文件的陈述不一致，hf-tasks 阶段无法判断该写多少个测试文件。
3. **§ 10.1 commit 粒度偏大**（important #3）。T1/T4 单 commit 异质动作过多，与 NFR-804 "任一组可独立 review" 意图存在张力，hf-tasks 阶段需要进一步拆分。
4. **§ 17 排除项漏 3 项 spec § 5 deferred**（important #4）。finalize 阶段无法形成完整 backlog 集合等价。
5. **首次 clone 贡献者 IDE 加载链空窗未在 ADR-D8-2 Consequences 显式承接**（minor #5）。
6. **ADR-D8-3 权威源选定缺 git log 证据**（minor #6）。
7. **ADR-D8-1 docs/templates vs principles layout 非对称未解释**（minor #7）。
8. **Walking Skeleton 仅覆盖一家宿主**（minor #8）。

## 下一步

`hf-design`（按本 review 的 1 important USER-INPUT + 3 important LLM-FIXABLE + 4 minor LLM-FIXABLE 做 1 轮定向回修）

回修优先级建议：
- **最先回修 important #1（ADR-D8-4 USER-INPUT）**：design 文档内显式声明"本 ADR 需 spec 真人在 design 真人确认时签署 acceptance 重述"；或父会话决定走 `hf-increment` 修订 spec FR-804 / § 2.2 #2 字面口径；二选一。**这条是本 review 的最重风险**，必须在进入 design 真人确认前关闭路径
- **接着回修 important #2-#4 LLM-FIXABLE**：§ 13/§ 12 测试数量对齐、§ 10.1 commit 拆分边界注明、§ 17 补齐 3 项 deferred；都是机械性 wording 调整，不需要新业务输入
- **最后回修 4 条 minor**：ADR Consequences 补充 / git log 证据 / layout 非对称解释 / Walking Skeleton 补宿主

回修期间不需要向真人提任何 USER-INPUT 问题，**仅 important #1 在回修后进入 design 真人确认时由真人签署 acceptance 重述**。

## 记录位置

`docs/reviews/design-review-F008-coding-pack-and-writing-pack.md`

## 交接说明

- `设计真人确认`：本轮 verdict = `需修改`，**不进入**
- `hf-design`：父会话应把本 review 记录路径与 1 important USER-INPUT + 3 important LLM-FIXABLE + 4 minor LLM-FIXABLE 全部回传给 design 起草会话；预计 1 轮定向回修 + 1 轮 design-review 即可冻结进入 design 真人确认
- `hf-workflow-router`：route / stage / 证据无冲突，不需要 reroute（`reroute_via_router=false`）
- `hf-tasks`：未到拆任务阶段，不进入
- `hf-increment`：仅当父会话或 design 起草会话判断 important #1 选 (b) 路径（修订 spec 字面口径而非 design 内 reinterpret）时，才走 `hf-increment` 改 spec
- 不修改 `task-progress.md`、不修改 F008 spec 文档、不修改 D008 design 文档、不 git commit / push（由父会话执行）

---

## 结构化返回（JSON 摘要）

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-design",
  "record_path": "docs/reviews/design-review-F008-coding-pack-and-writing-pack.md",
  "key_findings": [
    "[important][USER-INPUT][D1] ADR-D8-4 实质性下调 spec FR-804 验收 #1 / § 2.2 验收 #2 '装完后引用不 404' 的 acceptance 字面口径，需真人在 design 真人确认环节签署 acceptance 重述或回 hf-increment 改 spec",
    "[important][LLM-FIXABLE][D6] § 12 NFR-802 落地行列 4 个新增测试文件 vs § 13.1 自动化测试表只列 2 个，hf-tasks 阶段无法判断该写多少",
    "[important][LLM-FIXABLE][D5] § 10.1 T1 单 commit 含 7+ 类异质动作 / T4 含 4 类，与 NFR-804 '任一组可独立 review' spec 意图张力",
    "[important][LLM-FIXABLE][D1] § 17 排除项漏列 spec § 5 deferred 3 项（新增 hf-* skill / i18n / 反向同步 user→packs）",
    "[minor][LLM-FIXABLE][D2] ADR-D8-2 候选 C 首次 clone 贡献者 IDE 加载链空窗未在 ADR Consequences 显式承接"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "important",
      "classification": "USER-INPUT",
      "rule_id": "D1",
      "summary": "ADR-D8-4 实质性下调 spec FR-804 验收 #1 / § 2.2 验收 #2 '装完后引用不 404' 字面口径；spec 已批准但 design ADR 单方面重述硬验收语义，需真人在 design 真人确认时签署或回 hf-increment 改 spec"
    },
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "D6",
      "summary": "§ 12 NFR-802 落地行 vs § 13.1 自动化测试表对'新增测试文件数量'自相矛盾（4 vs 2），且 § 12 列出的 test_packs_garage_extended / test_dogfood_layout 在 § 13 无任何描述"
    },
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "D5",
      "summary": "§ 10.1 T1 单 commit 含 22 skill + 11 family asset + drift 反向同步 + pack.json + README + sentinel test 7+ 类异质动作；T4 含 rm -rf + .gitignore + AGENTS.md + 集成测试 4 类，与 spec NFR-804 '任一组可独立 review' 意图张力"
    },
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "D1",
      "summary": "§ 17 排除项漏列 spec § 5 deferred 中 3 项（给 packs/coding/ 加新 hf-* skill / 多语言 i18n / 反向同步 user→packs），finalize 阶段无法形成完整 backlog 集合等价"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "D2",
      "summary": "ADR-D8-2 候选 C Consequences 段未把'首次 clone 贡献者必须先跑 garage init 才能加载 IDE skill'列为已知 trade-off + 未明确 onboarding 指引落 README/AGENTS/CONTRIBUTING 哪一处"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "D3",
      "summary": "ADR-D8-3 称 family 副本是'更新版'但缺 git log/blame 证据；reverse-sync 方向选错可能丢失根级副本的 packs/coding/skills/docs/ 现代路径锚点"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "D5",
      "summary": "ADR-D8-1 选定 packs/coding/skills/{docs,templates}/ + packs/coding/principles/ 与 spec § 4.1 候选 A (packs/coding/{docs,templates,principles}/) 偏差，docs/templates vs principles 非对称未在 ADR 内显式解释"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "D5",
      "summary": "§ 13.3 最薄端到端验证路径仅覆盖 Claude Code 一家宿主，cursor/opencode 路径未展示；FR-806 三家宿主全装承诺与最薄路径展示不对等"
    }
  ]
}
```
