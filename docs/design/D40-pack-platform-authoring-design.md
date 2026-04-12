# D40: Pack Platform Authoring Design

- Design ID: `D40`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 packs、contracts、registry 在 authoring 侧如何被设计成可持续扩展的能力平台。
- 关联文档:
  - `docs/architecture/40-pack-platform-and-extension-layer.md`
  - `docs/features/F150-pack-platform-and-collaboration.md`

## 1. owner question

新增能力面时，作者如何理解 pack platform，而不是把平台当成一堆散乱扩展点。

## 2. 设计判断

- packs 是 team capability extension
- contracts 是 authoring language
- registry 是 discovery and validation seam

## 3. 不负责什么

- 不定义 pack runtime 实现
- 不定义具体 pack 内容
