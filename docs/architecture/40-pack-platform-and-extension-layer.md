# 40: Pack Platform And Extension Layer

- Architecture Level: `L1`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 回答 `Garage Team` 如何通过 packs、contracts 和 registry 持续扩展新能力面。
- 关联文档:
  - `docs/GARAGE.md`
  - `docs/architecture/2-garage-runtime-reference-model.md`
  - `docs/architecture/110-pack-runtime-binding.md`

## 1. owner question

新能力如何进入系统，而不污染 core 或推翻团队模型。

## 2. 关键判断

- packs extend team capability, not core truth
- contracts provide neutral shared language
- registry discovers and validates capability surfaces
- new domains should enter by extension, not by rewriting the platform

## 3. 非目标

- 不把 pack 变成 vendor authority
- 不把平台重写成 plugin market
