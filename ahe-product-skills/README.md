# AHE Product Skills

`ahe-product-skills/` 用于存放 AHE 里偏产品发现、机会收敛、概念塑形和假设验证的上游 skill 资产。

它与 `ahe-coding-skills/` 的关系是：

- `ahe-product-skills/`：帮助把模糊想法收敛成更有吸引力、更有差异化、更值得实现的产品输入。
- `ahe-coding-skills/`：在需求已经相对清晰后，负责高纪律地规格化、设计、任务化和实现。

## 目录约定

- `ahe-product-skills/README.md`：本目录总览。
- `ahe-product-skills/docs/`：共享约定、方法来源和 handoff 规则。
- `ahe-product-skills/templates/`：洞察、机会、概念、验证与 bridge 模板。
- `ahe-product-skills/<skill-name>/SKILL.md`：单个 skill 的入口文件。

## Public Entry Skill

- `ahe-product-skills/using-ahe-product-workflow/`：本家族的公开入口，用于判断当前应从哪个产品洞察节点起步。

## 当前技能目录

- `ap-outcome-framing/`：把模糊想法重写成可判断的 outcome、目标用户、替代方案和焦点问题。
- `ap-insight-mining/`：从 web、GitHub、社区、替代品与现有上下文中提取洞察和白空间信号。
- `ap-opportunity-mapping/`：把证据整理成 JTBD / Opportunity / wedge 视图。
- `ap-concept-shaping/`：对候选方向做概念发散、反 commodity 挑战和差异化收敛。
- `ap-assumption-probes/`：把危险未知项转成低成本验证探针。
- `ap-spec-bridge/`：把上游产物整理成可交给 `ahe-coding-skills` 的 pre-spec bridge。

## 配套子 Agents

位于仓库根目录 `agents/`：

- `product-web-researcher.md`：提取用户、社区、替代品和竞品信号。
- `github-pattern-scout.md`：研究 GitHub / 开源里的常见模式、白空间和同质化风险。
- `product-thesis-advocate.md`：替候选 insight、opportunity 或 concept 建立最强正方论证。
- `product-contrarian.md`：挑战“看起来正确但其实普通”的 framing。
- `product-debate-referee.md`：比较正反双方论证并输出 PK verdict。
- `wedge-synthesizer.md`：对多个概念方向做比较并收敛 wedge。
- `probe-designer.md`：把危险假设转成便宜 probe 和 kill criteria。

## 多 Agent 讨论 / PK

在洞察和创新阶段，默认不是“一个 agent 想完就算”，而是：

1. 先由 `Scout` agents 带回证据。
2. 再由 `Advocate` 替候选方向建立最强支持论证。
3. 再由 `Contrarian` 主动找 commodity 风险和伪需求。
4. 最后由 `Referee` 输出 PK 结果，再由主 skill 单点落盘。

共享协议见：

- `ahe-product-skills/docs/product-debate-protocol.md`

## 默认产物位置

默认将中间产物写到：

- `docs/insights/YYYY-MM-DD-<topic>-insight-pack.md`
- `docs/insights/YYYY-MM-DD-<topic>-opportunity-map.md`
- `docs/insights/YYYY-MM-DD-<topic>-concept-brief.md`
- `docs/insights/YYYY-MM-DD-<topic>-probe-plan.md`
- `docs/insights/YYYY-MM-DD-<topic>-spec-bridge.md`

## 使用建议

1. 先从 `using-ahe-product-workflow/SKILL.md` 判断当前节点。
2. 用产品 skill 产出洞察、机会、概念和验证计划。
3. 进入 `ap-spec-bridge`，把结果压缩成可交给 `ahe-coding-skills/ahe-specify` 的输入。
4. 再进入 `ahe-coding-skills/` 走精确实现链路。

## 设计原则

- 先发散，再收敛，不允许刚开始就把 feature 当答案。
- 明确区分 `证据`、`推断`、`概念` 和 `待验证假设`。
- 输出必须既保留创造性，也能形成下一步实现输入。
- 子 agent 应小而专注，避免一个 agent 同时承担“调研 + 创意 + 决策 + 写主文档”。
