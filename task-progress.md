# Task Progress

## Goal

- Goal: F008 — Garage Coding Pack 与 Writing Pack（把 `.agents/skills/` 物化为可分发 packs）
- Owner: hujianbest
- Status: 🟡 In Progress — F008 spec drafted, awaiting `hf-spec-review`
- Last Updated: 2026-04-22

## Previous Milestones

- F001 Phase 1: ✅ 完成（T1-T22，416 测试通过）
- F002 Garage Live: ✅ 完成（CLI + 真实 Claude Code 集成，436 测试通过）
- F003 Garage Memory: ✅ 完成（T1-T9，384 测试通过）
- F004 Garage Memory v1.1: ✅ 完成（T1-T5，414 测试通过）
- F005 Garage Knowledge Authoring CLI: ✅ 完成（T1-T6，451 测试通过）
- F006 Garage Recall & Knowledge Graph: ✅ 完成（T1-T5，496 测试通过；workflow closeout 见 `docs/verification/F006-finalize-closeout-pack.md`）
- F007 Garage Packs 与宿主安装器: ✅ 完成（T1-T5，586 测试通过；workflow closeout 见 `docs/verification/F007-finalize-closeout-pack.md`）

## Current Workflow State

- Current Stage: `hf-specify`
- Workflow Profile: `full`
- Execution Mode: `auto`
- Workspace Isolation: `in-place`（工作分支 `cursor/f008-coding-pack-and-writing-pack-bf33`）
- Current Active Task: 无（spec drafting 阶段，task plan 由 `hf-tasks` 在 design 通过后产出）
- Pending Reviews And Gates: `hf-spec-review`（待派发）
- Next Action Or Recommended Skill: `hf-spec-review`
- Relevant Files:
  - `docs/features/F008-garage-coding-pack-and-writing-pack.md`（草稿）
  - `docs/soul/manifesto.md`、`growth-strategy.md`、`design-principles.md`（愿景锚点）
  - `packs/README.md`、`packs/garage/`（F007 落下的现状）
  - `.agents/skills/harness-flow/`、`.agents/skills/write-blog/`、`.agents/skills/find-skills/`、`.agents/skills/writing-skills/`（搬迁源）
  - `RELEASE_NOTES.md` § "F007 — 已知限制 / 后续工作"（F008 候选清单来源）
- Constraints:
  - 不修改 F007 安装管道 / `pack.json` schema / host adapter 注册表
  - 搬迁是字节级 1:1（仅相对引用路径允许最小修复）
  - `.agents/skills/` 处置必须本 cycle 收敛（A/B/C 候选由 design 决定）
  - Stage 2 仍保持 workspace-first，不引入外部数据库 / 常驻服务 / Web UI

## Next Step

派发独立 reviewer subagent 执行 `hf-spec-review`，对 `docs/features/F008-garage-coding-pack-and-writing-pack.md` 出 verdict。

下一节点候选（由 spec-review 结果决定）：
- 通过 → `hf-design`（含 § 4 family-level 资产物理位置 + `.agents/skills/` 处置三个候选的 ADR 收敛）
- 需修改 → 回 `hf-specify` 按 review findings 修订
- 阻塞 → 回 `hf-workflow-router` 重新判定 scope
