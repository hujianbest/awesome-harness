---
name: ahe-assumption-probes
description: 适用于已有 concept brief 但关键假设尚无证据、需要设计低成本验证探针并明确 kill criteria 的场景。不适用于方向未选清（→ ahe-concept-shaping）或已有充分验证只需交接（→ ahe-spec-bridge）的场景。
---

# AHE Assumption Probes

负责在进入实现之前，把危险假设转化为可快速证伪的一次性探针。不替代 spec 编写或功能设计。

## When to Use

**正向触发：**
- 已有 concept brief，但没有明确 kill criteria
- 团队正准备把未验证方向直接送进实现
- 需要区分 desirability / usability / viability / feasibility 风险

**不适用：**
- 方向还没选清楚 → `ahe-concept-shaping`
- 已验证充分，只差 handoff → `ahe-spec-bridge`

**Direct invoke：** 用户明确说"先做个 smoke test""验证一下再说""这个方向有风险"

**相邻边界：** 若当前缺的不是验证而是概念方向本身，回到 `ahe-concept-shaping`。

## Workflow

### 1. 先读取已有 concept brief 和上游证据

读取项目中的 concept brief、opportunity map、insight pack 等已有工件。若无上游工件，reroute 到 `ahe-concept-shaping`。

### 2. 列出完整风险栈

至少区分：

- desirability：用户真的在乎吗
- usability：用户真的能顺畅完成吗
- viability：这件事对业务有价值吗
- feasibility：技术和流程上真的可行吗

### 3. 只选最危险的 1 到 3 个假设

不要一口气设计十几个 probe。

优先挑：

- 一旦被证伪，整条方向都要重来
- 或者会直接改变 scope 和 spec 写法

**决策点：** 若所有假设都同等危险，说明 concept 本身收敛不够，回到 `ahe-concept-shaping`。

### 4. 为每个关键假设设计最便宜 probe

默认优先：

- 访谈脚本
- 人工 concierge
- 低保真原型
- fake door
- 单页叙事稿
- 局部技术 spike

不是所有问题都要写代码。

### 5. 明确 harsh truth 和 kill criteria

每个 probe 都应写清：

- pass 条件
- fail 条件
- 哪个结果会让你停止继续下注

如果 probe 没有 kill criteria，它大概率只是"给自己打气"。

### 6. 明确 disposal plan

默认把 probe 当 disposable artifact，而不是 proto-MVP。

### 7. 落盘成 probe-plan

使用 pack 内模板 `../templates/probe-plan-template.md`，至少补齐：

- Risk Stack
- Selected Probe
- Success / Failure
- Minimal Setup

## Output Contract

- **写什么：** probe-plan 文档
- **写到哪里：** 项目约定位置（参考 AGENTS.md），默认示例 `docs/insights/YYYY-MM-DD-<topic>-probe-plan.md`
- **状态同步：** probe-plan 包含 risk stack、selected probes、kill criteria
- **下一步：** 执行 probe 后回到本节点更新结果；若已有足够 bridge 信息 → `ahe-spec-bridge`

## Red Flags

- probe 太大，已经接近做半个产品
- success criteria 全是模糊词
- 完全没有 failure threshold
- 所谓验证其实只是收集正反馈

## Common Mistakes

| 错误 | 后果 | 修复 |
|------|------|------|
| probe 设计成 MVP | 投入过大，舍不得停 | 限制每个 probe < 1 天工作量 |
| 只有 pass 条件 | 验证退化为"给自己打气" | 每条必须写明 kill 条件 |
| 一次验证太多假设 | 结论不清晰 | 只选 1-3 个最危险假设 |

## 和其他 Skill 的区别

| 对比项 | ahe-assumption-probes | ahe-concept-shaping | ahe-spec-bridge |
|--------|----------------------|---------------------|-----------------|
| 核心任务 | 设计验证探针 | 发散收敛概念方向 | 压缩上游输出为 spec 输入 |
| 输入 | concept brief + 假设 | opportunity map | 所有上游工件 |
| 输出 | probe-plan | concept-brief | spec-bridge |
| 何时用 | 方向已选但假设未验证 | 方向泛泛需要分化 | 已验证完毕准备交接 |

## Reference Guide

| 材料 | 路径 | 用途 |
|------|------|------|
| Probe Plan 模板 | `../templates/probe-plan-template.md` | 落盘格式 |
| 产品洞察共享约定 | `../docs/product-insight-shared-conventions.md` | 家族级术语和约定 |
| 产品辩论协议 | `../docs/product-debate-protocol.md` | 多 agent 讨论规范 |
| 产品洞察基础 | `../docs/product-insight-foundations.md` | 方法论背景 |
| Agent: probe-designer | `../../agents/probe-designer.md` | 探针设计辅助 |
| Agent: product-contrarian | `../../agents/product-contrarian.md` | 反向挑战 |

## Verification

- [ ] probe-plan 已落盘
- [ ] 每个关键假设都有对应 probe
- [ ] 每个 probe 都有明确的 pass / fail / kill criteria
- [ ] probe 方案足够便宜（不会诱导团队继续硬做）
- [ ] 下一步 skill 已明确（执行 probe / ahe-spec-bridge）
