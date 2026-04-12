# F113: Session API And Shared Entry Binding

- Feature ID: `F113`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `SessionApi` 作为 shared entry seam 的稳定语义。

## 1. 这份文档回答什么

所有入口怎样通过同一条 entry-facing seam 进入 `Garage Team runtime`，而不是各自直连不同内部对象。

## 2. owner question

`SessionApi` 应该拥有哪些稳定职责，哪些职责不能落到 `CLIEntry`、`WebEntry` 或 `HostBridgeEntry` 私有实现中。

## 3. 稳定语义

- all entries bind through `SessionApi`
- `SessionApi` is the entry-facing choke point
- create / resume / attach / submitStep stay on one path

## 4. 最小请求面

`SessionApi` 至少应统一承接下面这些动作：

- create
- resume
- attach
- submitStep
- interrupt
- closeout / approval-like progression hooks

这些动作的共同要求是：

- 都先绑定到同一个 workspace
- 都引用同一个 session identity
- 都通过同一个 runtime authority 链解释 profile / host / workspace

## 5. 最小返回面

对入口层来说，`SessionApi` 至少应稳定返回：

- session identity
- workspace identity
- host binding summary
- session status
- 关联的 workspace facts locator

对后续执行动作来说，`SessionApi` 还应稳定交出：

- shared runtime context
- session-bound execution handoff

## 6. 失败与拒绝语义

下面这些失败不应由入口各自私自解释：

- workspace binding 缺失或冲突
- session 不存在
- launch mode 与当前状态不匹配
- host binding 不兼容
- governance 在 entry gate 上阻断

这些都应先作为 `SessionApi` 级失败被归一化，再由不同入口决定如何展示。

## 7. 非目标

- 不让 `SessionApi` 直接拥有 provider/tool invocation 逻辑
- 不让入口绕过 `SessionApi` 直接操作 `Session`
- 不把 `SessionApi` 退化成只给某一个入口用的 helper

## 8. Acceptance

- CLI / Web / HostBridge 对同一组 create / resume / attach 动作使用同一条语义链
- 入口层不再需要自己定义 session identity 和 workspace binding 规则
- entry gate 的失败可以被统一解释并被不同入口消费
