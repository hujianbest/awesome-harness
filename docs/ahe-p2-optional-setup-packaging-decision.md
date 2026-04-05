# AHE P2 Optional Setup And Packaging Decision

## Decision Summary

本轮 **不新增** 以下 P2 optional assets：

- setup / install 文档
- hook 示例
- plugin 示例
- packaging 辅助层

原因不是这些资产永远不需要，而是当前还没有足够强的复用信号，证明它们已经值得进入长期维护面。

## Why Not Add Them Now

### 1. 当前问题已经能被 docs-first 资产覆盖

这一轮 P2 已经补齐了：

- `docs/ahe-workflow-externalization-guide.md`
- `docs/ahe-path-mapping-guide.md`
- `docs/ahe-workflow-core-vs-extensions.md`

它们已经能回答当前最关键的问题：

- 外部仓库最少需要哪些工件
- 如何把逻辑工件映射到实际路径
- 哪些属于 runtime core，哪些只是体验层 extension

在这些前提都还刚刚明确时，立刻再加 setup / install / hook 层，只会把“说明接入条件”和“真正自动化接入”两件事混在一起。

### 2. AHE 目前仍是 docs-first workflow family，不是分发型产品包

当前仓库的核心资产仍然是：

- `skills/ahe-workflow-starter/SKILL.md`
- 各 `skills/ahe-*/SKILL.md`
- `docs/` 下的 shared conventions、entrypoints、externalization 与 boundary docs

这些资产已经足以支撑：

- 仓库内 workflow 编排
- 外部仓库按映射方式采用
- direct invoke 与 chain invoke 的边界说明

但还不足以自然推出“一键安装”或“宿主无关 packaging”方案。若现在强行补包装层，产出会更像猜测，而不是被真实接入路径验证过的模式。

### 3. 宿主差异还没有稳定到值得抽象

setup / hook / plugin 层一旦存在，就必须回答很多宿主相关问题，例如：

- 哪些入口面向 Cursor，哪些面向 Claude Code，哪些只适用于某个宿主
- 哪些命令只是说明性 wrapper，哪些需要真正落地成命令文件
- hooks 应该在什么时机触发，是否会与 `ahe-workflow-starter` 的 authority 冲突

当前这些问题仍然更适合留在文档与参考资料层，而不是提前冻结成安装资产。

### 4. 维护税会先于收益出现

一旦新增 setup / install / hook / plugin / packaging 资产，后续每次更新以下内容都可能需要同步：

- shared conventions
- entrypoint 规则
- review / gate 流程
- profile 约束
- 外部仓库映射前提

在没有第二个真实宿主持续消费这些包装层之前，这类同步成本大概率会先于复用收益出现。

## Current Replacement Strategy

当前用以下更轻的资产组合替代 setup / packaging 层：

- 外部采用前置条件：`docs/ahe-workflow-externalization-guide.md`
- 路径与工件映射：`docs/ahe-path-mapping-guide.md`
- core / extension 边界：`docs/ahe-workflow-core-vs-extensions.md`
- 仓库级规则入口：`AGENTS.md`
- live runtime skills：`skills/ahe-*/SKILL.md`

这套组合的目标不是“零摩擦安装”，而是先保证“即使不安装任何包装层，也能正确采用 AHE contract”。

## Revisit Triggers

只有在出现以下至少一个真实信号时，再考虑进入 setup / packaging 实施：

- 明确有第二个仓库要采用 AHE workflow family
- 已经出现重复的手动安装 / 接入动作，且步骤相对稳定
- 内部使用者反复请求更低摩擦 setup
- 某个宿主的命令入口、hook 时机和安装边界已经被证明稳定

## What To Add When Revisited

若未来触发重启，本阶段优先考虑的产物应是：

- setup / install guide
- host-scoped hook examples
- host-scoped plugin or command examples
- “单节点采用” 与 “整链采用” 的接入示例
- 更明确的 core package / extension package 落地方式

注意：这些产物仍应被标记为 optional，不应反过来定义 AHE 的 runtime truth。

## Practical Outcome

因此，`P2-4` 当前结论是：

- setup / install：defer
- hook / plugin examples：defer
- packaging helper layer：defer

