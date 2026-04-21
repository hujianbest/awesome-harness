# Task Progress

## Goal

- Goal: F008 — Vendored Pack 契约 + 首批迁移（5 vendored pack + 3 first-party skill 落 `packs/`，`.agents/skills/` 改为 symlink 投影层）
- Owner: hujianbest
- Status: 🟡 Active — `hf-specify` 草稿已完成（492 行，10 FR + 7 NFR + 5 CON + 4 ASM + 4 OQ + 45 G/W/T 验收），下一步派发 `hf-spec-review`
- Last Updated: 2026-04-21

## Previous Milestones

- F001 Phase 1: ✅ 完成（T1-T22，416 测试通过）
- F002 Garage Live: ✅ 完成（CLI + 真实 Claude Code 集成，436 测试通过）
- F003 Garage Memory: ✅ 完成（T1-T9，384 测试通过）
- F004 Garage Memory v1.1: ✅ 完成（T1-T5，414 测试通过）
- F005 Garage Knowledge Authoring CLI: ✅ 完成（T1-T6，451 测试通过）
- F006 Garage Recall & Knowledge Graph: ✅ 完成（T1-T5，496 测试通过；workflow closeout 见 `docs/verification/F006-finalize-closeout-pack.md`）
- F007 Garage Packs 与宿主安装器: ✅ 完成（T1-T5，586 测试通过；workflow closeout 见 `docs/verification/F007-finalize-closeout-pack.md`）

## Current Workflow State

- Current Stage: `hf-specify`（草稿已落盘 `docs/features/F008-vendored-pack-contract-and-first-migration.md`；待派发 `hf-spec-review`）
- Workflow Profile: `full`（router 决定：无已批准 F008 规格 + cross-module 影响 packs/ + .agents/skills/ + AGENTS.md + skill-anatomy.md + dogfood 链路 → 命中 full 信号矩阵）
- Execution Mode: `interactive`（用户未声明；AGENTS.md 无默认；fallback default = interactive；spec 起草是高 impact 决策保留人工 approval window）
- Workspace Isolation: `in-place`（当前在 hf-specify 纯文档阶段；进入 hf-test-driven-dev 时 router 重新评估升级到 worktree-required）
- UI Surface（4A）: 不激活（packs 文件搬迁 + adapter 路径配置，纯 infra / file-system，无前端 / 页面 / 组件 / a11y / 响应式信号）→ design stage 只走 hf-design 单节点
- Current Active Task: 无（任务未拆分；待 hf-tasks 后建立）
- Pending Reviews And Gates: 无
- Next Action Or Recommended Skill: `hf-spec-review`（reviewer subagent，按 reviewer-handoff 协议派发；返回后由 hf-workflow-router 按 full profile 迁移表决定下一步）
- Relevant Files:
  - `docs/features/F008-vendored-pack-contract-and-first-migration.md`（本 cycle 草稿规格，待 hf-spec-review）
  - `docs/features/F007-garage-packs-and-host-installer.md`（已批准 F007 规格，F008 直接复用其安装管道、pack.json schema、manifest schema、conflict 检测）
  - `docs/soul/manifesto.md`、`user-pact.md`、`growth-strategy.md`、`design-principles.md`（项目灵魂，F008 价值锚点）
  - `packs/README.md`、`packs/garage/pack.json`（F007 已落 pack 容器契约，F008 扩 garage 为 4 skill + 增 5 vendored pack）
  - `.agents/skills/`（5 vendored pack + 3 first-party skill 搬迁源；将改造为 symlink 投影层）
  - `AGENTS.md`（路径引用 + 新增 Packs Inventory 子段）
  - `docs/principles/skill-anatomy.md`（skill 写作原则；可能含 .agents/skills/ 路径引用待更新）
  - `skills-lock.json`（vendored pack lock 信息）
  - `RELEASE_NOTES.md`（F007 条目已显式列 F008 候选；本 cycle 完成后增 F008 条目）
- Constraints:
  - Stage 2 仍保持 workspace-first，不引入外部数据库、常驻服务、Web UI
  - 优先使用 markdown、JSON、文件系统存储
  - 所有数据存储在 Garage 仓库内部
  - F007 已确立的 packs/ 容器契约 + 安装管道不可破坏（NFR：本 cycle 不动 .garage/config/host-installer.json schema、不动 HostInstallAdapter Protocol）
  - `packs/` 内禁止出现宿主特定术语（继承 F007 NFR-701 grep 测试；新增 packs/coding/ packs/writing/ 自动纳入守护范围）

## Next Step

hf-specify 已完成 Step 4-8，草稿落盘。下一步：

1. 派发 `hf-spec-review` reviewer subagent（独立 subagent，按 reviewer-handoff 协议）
2. 消费 reviewer 返回结构化 summary
3. 由 hf-workflow-router 按 full profile 迁移表决定下一节点：
   - 通过 → 规格真人确认（interactive 暂停点）
   - 需修改 / 阻塞 → 回 `hf-specify` 修订
   - 阻塞需重编排 → 回 `hf-workflow-router`

## hf-specify Step 1 审计的关键发现（事实校正记录）

启动时假设"30 个独立 HF skill 可机械搬到 packs/coding/"被审计推翻，真实情况是：
- **5 个 vendored pack**（harness-flow / architecture-designer / write-blog / ui-ux-pro-max / writing-skills，含 27 个 SKILL.md）
- **3 个 first-party skill**（find-skills / vision-obey / writing-docs）
- **22 个顶层 hf-* + using-hf-workflow 是 git symlink**，指向 harness-flow/skills/

→ F008 范围由"机械搬运"修订为"vendored pack 契约扩展 + 首批迁移"，spec 已按此修订形态落地。

## 已收尾候选 / 后续 cycle 候选（由后续 hf-workflow-router 独立判断）

- **F008 候选 — `.agents/skills/` 搬迁到 `packs/`**：✅ 已被本 cycle 拉入主链（见上方 Goal 段）
- **F009 候选 — `garage uninstall --hosts <list>` + `garage update --hosts <list>`**：F007 cycle 显式 deferred 的安装逆向操作 + 拉新流程；安装清单 manifest 已为这两条留好 entry point；F008 完成后下游用户拥有真实可 uninstall / update 的载荷，本候选价值才完整体现
- **单独候选 — 全局安装到 `~/.claude/skills/...`**（OpenSpec issue #752 模式）：solo creator 跨多客户仓库的需求；与 Garage workspace-first 信念有 trade-off，应单独 spec 化
- **F008+ 候选 — 新增宿主**（Codex / Gemini CLI / Windsurf / Copilot 等）：F007 已确立 first-class adapter 注册模式；新增宿主成本 = 1 个 adapter 子模块 + 注册表 1 行
- 处理 F006 finalize 中显式延后的 minor：`_recommend_experience` 多次累加语义对齐；CON-501/502/NFR-602 契约测试
- 处理 F006 § 5 deferred backlog：`garage knowledge unlink` / 多跳 graph / experience link / 跨类型 link / 图导出 / `recommend --format json`
- 处理 pre-existing baseline 的 1 个 mypy error（`_memory_review` line 562 on main）+ 47 个 ruff stylistic warnings（F002/F003/F004 历史；F007 已确认未新增）
- 评估是否启动 Stage 3（"工匠"）：进入信号 "知识库条目 >100" 与 "识别到 5+ 可复用模式" 仍依赖用户使用频率
- 详见 `RELEASE_NOTES.md` "F007 — 已知限制 / 后续工作" 段
