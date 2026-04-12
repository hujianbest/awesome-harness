# 20: Workspace And Artifact Routing Layer

- Architecture Level: `L1`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 回答 workspace-first truths 如何被定义，以及 artifact intents 如何进入权威工作区 surfaces。
- 关联文档:
  - `docs/GARAGE.md`
  - `docs/architecture/2-garage-runtime-reference-model.md`
  - `docs/architecture/104-artifact-routing-and-workspace-facts.md`

## 1. owner question

团队工作的主事实面放在哪里，以及它如何与 runtime home 分层。

## 2. 关键判断

- `artifacts / evidence / sessions / archives / .garage` 都属于 workspace facts
- runtime home 只承载 profile、cache、adapter metadata 等运行配置
- artifact routing 是 neutral intent -> authoritative surface 的映射层

## 3. 非目标

- 不让 runtime home 吞并 workspace truths
- 不让 pack 自己定义私有顶层事实目录