等真实复用信号出现后，再把本决策文档升级为实施输入，而不是现在预支维护成本。
# AHE P2 Optional Setup And Packaging Decision

## Decision Summary

本轮 **不新增** 以下 P2 optional assets：

- setup / install 文档
- hook 示例
- plugin 示例
- packaging 辅助层

原因不是这些资产永远不需要，而是当前还没有足够强的复用信号，证明它们已经值得进入长期维护面。

## Why Not Add Them Now

### 1. 当前问题已经能被 docs-first 资产覆盖

这一轮 P2 已经补齐了：

- `docs/ahe-workflow-externalization-guide.md`
- `docs/ahe-path-mapping-guide.md`
- `docs/ahe-workflow-core-vs-extensions.md`

它们已经能回答当前最关键的问题：

- 外部仓库最少需要哪些工件
- 如何把逻辑工件映射到实际路径
- 哪些属于 runtime core，哪些只是体验层 extension

在这些前提都还刚刚明确时，立刻再加 setup / install / hook 层，只会把“说明接入条件”和“真正自动化接入”两件事混在一起。

### 2. AHE 目前仍是 docs-first workflow family，不是分发型产品包

当前仓库的核心资产仍然是：

- `skills/ahe-workflow-starter/SKILL.md`
- 各 `skills/ahe-*/SKILL.md`
- `docs/` 下的 shared conventions、entrypoints、externalization 与 boundary docs

这些资产已经足以支撑：

- 仓库内 workflow 编排
- 外部仓库按映射方式采用
- direct invoke 与 chain invoke 的边界说明

但还不足以自然推出“一键安装”或“宿主无关 packaging”方案。若现在强行补包装层，产出会更像猜测，而不是被真实接入路径验证过的模式。

### 3. 宿主差异还没有稳定到值得抽象

setup / hook / plugin 层一旦存在，就必须回答很多宿主相关问题，例如：

- 哪些入口面向 Cursor，哪些面向 Claude Code，哪些只适用于某个宿主
- 哪些命令只是说明性 wrapper，哪些需要真正落地成命令文件
- hooks 应该在什么时机触发，是否会与 `ahe-workflow-starter` 的 authority 冲突

当前这些问题仍然更适合留在文档与参考资料层，而不是提前冻结成安装资产。

### 4. 维护税会先于收益出现

一旦新增 setup / install / hook / plugin / packaging 资产，后续每次更新以下内容都可能需要同步：

- shared conventions
- entrypoint 规则
- review / gate 流程
- profile 约束
- 外部仓库映射前提

在没有第二个真实宿主持续消费这些包装层之前，这类同步成本大概率会先于复用收益出现。

## Current Replacement Strategy

当前用以下更轻的资产组合替代 setup / packaging 层：

- 外部采用前置条件：`docs/ahe-workflow-externalization-guide.md`
- 路径与工件映射：`docs/ahe-path-mapping-guide.md`
- core / extension 边界：`docs/ahe-workflow-core-vs-extensions.md`
- 仓库级规则入口：`AGENTS.md`
- live runtime skills：`skills/ahe-*/SKILL.md`

这套组合的目标不是“零摩擦安装”，而是先保证“即使不安装任何包装层，也能正确采用 AHE contract”。

## Revisit Triggers

只有在出现以下至少一个真实信号时，再考虑进入 setup / packaging 实施：

- 明确有第二个仓库要采用 AHE workflow family
- 已经出现重复的手动安装 / 接入动作，且步骤相对稳定
- 内部使用者反复请求更低摩擦 setup
- 某个宿主的命令入口、hook 时机和安装边界已经被证明稳定

## What To Add When Revisited

若未来触发重启，本阶段优先考虑的产物应是：

- setup / install guide
- host-scoped hook examples
- host-scoped plugin or command examples
- “单节点采用” 与 “整链采用” 的接入示例
- 更明确的 core package / extension package 落地方式

注意：这些产物仍应被标记为 optional，不应反过来定义 AHE 的 runtime truth。

## Practical Outcome

因此，`P2-4` 当前结论是：

- setup / install：defer
- hook / plugin examples：defer
- packaging helper layer：defer

等真实复用信号出现后，再把本决策文档升级为实施输入，而不是现在预支维护成本。
