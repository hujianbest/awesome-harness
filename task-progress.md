# Task Progress

## Goal

- Goal: F009 — `garage init` 双 Scope 安装（project / user）+ 交互式 Scope 选择
- Owner: hujianbest
- Status: 🟡 In Progress — F009 6 个 task 全部 commit 落地（T1-T6），等待 manual smoke walkthrough + hf-test-review 链路
- Last Updated: 2026-04-23

## Previous Milestones

- F001 Phase 1: ✅ 完成（T1-T22，416 测试通过）
- F002 Garage Live: ✅ 完成（CLI + 真实 Claude Code 集成，436 测试通过）
- F003 Garage Memory: ✅ 完成（T1-T9，384 测试通过）
- F004 Garage Memory v1.1: ✅ 完成（T1-T5，414 测试通过）
- F005 Garage Knowledge Authoring CLI: ✅ 完成（T1-T6，451 测试通过）
- F006 Garage Recall & Knowledge Graph: ✅ 完成（T1-T5，496 测试通过；workflow closeout 见 `docs/verification/F006-finalize-closeout-pack.md`）
- F007 Garage Packs 与宿主安装器: ✅ 完成（T1-T5，586 测试通过；workflow closeout 见 `docs/verification/F007-finalize-closeout-pack.md`）
- F008 Garage Coding Pack 与 Writing Pack: ✅ 完成（T1a/T1b/T1c + T2 + T3 + T4a/T4b/T4c + T5，633 测试通过；workflow closeout 见 `docs/verification/F008-finalize-closeout-pack.md`）

## Current Workflow State

- Current Stage: `hf-test-review`（待派发，6 个 task 全部 commit 落地后）
- Workflow Profile: `full`
- Execution Mode: `auto`
- Workspace Isolation: `in-place`（工作分支 `cursor/f009-init-scope-selection-bf33`；PR #24）
- Current Active Task: 无（6/6 task commit 落地）
- Pending Reviews And Gates: `hf-test-review` → `hf-code-review` → `hf-traceability-review` → `hf-regression-gate` → `hf-completion-gate` → `hf-finalize`
- Next Action Or Recommended Skill: manual smoke walkthrough + `hf-test-review`
- Relevant Files:
  - `docs/features/F009-garage-init-scope-selection.md`（已批准 r2，10 FR + 4 NFR + 4 CON + 4 ASM）
  - `docs/designs/2026-04-23-garage-init-scope-selection-design.md`（已批准 r2，11 ADR + 6 task + 9 INV + 11 测试文件）
  - `docs/approvals/F009-{spec,design}-approval.md`（auto-mode approval records）
  - `docs/reviews/{spec,design}-review-F009-garage-init-scope-selection.md`（r1 需修改 + r2 通过）
  - `docs/tasks/2026-04-23-garage-init-scope-selection-tasks.md`（已批准 r3，6 个 task：T1 adapter / T2 pipeline / T3 manifest / T4 cli / T5 tests / T6 docs）
  - `docs/approvals/F009-tasks-approval.md`（auto-mode approval record）
  - `docs/reviews/tasks-review-F009-garage-init-scope-selection.md`（r1 → r2 → r3 通过）
  - `docs/soul/manifesto.md`、`user-pact.md`、`design-principles.md`、`growth-strategy.md`（价值锚点；本 cycle 与 workspace-first 信念有 trade-off，需显式评估）
  - F008 spec § 5 deferred backlog 第 3 行（"全局安装到 `~/.claude/skills/...`：solo creator 跨多客户仓库的需求"——本 cycle 即落地）
  - F007 安装管道 `src/garage_os/adapter/installer/{pack_discovery,pipeline,manifest,host_registry}.py` + 三家 adapter `hosts/{claude,opencode,cursor}.py`（F009 扩展点）
  - 调研锚点 3 家宿主官方 user scope path 文档（spec § 1）
- Constraints:
  - F002/F007/F008 既有 `garage init` 行为字节级不变（CON-901 + 沿用 CON-702）
  - D7 安装管道核心算法不动（CON-902，仅 phase 2 增 scope 分流）
  - 复用 F007 pack.json schema + F008 ADR-D8-9 EXEMPTION_LIST（CON-903）
  - manifest schema 1 → 2 migration 单向（CON-904）
  - 不改 packs/ 内容物
  - 不引入 enterprise / plugin scope（solo creator 用不到）

## Next Step

6/6 task commit 落地。下一步：

1. **Manual smoke walkthrough**（dogfood + tmp 双轨）：
   - dogfood: 在 Garage 仓库自身根目录跑 `garage init --hosts cursor,claude` 验证 NFR-901 Dogfood 不变性
   - tmp: 在 `/tmp/f009-smoke/` 跑 `garage init --hosts all --scope user` 验证 user scope 三家宿主全装
2. 派发 `hf-test-review` reviewer subagent
3. 派发 `hf-code-review` reviewer subagent
4. 派发 `hf-traceability-review` reviewer subagent
5. `hf-regression-gate`
6. `hf-completion-gate`
7. `hf-finalize`（用 manual smoke 实测填 RELEASE_NOTES F009 段 5 项 TBD + workflow closeout pack）

## 实施完成证据

- 测试基线: 633 (F008 baseline) → **708 passed** (+75 增量, 0 退绿)
- INV-F9-1..9 全部通过（design § 11.1，含 INV-F9-1 dogfood SHA-256 sentinel + INV-F9-7 manifest schema 2 + INV-F9-8 fixture-isolated）
- `git diff main..HEAD -- pyproject.toml uv.lock` 输出空（零依赖变更）
- `git diff main..HEAD -- src/garage_os/` 仅 installer + cli 改动（CON-901 + CON-902 严守）
- 6 sub-commit 分组提交（NFR-904 git diff 可审计）：T1 adapter / T2 pipeline / T3 manifest / T4 cli / T5 tests / T6 docs
- F009 总 11 个新增测试文件（含 baseline JSON fixture）+ 4 处 carry-forward wording 修复
