# Approval Record - F009 Design

- Artifact: `docs/designs/2026-04-23-garage-init-scope-selection-design.md`
- Approval Type: `designApproval`
- Approver: cursor cloud agent (auto-mode policy approver)
- Date: 2026-04-23
- Workflow Profile / Execution Mode: `full` / `auto`
- Workspace Isolation: `in-place`（PR #24）

## Evidence

- **Round 1 review**: `docs/reviews/design-review-F009-garage-init-scope-selection.md`（R1） — `需修改`
  - 0 critical / 2 important + 7 minor，全 LLM-FIXABLE，0 USER-INPUT
  - 6 维评分均分 7.83/10
  - I1 [important][D4] § 14 F1 UserHomeNotFoundError 缺独立 ADR
  - I2 [important][D6] § 13 dogfood SHA-256 sentinel 等价语义边界未锚定
  - 7 minor: ADR-D9-9/D9-4 缺 Compare / T1 测试数 / D9 vs D10 编号 / ADR-D9-2 标题 / sentinel 边界 / candidate C dogfood 关系
- **Round 1 follow-up commit**: `b023a2e` "f009(design): r1 design-review 通过定向回修 (2 important + 7 minor 全部 LLM-FIXABLE)"
  - I1 闭合：新增 ADR-D9-10 UserHomeNotFoundError 类型与退出码（含 Compare + Decision exit 1 + Consequences）；§ 14 F1 引用更新指向 ADR-D9-10
  - I2 闭合：新增 ADR-D9-11 Dogfood SHA-256 sentinel test 等价语义边界（3 候选 Compare + Decision: 仅 SKILL.md+agent.md 落盘字节级，manifest 显式不参与）；§ 13 加 test_manifest_v2_dogfood_fields_stable.py + 测试边界澄清段
  - 7 minor 全部闭合：ADR-D9-9 三层守门 / ADR-D9-4 2 候选 Compare / T1 "2 个" / "F010 候选" / ADR-D9-2 标题精细化 / 测试边界澄清段 / candidate C dogfood anchor
- **Round 2 review**: `docs/reviews/design-review-F009-garage-init-scope-selection.md`（R2） — **`通过`**
  - 0 critical / 0 important / 0 minor
  - r1 全部 9 条 finding 闭合（9 closed / 0 open / 0 regressed）
  - 2 条非阻塞 narrative gap（不阻塞 verdict）：
    - § 17 design 注释 "F010 候选" wording 与 spec § 5 实测 "D9 候选" 不严格一致
    - § 12 NFR-902 落地表 "≥ 8 个新增测试文件" 与 § 13 实际 11 文件 informational gap
- **2 narrative gap 顺手清理**（在 approval 前由父会话直接修文，r2 reviewer 已识别为非阻塞）：
  - spec § 5 + design § 17 D7 管道扩展行 wording 统一为 "F010 候选"
  - design § 12 NFR-902 落地行 "≥ 8 个新增测试文件" → "≥ 11 个新增测试文件（详见 § 13.1 表）"
- **Auto-mode policy basis**: 同 spec approval

## Decision

**Approved**. Design 状态由 `草稿` → `已批准（auto-mode approval）`。下一步 = `hf-tasks`，输入为：

- 本 D009 design（已批准），含：
  - 11 项 ADR (D9-1..D9-11)
  - § 10.1 6 类提交分组（T1-T6）
  - § 11.1 9 条 INV 不变量
  - § 13.1 11 个新增测试文件
  - § 14 7 条失败模式
  - § 17 与 spec § 5 完整集合等价的延后项表
- F009 spec（已批准 r2）
- F007/F008 已落 packs/ + D7 安装管道（CON-901/902/903 严守）

`hf-tasks` 阶段需产出可评审任务计划，按 § 10.1 T1-T6 拆分（或视情况合并 sub-commit）；每个 task 至少含：覆盖的 INV / 触发的 spec FR/NFR / acceptance / 失败模式应对。

## Hash & 锚点

- Design 初稿提交: `f45894b` "f009(design): r1 设计草稿, 9 ADR + 6 task + 9 INV + 10 测试文件"
- r1 回修提交: `b023a2e` "f009(design): r1 design-review 通过定向回修 (2 important + 7 minor 全部 LLM-FIXABLE)"
- approval 提交（含 narrative gap 清理 + 状态 → 已批准）: 本 commit

## 后续 (informational, 不阻塞 approval)

- 11 项 ADR 由 hf-tasks 拆任务时自然消化
- 11 个新增测试文件 + 1 个 carry-forward (test_cli.py schema_version assertion 放宽) 由 hf-tasks T1-T5 拆分
- F008 cycle 5 类 minor LLM-FIXABLE 残留 与 F009 cycle 正交，本 cycle 不顺手清理
