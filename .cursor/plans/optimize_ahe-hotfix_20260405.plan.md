# 优化 `ahe-hotfix` 方案

## 目标

把 `skills/ahe-hotfix/SKILL.md` 从“能处理紧急缺陷修复请求”的 skill，提升为“能在紧急场景下稳定做出安全、可追溯、root-cause-first 的热修复判断，并向 `ahe-test-driven-dev` 产出高质量 handoff”的 skill。

本次优化不改变 AHE 主链契约：

- 仍然由 `ahe-hotfix` 负责热修复分析、复现、范围收敛和状态写回
- 仍然只有 `ahe-test-driven-dev` 是唯一实现入口
- 仍然不能因为“紧急”就放弃 fail-first、验证和后续门禁
- 仍然由 `ahe-workflow-starter` 统一拥有后续恢复编排权

## 当前问题

当前 `ahe-hotfix` 已经强调“先复现、最小修复、再验证”，但还存在几个高价值短板：

- 复现和修复边界被提到，但 root cause 还不够显式，容易滑向症状修补
- 缺少“无法稳定复现 / 间歇性问题”时的暂停和升级协议
- 输出格式能表达热修概要，但还不够像一份可被 `ahe-test-driven-dev` 直接消费的 handoff
- 缺少 blast radius、回滚 / feature flag、监控补位等紧急修复高价值信息
- 与 `ahe-increment` 的边界不够清楚，容易把“需求/验收变了”误判成热修
- `Next Action Or Recommended Skill` 还没有足够明确地收紧到 canonical `ahe-*` skill ID

## 优化方向

### 1. 增加 root cause 纪律

要求热修分析至少走完：

- 现象
- 证据
- 当前假设
- 最小验证
- 已确认 root cause

为什么这么改：

- 高质量热修不是“先打补丁压住”，而是先确认问题到底出在哪
- 这能显著减少症状修补和范围外改动

主要参考：

- `references/gstack-main/investigate/SKILL.md`
- `references/superpowers-main/skills/systematic-debugging/SKILL.md`
- `references/longtaskforagent-main/skills/long-task-hotfix/SKILL.md`

### 2. 增加“无法稳定复现 / 间歇性问题”协议

当问题无法稳定复现时，要求至少记录：

- 环境
- 触发条件
- 已尝试的复现步骤
- 当前证据缺口
- 为什么此时不能直接进入实现

为什么这么改：

- 热修场景最容易因为紧急而跳过这一步
- 但如果连问题是否存在、何时出现都不稳定，就不应直接进入代码修复

主要参考：

- `references/gstack-main/investigate/SKILL.md`
- `references/longtaskforagent-main/skills/long-task-hotfix/SKILL.md`

### 3. 把输出升级成可执行 handoff

输出格式要能直接支持 `ahe-test-driven-dev`，至少显式写明：

- Hotfix ID / Task ID
- 回流来源 `ahe-hotfix`
- 复现步骤与失败签名
- 已确认 root cause
- 最小修复边界
- blast radius / out-of-scope
- 最新验证证据
- canonical `Next Action Or Recommended Skill`

为什么这么改：

- 这样热修 skill 的结果才不只是“分析摘要”，而是可继续执行的上游工件
- 也能减少实现阶段重新补齐上下文

主要参考：

- `skills/ahe-test-driven-dev/SKILL.md`
- `references/superpowers-main/skills/verification-before-completion/SKILL.md`

### 4. 增加 hotfix / increment 边界判断

明确区分：

- 这是实现缺陷，还是需求 / 验收 / 范围变化
- 若本质是增量或规则变更，应回到 `ahe-increment` 或 `ahe-workflow-starter`

为什么这么改：

- 热修分支如果接管了变更请求，会直接破坏主链稳定性

主要参考：

- `skills/ahe-increment/SKILL.md`
- `skills/ahe-workflow-starter/SKILL.md`

### 5. 强化 hotfix 阶段自己的 fresh evidence

在说“已经复现”“已经理解问题”“修复边界已确认”之前，要求：

- 给出命令 / 操作入口
- 说明结果
- 保留短证据摘要

为什么这么改：

- 热修场景里最容易把“我看懂了”当成证据
- 需要在进入实现前就把分析阶段的证据做实

主要参考：

- `references/superpowers-main/skills/verification-before-completion/SKILL.md`
- `skills/ahe-hotfix/SKILL.md`

### 6. 增加 blast radius 与回滚意识

至少要求说明：

- 影响模块 / 文件范围
- 是否存在 feature flag / 回滚手段
- 修复后需要关注的监控 / 验证点

为什么这么改：

- 紧急修复最怕修复本身引入更大的运营风险

主要参考：

- `references/gstack-main/investigate/SKILL.md`
- `docs/skills_refer.md`

### 7. 明确后续链路提示但不抢 starter 的权

保留“通常下一步”的提示，例如：

- 多数热修分析完成后先进入 `ahe-test-driven-dev`
- 完成实现后再由 starter 判断是否进入 `ahe-bug-patterns`、`ahe-regression-gate` 等

为什么这么改：

- 既能减少 `Next Action` 的自由文本漂移
- 又不会抢走 `ahe-workflow-starter` 的恢复编排权

主要参考：

- `skills/ahe-workflow-starter/SKILL.md`
- `skills/ahe-test-driven-dev/SKILL.md`

## 明确不做的事

- 不在 `ahe-hotfix` 内直接写生产代码
- 不新增第二条实现入口
- 不把热修 skill 写成完整的运维事件管理手册
- 不替代 `ahe-bug-patterns`、`ahe-regression-gate` 或 `ahe-completion-gate`

## 计划中的实际改动

会对 `skills/ahe-hotfix/SKILL.md` 做一轮聚焦增强，预计包括：

- 增加 root cause-first 纪律
- 增加无法稳定复现时的暂停协议
- 升级输出格式为可执行 hotfix handoff
- 增加 hotfix / increment 边界判断
- 强化分析阶段的 fresh evidence
- 增加 blast radius / 回滚 / 监控提示
- 收紧 canonical 下一步 skill 的写法

## 预期效果

优化后的 `ahe-hotfix` 应该具备这些特征：

- 不只是“先复现再修”，而是能稳定做出更安全的热修判断
- 更少出现症状修补、机会式扩改和自由文本 handoff
- 更容易把热修分析结果交给 `ahe-test-driven-dev` 和后续质量链直接消费
- 在紧急情况下仍保持 AHE 主链契约不变形
