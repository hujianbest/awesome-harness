---
name: ahe-spec-bridge
description: 适用于 outcome/opportunity/concept/assumptions 已基本清楚、需要把上游产品洞察压缩为 ahe-specify 可消费输入的场景。不适用于上游方向未收敛（→ 前序 product insight 节点）或已在写正式 spec（→ ahe-specify）的场景。
---

# AHE Spec Bridge

负责把 product insight family 的上游工件压缩成 `ahe-specify` 可消费的预 spec 输入——避免 coding family 被迫从模糊想法里反向猜产品命题。不替代 `ahe-specify` 本身。

## When to Use

**正向触发：**
- 已有 framing、insight、opportunity、concept 或 probe 结果
- 当前需要进入 `ahe-specify`
- 想把 evidence、concept 和 unknowns 一起带过去

**不适用：**
- 上游方向还没收敛 → 回到前面的 product 节点
- 当前已经在写正式 spec → 直接用 `ahe-specify`

**Direct invoke：** 用户说"可以开始写 spec 了""准备好交给开发了""把产品洞察整理一下"

**相邻边界：** 若整理过程中发现上游工件严重缺失（无 concept brief、无 probe 结果），应先退回对应前序节点补齐，而非强行桥接。

## Workflow

### 1. 先读取所有上游工件

读取项目中已有的 insight-pack、opportunity-map、concept-brief、probe-plan。若无任何上游工件，reroute 到 `using-ahe-product-workflow` 判断应进入哪个前序节点。

### 2. 把上游内容压缩成"机会 thesis"

必须能写成一句话：

- 为谁
- 在什么情境下
- 解决什么 progress blockage
- 预期改变什么 outcome

### 3. 明确哪些内容已经足够稳定

至少区分：

- 已被 evidence 支撑的内容
- 仍然只是工作假设的内容

### 4. 给 ahe-specify 准备 scope 边界

至少写清：

- v1 必须包含什么行为
- 这轮明确不做什么
- 哪些开放问题需要在 spec 阶段继续澄清

**决策点：** 若 v1 scope 仍然模糊，说明上游 concept 收敛不够，退回 `ahe-concept-shaping`。

### 5. 不把 concept brief 直接冒充正式需求规格

这里的目标不是抢写 spec，而是提供：

- 更好的上游输入
- 更少的猜测空间
- 更明确的非目标和风险

### 6. 落盘成 spec-bridge

使用 pack 内模板 `../templates/spec-bridge-template.md`，至少补齐：

- Opportunity Thesis
- Target User And Context
- Desired Outcome
- Proposed v1 Shape
- Differentiation
- Evidence And Unknowns
- Open Questions For Spec

## Output Contract

- **写什么：** spec-bridge 文档 + bridge status
- **写到哪里：** 项目约定位置（参考 AGENTS.md），默认示例 `docs/insights/YYYY-MM-DD-<topic>-spec-bridge.md`
- **状态同步：** bridge status 标记为 `ready-for-ahe-specify`
- **下一步：** `ahe-specify`（在 coding pack 中）

## Red Flags

- 读完 bridge 仍然不知道"为什么值得做"
- 所有内容都像 marketing 文案
- 完全没有 open questions
- 把 feature list 当作全部 bridge 内容

## Common Mistakes

| 错误 | 后果 | 修复 |
|------|------|------|
| 把 concept brief 直接当 spec 用 | coding family 缺少结构化输入 | 只提供预 spec 输入，让 ahe-specify 写正式 spec |
| 不标注 unknowns | spec 阶段被迫猜测 | 显式列出 evidence-backed vs working hypothesis |
| scope 没有边界 | v1 无限膨胀 | 明确写清"这轮不做什么" |

## 和其他 Skill 的区别

| 对比项 | ahe-spec-bridge | ahe-assumption-probes | ahe-concept-shaping | ahe-specify |
|--------|----------------|----------------------|---------------------|-------------|
| 核心任务 | 压缩上游为 spec 输入 | 设计验证探针 | 发散收敛概念方向 | 编写正式功能规格 |
| 输入 | 所有上游工件 | concept brief | opportunity-map | spec-bridge |
| 输出 | spec-bridge | probe-plan | concept-brief | feature spec |
| 所在 family | product-insights | product-insights | product-insights | coding |
| 在链路中的位置 | product 最后一站 | concept 之后 | opportunity 之后 | bridge 之后 |

## Reference Guide

| 材料 | 路径 | 用途 |
|------|------|------|
| Spec Bridge 模板 | `../templates/spec-bridge-template.md` | 落盘格式 |
| 产品洞察共享约定 | `../docs/product-insight-shared-conventions.md` | 家族级术语和约定 |
| 产品洞察基础 | `../docs/product-insight-foundations.md` | 方法论背景 |

## Verification

- [ ] spec-bridge 已落盘
- [ ] 机会 thesis 能写成一句话
- [ ] evidence-backed vs working hypothesis 已区分
- [ ] v1 scope 有明确边界（含非目标）
- [ ] open questions 已列出
- [ ] bridge status = ready-for-ahe-specify
- [ ] 下一步 skill 已明确（→ ahe-specify）
