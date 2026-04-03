# AHE Skills

`skills/` 用于存放 `awesome-harness-engineering`（`ahe`）仓库自己的可复用 skill 资产，以及直接服务于这些 skill 的设计规则。

## 目录约定

- `skills/README.md`：本目录总览
- `skills/design_rules.md`：skill 与 harness 资产的设计原则
- `skills/<skill-name>/SKILL.md`：单个 skill 的入口文件
- `skills/<skill-name>/references/`：该 skill 的补充说明、模板或参考资料

## 当前状态

旧的 `mdc-*` workflow skills 已移除。当前 `skills/` 目录保留为通用 skill 工作区，后续新增内容应直接遵循当前结构，不再依赖历史命名或已删除路径。

## 新增 skill 时的建议

1. 先明确 skill 只解决一个清晰问题。
2. 入口统一放在 `skills/<skill-name>/SKILL.md`。
3. 大段参考资料、模板和案例放到同目录下的 `references/`。
4. 文档中的路径始终引用当前仓库真实存在的位置。
5. 如果需要校验或打包，使用 `.cursor/skills/skill-creator/` 下的脚本，而不是在本目录重复造工具。

## 不再使用的历史约束

- 不再引用 `skills/mdc-workflow/...`
- 不再要求 `mdc-workflow-starter`
- 不再默认存在 `daily-skills/`、`playbooks/` 或其他旧结构
