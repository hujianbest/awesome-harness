# D21: Web Entry Product Design

- Design ID: `D21`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `WebEntry` 作为 local-first 工作环境入口时的产品体验模型。
- 关联文档:
  - `docs/GARAGE.md`
  - `docs/architecture/109-web-entry.md`
  - `docs/features/F100-agent-teams-product-surface.md`
  - `docs/features/F110-runtime-topology-and-entry-bootstrap.md`

## 1. owner question

Web 作为独立工作环境入口，用户如何在浏览器里进入和使用自己的 `Garage Team`。

## 2. 设计判断

- Web 是独立产品入口，而不是附属控制面
- Web 默认 local-first
- Web 不应复制第二套 runtime 真相

## 3. 核心体验

- current team view
- session view
- workspace facts visibility
- review / approval visibility
- live work progression visibility

## 4. 不负责什么

- 不定义前端技术栈
- 不定义 streaming 协议实现
