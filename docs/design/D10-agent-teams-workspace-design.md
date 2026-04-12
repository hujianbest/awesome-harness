# D10: Agent Teams Workspace Design

- Design ID: `D10`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 `Garage` 作为 `Agent Teams` 工作环境时，用户实际面对的团队对象、工作空间对象与长期工作体验模型。
- 关联文档:
  - `docs/VISION.md`
  - `docs/GARAGE.md`
  - `docs/architecture/1-garage-system-overview.md`
  - `docs/features/F100-agent-teams-product-surface.md`

## 1. owner question

用户进入 `Garage` 时，到底进入了什么样的工作环境。

## 2. 设计判断

- 用户进入的是自己的 `Garage Team`
- team 比 model / tool list 更靠前
- workspace 不是文件夹视图的附属物，而是团队工作的长期事实面
- 不同 agents 需要被用户感知为团队成员，而不是匿名执行器

## 3. 设计要素

- team identity
- role visibility
- handoff visibility
- review visibility
- workspace facts visibility

## 4. 不负责什么

- 不定义 runtime 内部对象
- 不定义具体入口控件或页面
