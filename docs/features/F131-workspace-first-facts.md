# F131: Workspace-First Facts

- Feature ID: `F131`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 workspace-first facts 的稳定语义。

## 1. 这份文档回答什么

为什么 `artifacts / evidence / sessions / archives / .garage` 必须留在 workspace 中，以及它们如何成为团队工作的主事实面。

## 2. owner question

谁拥有工作真相，哪些事实必须人类可读、系统可回读、入口可共享。

## 3. 稳定语义

- artifacts, evidence, sessions, archives, and .garage are workspace facts
- runtime home must not swallow workspace truth
- humans and systems should both be able to inspect core facts

## 4. 最小事实面

- artifacts
- evidence
- sessions
- archives
- .garage

## 5. 边界规则

- workspace facts 优先于宿主缓存
- workspace facts 优先于临时内存状态
- runtime home 不能拥有这些事实的主 authority

## 6. 非目标

- 不要求所有派生状态都进入 workspace facts
- 不把 workspace facts 设计成数据库优先控制面

## 7. Acceptance

- 核心团队工作事实都能在 workspace 中找到
- 不同入口共享同一组 workspace truths
- runtime home 与宿主缓存不会吞掉这些事实
