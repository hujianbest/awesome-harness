# Task Progress

## Goal

- Goal: F008 — `.agents/skills/` 30 个 HF skills 搬迁到 `packs/<pack-id>/skills/`（让 manifesto"挂载 Garage 几秒变成你的 Agent"承诺第一次有真实载荷）
- Owner: hujianbest
- Status: 🟡 Active — `hf-specify` 阻塞于范围边界 6 问待用户确认（Q1 pack 拆分粒度 / Q2 .agents/skills 是否保留 / Q3 dogfood / Q4 pack.json schema / Q5 AGENTS.md Packs Inventory / Q6 references 子目录搬迁）
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

- Current Stage: `hf-specify`（阻塞于 6 个范围边界问题待用户确认；spec 草稿正文未起草）
- Workflow Profile: `full`（router 决定：无已批准 F008 规格 + cross-module 影响 packs/ + .agents/skills/ + AGENTS.md + skill-anatomy.md + dogfood 链路 → 命中 full 信号矩阵）
- Execution Mode: `interactive`（用户未声明；AGENTS.md 无默认；fallback default = interactive；spec 起草是高 impact 决策保留人工 approval window）
- Workspace Isolation: `in-place`（当前在 hf-specify 纯文档阶段；进入 hf-test-driven-dev 时 router 重新评估升级到 worktree-required）
- UI Surface（4A）: 不激活（packs 文件搬迁 + adapter 路径配置，纯 infra / file-system，无前端 / 页面 / 组件 / a11y / 响应式信号）→ design stage 只走 hf-design 单节点
- Current Active Task: 无（任务未拆分；待 hf-tasks 后建立）
- Pending Reviews And Gates: 无
- Next Action Or Recommended Skill: `hf-specify`（阻塞中：等待用户对 Q1-Q6 6 问回应后继续 step 4 起草需求 rows）
- Relevant Files:
  - `docs/features/F007-garage-packs-and-host-installer.md`（已批准 F007 规格，F008 直接依赖其安装管道）
  - `docs/soul/manifesto.md`、`user-pact.md`、`growth-strategy.md`、`design-principles.md`（项目灵魂，F008 价值锚点）
  - `packs/README.md`、`packs/garage/pack.json`（F007 已落 pack 容器契约，F008 增加 packs/coding/、packs/writing/）
  - `.agents/skills/`（30 个 HF skills 搬迁源目录）
  - `AGENTS.md`（路径引用 + Packs & Host Installer 段需更新）
  - `docs/principles/skill-anatomy.md`（skill 写作原则；可能含 .agents/skills/ 路径引用待更新）
  - `RELEASE_NOTES.md`（F007 条目已显式列 F008 候选；本 cycle 完成后增 F008 条目）
- Constraints:
  - Stage 2 仍保持 workspace-first，不引入外部数据库、常驻服务、Web UI
  - 优先使用 markdown、JSON、文件系统存储
  - 所有数据存储在 Garage 仓库内部
  - F007 已确立的 packs/ 容器契约 + 安装管道不可破坏（NFR：本 cycle 不动 .garage/config/host-installer.json schema、不动 HostInstallAdapter Protocol）
  - `packs/` 内禁止出现宿主特定术语（继承 F007 NFR-701 grep 测试；新增 packs/coding/ packs/writing/ 自动纳入守护范围）

## Next Step

`hf-specify` 阻塞于 6 个范围边界问题待用户确认（详见会话历史本轮 router → hf-specify 转入消息）：

- Q1：pack 拆分粒度（A=3-pack [coding+writing] / B=2-pack / C=1-pack [全塞 garage]）— 默认 A
- Q2：搬迁后是否删除 `.agents/skills/`（默认是，强制 dogfood）
- Q3：本 cycle 是否实际把 packs 装到 Garage 仓库自身的 `.cursor/skills/` + `.claude/skills/`（默认是，作为 NFR + 验收）
- Q4：`pack.json` 是否新增字段（默认不变 schema_version=1）
- Q5：AGENTS.md 是否新增 `## Packs Inventory` 子段（默认是）
- Q6：`hf-*` skills 的 `references/` 子目录是否随主 SKILL.md 一起搬迁（默认是，整体搬迁）

用户回应后，hf-specify 进入 step 4-8（需求 rows + 起草 + 自检），然后 step 9 派发 `hf-spec-review`。

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
