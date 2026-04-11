# Garage Product Insights Pack

- 状态: current reference-pack slice
- 日期: 2026-04-11
- 定位: `packs/product-insights/` 是 `Product Insights Pack` 的当前目录入口，后续承接 framing、research、opportunity、concept、probe 与 bridge 相关实现壳。

## 当前角色

这里是 `Product Insights Pack` 的当前实现面。

当前它与现有资产的关系是：

- `packs/product-insights/skills/` 仍是当前来源资产与参考面
- `packs/product-insights/contracts/` 已承接当前 reference pack 的 role/node/artifact/evidence contracts
- `packs/product-insights/policies/` 承接 pack-local governance overlay
- `packs/product-insights/continuity/` 承接 continuity candidate emission 挂点
- 这里才是后续 `Garage` runtime 中的 pack 落点

## 边界

这里放：

- pack manifest
- `contracts/roles/`、`contracts/nodes/`、`contracts/artifacts/`、`contracts/evidence/`
- pack-local roles / nodes
- 上游 artifact 与 evidence mappings
- pack-local governance overlay
- continuity candidates 的 pack 输出钩子
- bridge-ready 输出钩子

这里不放：

- 平台中立 core 逻辑
- `packs/product-insights/skills/` 的整体直接搬运副本
