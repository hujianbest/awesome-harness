# Increment 评测

## Protected Behavior Contracts

这些评测保护 `ahe-increment` 的以下行为契约：

1. **分支判断**：正确区分 increment（需求变更）与 hotfix（缺陷修复）
2. **失效标记**：范围变化后必须显式标记失效的批准、任务和验证证据
3. **唯一直入节点**：必须选定唯一 canonical re-entry 节点，不写自由文本
4. **最小更新**：只更新最小必要工件，不把 increment 写成第二次从零规格化
5. **状态同步**：Current Stage、Profile、Active Task、Pending Reviews 必须同步
