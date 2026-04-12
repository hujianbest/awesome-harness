# 103: Execution Runtime

- Architecture Level: `L2`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 展开 provider / tool execution、trace 与 evidence materialization 的子系统级架构。
- 关联文档:
  - `docs/architecture/12-execution-and-provider-layer.md`

## 1. owner question

provider invocation、tool execution 和 trace 归一化怎样成立而不污染 core。

## 2. 关键判断

- execution owns provider/tool invocation
- governance precedes execution
- trace is a normalized runtime object
- evidence records execution, but does not replace it
