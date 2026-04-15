---
name: ahe-outcome-framing
description: 适用于 idea 听起来仍像"做一个 X App"、已上线产品感觉平庸、或需要在 research 前先把问题写锋利的场景。不适用于已有清晰 outcome 只缺证据（→ ahe-insight-mining）或已有 framing 需要排机会（→ ahe-opportunity-mapping）的场景。
---

# AHE Outcome Framing

负责把模糊 idea 重写为一个更锋利的问题定义——目标用户、progress blockage、当前替代品和 commodity 风险。不替代 insight 挖掘或机会排序。

## When to Use

**正向触发：**
- 用户只有一个宽泛品类想法
- 用户说项目"普通""没有吸引力"
- 需要先把问题写锋利，再决定查什么
- 怀疑当前讨论还停留在 solution-first

**不适用：**
- 已有清晰 outcome 和用户 progress → `ahe-insight-mining`
- 已有足够 framing，需要机会排序 → `ahe-opportunity-mapping`

**Direct invoke：** 用户说"帮我重新定义问题""这个方向太模糊了""我不知道用户到底卡在哪"

**相邻边界：** 若在 framing 过程中用户已带来大量外部信号，可直接跳到 `ahe-opportunity-mapping`。

## Workflow

### 1. 先读取已有的项目材料和用户输入

读取项目中已有的 idea 描述、用户反馈、会议记录等。收集用户对问题的原始说法。

### 2. 把当前 idea 还原成一句"未经打磨的原始说法"

例如：

- "做一个摄影社区"
- "做一个 AI 创业工具"
- "做一个 xx 管理平台"

不要假装这已经是好问题定义。

### 3. 强制改写成 outcome 语言

至少补齐：

- 目标用户是谁
- 他们在什么情境下遇到问题
- 现在怎么凑合解决
- 如果这件事被解决，会改善什么 outcome

### 4. 识别当前 framing 的 commodity 风险

至少检查：

- 这是不是一个"任何人都能说"的大类目
- 它是不是只描述了工具形态，没有描述 progress
- 它是不是没有说明为什么现在值得做
- 它是不是没有说清为什么用户不会继续用现有替代品

**决策点：** 若 commodity 风险极高且无法用 progress 语言重写，可能 idea 本身需要重新审视。

### 5. 生成多个 framing，而不是只保留一个

至少提出 3 个候选 framing：

- pain-first
- progress-first
- wedge-first

每个 framing 都应说明：

- 一句话问题定义
- 目标用户
- outcome
- 最大风险

### 6. 选择当前最值得继续研究的 framing

优先选择同时满足：

- 有潜在强痛点或强动机
- 有清晰替代品或 workaround
- 有机会形成差异化 wedge

### 7. 落盘到可继续研究的结构

使用 pack 内模板 `../templates/insight-pack-template.md`，至少先填：

- Problem Snapshot
- Commodity Risks
- Open Questions

## Output Contract

- **写什么：** problem / outcome frame 文档
- **写到哪里：** 项目约定位置（参考 AGENTS.md），默认示例 `docs/insights/YYYY-MM-DD-<topic>-framing.md`
- **状态同步：** framing 包含问题定义、目标用户、outcome、替代品、commodity 风险
- **下一步：** `ahe-insight-mining`（若用户已有大量外部信号，可直接 → `ahe-opportunity-mapping`）

## Red Flags

- 说了很多 feature，但说不出用户现在怎么凑合做
- outcome 仍然是"提升体验""做得更好"这种空话
- 只有一个 framing，没有做任何发散
- 把品牌 slogan 当问题定义

## Common Mistakes

| 错误 | 后果 | 修复 |
|------|------|------|
| 只保留 1 个 framing | 失去发现更好问题的机会 | 强制至少 3 个候选 framing |
| 用 feature 语言写问题 | 后续所有 skill 都会跑偏 | 改用 progress / outcome 语言 |
| 不写替代品 | 无法判断 wedge 是否成立 | 必须写清用户现在怎么凑合 |

## 和其他 Skill 的区别

| 对比项 | ahe-outcome-framing | ahe-insight-mining | ahe-opportunity-mapping |
|--------|--------------------|--------------------|------------------------|
| 核心任务 | 重写模糊 idea 为锋利问题 | 提取外部信号和洞察 | 选择优先机会 |
| 输入 | 用户模糊 idea | framing 文档 | insight-pack |
| 输出 | problem/outcome frame | insight-pack | opportunity-map |
| 关键动作 | 问题重构 + commodity 检查 | 多源信号 → thesis PK | JTBD + 机会排序 |
| 在链路中的位置 | 第一个节点 | 第二个节点 | 第三个节点 |

## Reference Guide

| 材料 | 路径 | 用途 |
|------|------|------|
| Insight Pack 模板（含 framing 部分） | `../templates/insight-pack-template.md` | 落盘格式 |
| 产品洞察共享约定 | `../docs/product-insight-shared-conventions.md` | 家族级术语和约定 |
| 产品洞察基础 | `../docs/product-insight-foundations.md` | 方法论背景 |

## Verification

- [ ] framing 文档已落盘
- [ ] 问题定义不再只是一个品类名
- [ ] 明确写出了目标用户和触发情境
- [ ] 明确写出了 desired outcome
- [ ] 明确写出了当前替代品或 workaround
- [ ] 明确写出了 commodity 风险
- [ ] 下一步 skill 已明确（→ ahe-insight-mining 或 ahe-opportunity-mapping）
