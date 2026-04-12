# F112: Bootstrap And Runtime Profile

- Feature ID: `F112`
- 状态: 草稿
- 日期: 2026-04-11
- 定位: 定义 bootstrap 责任链与 `RuntimeProfile` authority 的稳定语义。

## 1. 这份文档回答什么

启动时谁先解析、谁拥有 authority、哪些输入可以是 default，哪些必须显式提供。

## 2. owner question

bootstrap 和 `RuntimeProfile` 的边界应该怎么切，才能让不同入口共用同一条启动与 authority 链。

## 3. 稳定语义

- bootstrap resolves topology before work starts
- `RuntimeProfile` owns provider/model authority
- host hints cannot override profile authority

## 4. 最小责任顺序

1. 解析 source root / runtime home / workspace topology
2. 解析 `RuntimeProfile`
3. 绑定 host adapter
4. 暴露 `SessionApi`
5. 再进入 session-bound work

## 5. authority 边界

- profile 可以决定 provider/model defaults
- host 只能提供非权威 hint
- packs 不能拥有 vendor 选择权

## 6. 非目标

- 不把 bootstrap 扩成业务能力解释层
- 不把 host hint 当作 authority 覆盖
- 不让入口私自定义自己的 bootstrap 主链

## 7. Acceptance

- 不同入口复用同一 bootstrap 责任顺序
- provider/model authority 有单一 owner
- 入口与宿主不能通过局部实现绕过 `RuntimeProfile`
