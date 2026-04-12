# 107: Pack Runtime Binding

- Architecture Level: `L2`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 展开 packs、contracts、registry 与 team runtime 的绑定方式。
- 关联文档:
  - `docs/architecture/40-pack-platform-and-extension-layer.md`

## 1. owner question

新 pack 如何接入 Garage Team runtime，而不破坏 core neutrality。

## 2. 关键判断

- packs bind through contracts and registry
- packs extend capability, not platform truth
- pack-local language must not leak into core
