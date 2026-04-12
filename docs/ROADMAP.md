# M040: Garage Feature Roadmap

- Document ID: `M040`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: `docs/ROADMAP.md` 维护新的 feature families、它们和 architecture 主线的关系，以及这些 capability docs 当前由哪些任务切片承接。
- 关联文档:
  - `docs/README.md`
  - `docs/VISION.md`
  - `docs/GARAGE.md`
  - `docs/tasks/README.md`

## 1. 这份文档回答什么

这份文档主要回答 3 个问题：

- 新的 `docs/features/` 主线怎么切
- 各 capability family 对应哪些 architecture owner docs
- 当前任务链大致承接了哪些 capability family

它不替代：

- `docs/GARAGE.md` 的产品定义
- `docs/tasks/README.md` 的实施顺序索引
- 每篇 feature 文档自身的详细语义

## 2. 新的 feature 原则

- `docs/features/` 跟随新的 architecture 主线，不再继承旧 `F010-F230` 的切分逻辑。
- 它讲的是稳定 capability families，不是阶段性开发故事。
- 当 feature 语义和 task 语义冲突时，以 `docs/features/` 为准，再回头重切 `docs/tasks/`。
- feature 文档应回答 “系统需要具备什么能力语义”，而不是 “当前代码已经怎么写”。

## 3. 编号规则

新的 `docs/features/` 仍使用：

- `FNNN-<topic>.md`

但当前主线改成围绕新的 capability families 展开，统一收口在：

- `F100-F199`

## 4. 当前 Feature Families

| ID | Feature family | 作用 | 对应 architecture 主线 | 当前实施切片 |
| --- | --- | --- | --- | --- |
| `F100` | Agent Teams Product Surface | 定义产品入口、团队对象、独立工作环境与能力注入层 | `1`、`10` | `T140`、`T150`、`T160` |
| `F110` | Runtime Topology And Entry Bootstrap | 定义 runtime home / workspace / bootstrap / SessionApi 的共享主线 | `10`、`11`、`101` | `T110`、`T120`、`T140`、`T150`、`T160`、`T170` |
| `F120` | Garage Team Runtime Core | 定义 neutral records、session、handoff、registry 与团队协作核心 | `2`、`11`、`102` | `T020`、`T030`、`T040` |
| `F130` | Governance And Workspace Truth | 定义 governance、artifact routing、workspace-first facts 与 evidence surface | `20`、`30`、`104`、`105` | `T040`、`T050`、`T100`、`T110` |
| `F140` | Continuity And Growth | 定义 `memory / skill / evidence / GrowthProposal` 与长期成长主线 | `21`、`31`、`106` | `T060`、`T080`、`T090`、`T130` |
| `F150` | Pack Platform And Collaboration | 定义 packs、contracts、reference packs 与 cross-pack collaboration | `40`、`41`、`107`、`111` | `T030`、`T070`、`T080`、`T090`、`T100` |
| `F160` | Execution And Provider Tool Plane | 定义 provider authority、tool execution、execution trace 与 evidence-linked outcomes | `12`、`103` | `T130`、`T170`、`T180`、`T200`、`T201` |

## 5. 阅读顺序

建议这样读：

1. `docs/VISION.md`
2. `docs/GARAGE.md`
3. `docs/architecture/`
4. `docs/features/F100 -> F160`
5. `docs/design/README.md`
6. `docs/tasks/README.md`

## 6. Feature 与 Task 的关系

`docs/features/` 负责稳定 capability cuts。  
`docs/design/` 负责把这些 capability cuts 进一步解释成产品/交互与详细设计。  
`docs/tasks/` 负责把这些 capability cuts 按交付顺序拆成 implementation slices。

这意味着：

- 先用 features 理解系统应该具备什么能力
- 再用 design 理解这些能力如何被产品化和详细化
- 最后用 tasks 理解当前先交付哪一部分

## 7. 后续 feature 扩展建议

未来新增 feature docs 时，建议继续按 capability family 扩展，而不是恢复旧的 runtime-first 清单式切法。

优先扩展方向包括：

- 更完整的 WebEntry capability family
- 更细的 host injection / host adapter family
- release / ops / diagnostics family
- 更明确的 runtime update / evolution family

## 8. 一句话总结

新的 `docs/ROADMAP.md` 不再维护旧 `F010-F230` feature map，而是维护跟随新 architecture 主线的 capability families，让 features 真正从产品与架构源头推导出来。
