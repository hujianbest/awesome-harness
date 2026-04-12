# F152: Shared Contracts And Schemas

- Feature ID: `F152`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 shared contracts 和 schema shapes 的稳定语义。

## 1. 这份文档回答什么

pack extension 为什么必须通过 shared contracts 和 schemas，而不是靠隐式约定和私有对象协议。

## 2. owner question

哪些对象属于 shared contracts，哪些字段和形状必须稳定，哪些不应被宿主或 pack 私自扩成系统真相。

## 3. 稳定语义

- contracts provide neutral shared language
- schemas keep contract shapes stable and versionable
- pack extension depends on contracts, not on implicit conventions

## 4. 最小共享对象面

- pack-facing capability declarations
- runtime-readable role / node / artifact / evidence anchors
- host adapter related shared boundary objects

## 5. 边界规则

- contracts 负责共享语言，不负责 provider truth
- schemas 负责稳定形状，不负责业务实现
- pack-local convenience metadata 不能反向升级成核心共享语义

## 6. 非目标

- 不做领域特化 contract marketplace
- 不把 contracts 扩成每个 pack 自己的私有类型系统

## 7. Acceptance

- packs 通过 shared contracts 接入系统
- schema 形状可被校验和版本化
- 隐式约定不再承担主线互操作责任
