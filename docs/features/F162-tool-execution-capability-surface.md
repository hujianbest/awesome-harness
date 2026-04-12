# F162: Tool Execution Capability Surface

- Feature ID: `F162`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 tool execution capability surface 的稳定语义。

## 1. 这份文档回答什么

tools 在系统里到底是什么对象，packs / hosts / execution 分别怎样与它们发生关系。

## 2. owner question

tool capability surface 应由谁定义，谁可以请求它，谁可以限制它，谁不能重写它。

## 3. 稳定语义

- tools are runtime capabilities
- packs request capabilities, not implementations
- hosts may constrain capabilities but not redefine them

## 4. 最小关系

- packs request capabilities
- runtime registers and exposes capabilities
- execution invokes capabilities
- hosts may locally constrain exposure

## 5. 边界规则

- capability != concrete implementation
- host constraint != capability ownership
- execution invokes tools, but governance still constrains work

## 6. 非目标

- 不把 tool capability 面退化成 provider 私有插件列表
- 不让 packs 或 hosts 直接拥有实现选择权

## 7. Acceptance

- tool capability surface 有清楚的 owner 和边界
- packs / hosts / execution 的关系不再混写
- 下游 design 可以在不补脑的前提下继续展开具体工具面
