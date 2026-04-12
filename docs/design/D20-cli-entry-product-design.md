# D20: CLI Entry Product Design

- Design ID: `D20`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `CLIEntry` 作为独立工作环境入口时的产品体验模型。
- 关联文档:
  - `docs/GARAGE.md`
  - `docs/architecture/108-cli-entry.md`
  - `docs/features/F100-agent-teams-product-surface.md`
  - `docs/features/F110-runtime-topology-and-entry-bootstrap.md`

## 1. owner question

CLI 作为独立工作环境入口，用户如何进入自己的 `Garage Team`。

## 2. 设计判断

- CLI 不是调试壳，而是正式入口
- CLI 必须让用户看见 team / session / workspace identity
- CLI 可以薄，但不能丢掉 team semantics

## 3. 核心体验

- create / resume / attach
- workspace binding visibility
- current team state visibility
- governance / block / approval visibility

## 4. 不负责什么

- 不定义底层 bootstrap 实现
- 不定义 provider backend 细节
