# 场景 03：任务计划已批准，可进入实现

## 目的

验证在 spec、design、task plan 都已批准，且当前任务进度证据指向实现阶段时，是否路由到 `mdc-implement`。

## 用户 Prompt

```text
继续这个项目。按照已经确认好的任务计划，先做当前该做的那一项，不要自己扩 scope。
```

## 期望

- 先命中 `mdc-workflow-starter`
- 读取 `task-progress.md` 或等价进度证据
- 路由到 `mdc-implement`
- 后续应明确 review/gate 顺序
