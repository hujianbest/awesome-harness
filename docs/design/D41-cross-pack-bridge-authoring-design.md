# D41: Cross-Pack Bridge Authoring Design

- Design ID: `D41`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义跨 pack handoff 在 authoring 侧如何被设计成可理解、可验证、可重工的 bridge 体验。
- 关联文档:
  - `docs/architecture/41-cross-pack-bridge-layer.md`
  - `docs/features/F150-pack-platform-and-collaboration.md`

## 1. owner question

作者如何设计跨 pack 协作，而不是把不同能力面之间的切换埋进隐式上下文。

## 2. 设计判断

- bridge 必须显式
- acceptance / rework 必须显式
- lineage 必须可追溯

## 3. 不负责什么

- 不定义 bridge runtime 细节
- 不定义某个具体 pack 的业务流程
