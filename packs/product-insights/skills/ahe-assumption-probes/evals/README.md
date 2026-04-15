# Eval: ahe-assumption-probes

## 保护的行为 contract

1. 给定 concept brief，能识别并区分 desirability / usability / viability / feasibility 四类风险
2. 从风险栈中选出最危险的 1-3 个假设，而非列举全部
3. 为每个假设设计带 kill criteria 的低成本探针
4. 若无上游工件，应 reroute 到 `ahe-concept-shaping`

## 运行方式

```bash
# 使用 evals.json 中的 prompt 分别运行 with_skill 和 without_skill
# 对比输出是否满足 assertions
```
