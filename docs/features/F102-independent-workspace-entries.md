# F102: Independent Workspace Entries

- Feature ID: `F102`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `CLIEntry` 与 `WebEntry` 作为独立工作环境入口应共享的稳定产品语义。

## 1. 这份文档回答什么

什么叫“独立工作环境入口”。

## 2. owner question

CLI 和 Web 作为独立入口，应共享哪些产品语义，哪些差异只能停留在 UX 层。

## 3. 稳定语义

- CLI 与 Web 都是 `Garage` 自己的产品入口
- 它们可以有不同 UX，但不能拥有不同 runtime truth
- 它们都必须进入同一条 `Bootstrap -> SessionApi -> Session` 主链

## 4. 必须共享的对象

- `Garage Team`
- workspace binding
- session identity
- governance-backed work progression
- evidence-linked work results

## 5. 允许差异的层面

- 交互方式
- 展示方式
- 恢复和状态呈现的 UX
- 是否支持 richer controls，例如 Web 的多面板视图

## 6. 不允许差异的层面

- profile authority
- session lifecycle 语义
- pack / bridge truth
- growth truth

## 7. 非目标

- 不要求 CLI 与 Web 在视觉或交互细节上完全一致
- 不把 Web 提前升级成 remote SaaS 控制面
- 不让 CLI 退化成只给开发者调试的内部入口

## 8. Acceptance

- 用户从 CLI 或 Web 进入时，进入的是同一个 `Garage Team` 工作环境
- 两类入口可以恢复同一 workspace / session，而不会出现双重真相
- 任何一类入口都不能定义私有 runtime 规则
