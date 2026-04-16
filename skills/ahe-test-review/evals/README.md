# 测试评审评测

这个目录包含 `ahe-test-review` 的评测 prompts。

## 目的

这些评测用于验证测试评审是否真正做到：

- 判断 fail-first 有效性、行为覆盖、风险覆盖
- 防止浅层"绿测"冒充可信验证
- 给出明确 verdict 和唯一下一步
- 不在评审中修测试

## 建议评分关注点

1. 是否基于 RED/GREEN 证据判断 fail-first 有效性
2. 是否检查 bug-patterns 风险覆盖
3. 是否给出唯一 canonical 下一步
