# T000: Garage Tasks

- Task ID: `T000`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: `docs/tasks/` 负责把当前 `Garage` 的产品定义、architecture 主线与 feature 主线拆成 delivery slices，解释先做什么、后做什么，但不反向拥有系统真相。

## 1. 这组文档回答什么

`docs/tasks/` 只回答执行问题：

- 哪些能力应该先做
- 哪些切片可以并行
- 每个切片交付什么
- 当前实现怎样对齐新的 architecture / features 主线

## 2. 阅读顺序

先读：

1. `docs/VISION.md`
2. `docs/GARAGE.md`
3. `docs/architecture/`
4. `docs/features/`
5. 再读 `docs/design/`
6. 最后读 `docs/tasks/README.md`

## 3. 编号规则

- `tasks` 保留 `T` 前缀
- 顶层任务流使用 2 位编号，例如 `T10`、`T11`
- 执行切片使用 3 位编号，例如 `T101`、`T111`
- `docs/tasks/README.md` 继续作为总索引与总排序入口

## 4. owner 边界

- `docs/tasks/` 只负责 delivery slices
- `docs/tasks/` 不定义产品愿景
- `docs/tasks/` 不定义产品是什么
- `docs/tasks/` 不定义 architecture / features 真相
- 当 task 和 design / architecture / features 冲突时，以上游主线为准

## 5. 当前任务流

| 任务流 | 作用 | 上游来源 |
| --- | --- | --- |
| `T10*` | Agent Teams 产品表面 | `F100` |
| `T11*` | runtime topology / bootstrap / entry binding | `F110` |
| `T12*` | Garage Team runtime core | `F120` |
| `T13*` | governance + workspace truth | `F130` |
| `T14*` | continuity + growth | `F140` |
| `T15*` | packs + cross-pack collaboration | `F150` |
| `T16*` | execution + provider/tool plane | `F160` |

## 6. 维护约定

- task docs 保持执行导向，不重复设计长文
- architecture / features / design 主线如果重切，任务树必须跟着重切
- 新增 task doc 时，先更新本页索引与依赖顺序
- 旧任务树若存在，只能作为历史实现参考，不再继续扩展
