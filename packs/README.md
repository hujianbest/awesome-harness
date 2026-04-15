# Garage Packs

- 状态: current reference-pack surface
- 日期: 2026-04-11
- 定位: `packs/` 是 `Garage` reference packs 的当前 pack surface，pack-specific 角色、节点、artifact、evidence 与治理 overlay 都应留在各自 pack 下。

## 当前 reference packs

- `packs/product-insights/`
- `packs/experience-design/`
- `packs/coding/`

## 默认 handoff 形状

- `product-insights` 负责机会、wedge、probe 与 `spec-bridge`
- `experience-design` 负责 non-trivial UI 的 `experience-bridge` 与 `UCD`
- `coding` 负责 formal spec、engineering design、tasks、implementation、review 与 gate

默认链路：

- 无 UI 或 trivial UI：`product-insights -> coding`
- non-trivial UI：`product-insights -> experience-design -> coding`

## 边界

这里放：

- pack manifests
- `contracts/manifest.json` 与 pack shell contract 挂点
- pack-local roles / nodes / policies
- pack-local artifact 与 evidence mappings
- continuity candidates 的 pack 输出钩子

这里不放：

- 平台中立 core 逻辑
- 共享 contract 定义
- 与 pack 无关的 host adapter 逻辑
- `src/` 中的 runtime package 代码
