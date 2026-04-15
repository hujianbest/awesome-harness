---
name: ahe-concept-shaping
description: 适用于已选定机会但解法方向泛泛或同质化、需要发散多个 product concept 再收敛差异化 wedge 的场景。不适用于机会未选清（→ ahe-opportunity-mapping）或假设未暴露（→ ahe-assumption-probes）的场景。
---

# AHE Concept Shaping

负责把"值得追的机会"发散成多个概念方向，再通过多 agent 对撞收敛为有记忆点的 wedge。不替代机会排序或验证探针。

## When to Use

**正向触发：**
- opportunity 已选好，但解法仍然泛泛
- 需要提出多个 product concept，再收敛 wedge
- 怀疑当前方向"看起来正确，但没有记忆点"

**不适用：**
- 机会还没选清楚 → `ahe-opportunity-mapping`
- 关键未知项还没暴露，先做概念收敛后再去 `ahe-assumption-probes`

**Direct invoke：** 用户说"方向有了但太平庸""帮我找到差异化""概念不够 sharp"

**相邻边界：** 若在发散过程中发现机会本身有问题，退回 `ahe-opportunity-mapping`。

## Workflow

### 1. 先读取已有的 opportunity map 和上游工件

读取项目中的 opportunity map、insight pack、framing 文档。若无 opportunity 工件，reroute 到 `ahe-opportunity-mapping`。

### 2. 把 selected opportunity 写成一句人话

确保能用 1-2 句话说明：

- 用户到底卡在哪一步
- 现有替代方案为什么不够好

### 3. 强制发散至少 3 个 concept direction

每个方向都要写：

- 一句话 pitch
- 主要价值
- 与现有常见做法的差异
- 为什么用户可能记得住

**决策点：** 若发散不出 3 个有实质差异的方向，说明 opportunity 定义太窄或太 solution-specific，退回 step 2 或回到 `ahe-opportunity-mapping`。

### 4. 让 Advocate 为每个方向写 strongest case

使用 `../../agents/product-thesis-advocate.md`，至少说明：

- 为什么用户会被这个方向吸引
- 如果它成立，真正的 wedge 是什么
- 为什么它可能比其他方向更有 pull

### 5. 对每个方向做 commodity challenge

使用 `../../agents/product-contrarian.md`，至少问：

- 这个方向是不是只是在已有产品上加一层新外壳
- 最容易被复制的部分是什么
- 如果没有品牌光环，还有什么硬 wedge

### 6. 让 Referee 做 concept PK

使用 `../../agents/product-debate-referee.md`，至少输出：

- 哪些方向 survive / park / drop
- 每个被淘汰方向为什么出局

### 7. 补齐 surviving concepts 的 retained value 逻辑

每个候选方向至少回答：

- 用户第一次为什么会试
- 用户第二次为什么会回来
- 随着使用增加，价值会不会变强

### 8. 让 wedge-synthesizer 做最终收敛

使用 `../../agents/wedge-synthesizer.md`，要求：

- 不能跳过前面的 PK
- 必须明确为什么推荐方向胜过其他 surviving options

### 9. 选择当前推荐 wedge

推荐 wedge 不一定是最完整的方向，而是：

- 最有差异化
- 最有初始 pull
- 最能被便宜验证
- 最适合进入下一步 probe

### 10. 落盘成 concept-brief

使用 pack 内模板 `../templates/concept-brief-template.md`，至少补齐：

- Concept Directions
- Concept PK
- Recommended Wedge
- Loop / Retention Logic
- Scope Guess

## Output Contract

- **写什么：** concept-brief 文档
- **写到哪里：** 项目约定位置（参考 AGENTS.md），默认示例 `docs/insights/YYYY-MM-DD-<topic>-concept-brief.md`
- **状态同步：** concept-brief 包含至少 3 个方向比较、PK 结论、推荐 wedge
- **下一步：** `ahe-assumption-probes`

## Red Flags

- 所谓多个方向，其实只是同一方案换说法
- 推荐理由只有"容易做"或"功能多"
- 完全没有 retained value 逻辑
- 明明很像竞品 copy，却没有正面承认
- 还没经过 PK 就让 wedge-synthesizer 直接拍板

## Common Mistakes

| 错误 | 后果 | 修复 |
|------|------|------|
| 只发散 1-2 个方向 | 选不出真正有差异的 wedge | 强制至少 3 个方向 |
| 跳过 commodity challenge | 选出的方向容易被复制 | 每个方向必须过 contrarian 审查 |
| 不写 retained value | 只看首次吸引力 | 补齐"为什么回来"逻辑 |

## 和其他 Skill 的区别

| 对比项 | ahe-concept-shaping | ahe-opportunity-mapping | ahe-assumption-probes | ahe-spec-bridge |
|--------|---------------------|------------------------|----------------------|-----------------|
| 核心任务 | 发散收敛概念方向 | 选择优先机会 | 设计验证探针 | 压缩为 spec 输入 |
| 输入 | opportunity map | insight pack | concept brief | 所有上游工件 |
| 输出 | concept-brief | opportunity-map | probe-plan | spec-bridge |
| 关键动作 | 多方向 PK + wedge 收敛 | JTBD + 机会排序 | 假设 → kill criteria | thesis 压缩 |

## Reference Guide

| 材料 | 路径 | 用途 |
|------|------|------|
| Concept Brief 模板 | `../templates/concept-brief-template.md` | 落盘格式 |
| 产品洞察共享约定 | `../docs/product-insight-shared-conventions.md` | 家族级术语和约定 |
| 产品辩论协议 | `../docs/product-debate-protocol.md` | 多 agent 讨论规范 |
| 产品洞察基础 | `../docs/product-insight-foundations.md` | 方法论背景 |
| Agent: thesis-advocate | `../../agents/product-thesis-advocate.md` | 为方向辩护 |
| Agent: contrarian | `../../agents/product-contrarian.md` | 反向挑战 |
| Agent: debate-referee | `../../agents/product-debate-referee.md` | PK 裁判 |
| Agent: wedge-synthesizer | `../../agents/wedge-synthesizer.md` | 最终收敛 |

## Verification

- [ ] concept-brief 已落盘
- [ ] 至少比较了 3 个概念方向
- [ ] 至少指出 1 个最容易平庸化的方向
- [ ] 推荐 wedge 有差异化说明（非 clone 理由）
- [ ] 有多 agent PK 结论记录
- [ ] 下一步 skill 已明确（→ ahe-assumption-probes）
