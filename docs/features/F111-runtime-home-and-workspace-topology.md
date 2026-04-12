# F111: Runtime Home And Workspace Topology

- Feature ID: `F111`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `runtime home / workspace` 的稳定拓扑语义。

## 1. 这份文档回答什么

`runtime home`、workspace 和 source root 之间到底怎样分层，哪些事实落在哪里，哪些不能混写。

## 2. owner question

谁拥有运行配置，谁拥有工作事实，以及不同入口如何在同一套拓扑规则上工作。

## 3. 稳定语义

- workspace facts live in the workspace
- runtime home owns runtime config, cache, and adapter metadata
- source root, runtime home, and workspace must remain distinct layers

## 4. 最小结构要求

workspace 至少承接：

- artifacts
- evidence
- sessions
- archives
- .garage

runtime home 至少承接：

- profiles
- config
- cache
- adapters metadata

## 5. 失败语义

下面这些情况必须被视为拓扑错误：

- runtime home 与 workspace root 相同
- runtime home 落到 workspace facts 目录内部
- source root、workspace、runtime home 的角色被混淆

## 6. 非目标

- 不要求 source root 永远等于 workspace
- 不把 runtime home 设计成主事实面
- 不允许通过宿主缓存替代 workspace facts

## 7. Acceptance

- 三层拓扑边界可被显式检查
- 不同入口对同一 workspace / runtime home 得出相同解释
- workspace facts 与 runtime config 的归属不会再由实现猜测
