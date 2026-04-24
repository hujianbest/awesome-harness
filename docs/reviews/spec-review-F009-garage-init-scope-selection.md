# Spec Review — F009 `garage init` 双 Scope 安装（project / user）+ 交互式 Scope 选择

- 评审目标: `docs/features/F009-garage-init-scope-selection.md`（草稿 r1，2026-04-23）
- Reviewer: 独立 reviewer subagent（按 `hf-spec-review` skill 执行）
- 评审时间: 2026-04-24
- 上游证据基线:
  - `task-progress.md`（Stage=`hf-specify` / Profile=`full` / Mode=`auto`）
  - `docs/features/F008-garage-coding-pack-and-writing-pack.md`（已批准，§ 5 deferred 第 3 行明确指向 F009）
  - `docs/features/F007-garage-packs-and-host-installer.md`（已批准；FR-705 manifest schema / CON-703 / FR-708 marker / FR-704 5-phase 管道）
  - `src/garage_os/adapter/installer/{pipeline,host_registry}.py` + `hosts/{claude,opencode,cursor}.py`（F007 实现入口，已确认 `target_skill_path` / `target_agent_path` 既有签名为 project-root-relative `Path`）
  - `.gitignore` L34 实测：`.garage/config/host-installer.json` 不入 git
  - `docs/soul/{manifesto,user-pact,design-principles,growth-strategy}.md`（workspace-first vs "你做主" / "数据归你" trade-off 锚点）

## Precheck

- [x] 存在稳定 spec 草稿：10 FR + 4 NFR + 4 CON + 4 ASM + 8 项 § 11 非阻塞开放问题，结构骨架对齐项目模板
- [x] route / stage / profile 明确：`task-progress.md` 显示 Stage=`hf-specify`, Profile=`full`, Mode=`auto`，Next Action=`hf-spec-review`
- [x] 上游证据不冲突：F008 closeout 633 测试通过 + spec § 5 deferred 第 3 行 + F007 安装管道实测代码与 spec 描述一致

Precheck **PASS**，进入正式 rubric 审查。

## 结论

需修改

verdict 理由：F009 spec 范围清晰、动机充分（solo creator 跨多客户项目摩擦实测可验证）、与 F007/F008 既有契约边界明确（§ 4.3 表逐项标注影响 / 不变）、deferred backlog 完整、ASM/CON 显式可回读、11 项 success criteria 可派生为验收、8 项 § 11 非阻塞 design 决策每项均带默认值（设计可消化）。但发现 **4 条 important LLM-FIXABLE** finding 集中在 (a) **CON-901/NFR-901 "字节级一致" 与 FR-905 manifest schema migration 的概念边界模糊**、(b) **CON-902 "phase 5 算法字节级保持" 与 FR-905 manifest schema 升级的执行时序未澄清**、(c) **FR-903 交互式两轮提示缺 "all P / all u" 快捷路径的设计决策点未列**、(d) **dogfood 不破坏的硬约束缺独立验收 anchor**；以及 5 条 minor LLM-FIXABLE 边界细化。无 critical、无 USER-INPUT、无 route/stage/证据冲突。所有 finding 都能在 1 轮定向回修内闭合，不破坏核心范围、不引入新业务事实，因此判 `需修改` 而非 `阻塞`。

## 发现项

### Critical

无 critical 级 finding。

### Important

- [important][LLM-FIXABLE][C2/C7] **CON-901 / NFR-901 "字节级一致" 与 FR-905 manifest schema migration 的概念边界模糊**：
  - NFR-901 验收 #1 写 "F008 cycle 期间录制的 `garage init --hosts claude` 端到端 stdout/stderr 副本... F009 实施后再跑同样命令... 字节级一致（除 stdout 中可变 path 部分）"，验收 #2 写 "F007/F008 既有 30+ installer 测试 100% 通过且 0 改写"。
  - 但 FR-905 同时承诺 "F008 用户已落下的 schema 1 manifest，F009 第一次 init 自动迁移到 schema 2，旧 entry 全部 `scope: "project"` + dst 由 relative 转 absolute"。
  - 矛盾点：(a) F008 用户首次跑 F009 init 时 `.garage/config/host-installer.json` 文件**内容必然变化**（schema_version 1→2、dst relative→absolute、新增 scope 字段），与 NFR-901 "`.garage/` 目录创建" 字节级一致措辞冲突；(b) F007/F008 既有测试若含 manifest 字段断言（如 `dst: ".claude/skills/garage-hello/SKILL.md"` 这种 relative path 字面值），在 F009 schema 2 下必然失败，与 NFR-901 验收 #2 "0 改写" 冲突。
  - 修复指引：在 NFR-901 验收陈述中显式枚举 "字节级一致" 的 manifest 例外，明确 `.garage/config/host-installer.json` 的内容会因 schema migration 而变化，但 stdout / stderr / exit code / `<cwd>/.{host}/skills/<id>/SKILL.md` 文件落盘字节不变；并把 "0 改写" 松绑为 "0 语义退绿，schema migration 引起的 manifest 字段断言可机械适配"。
  - 锚点：F009 spec L391-399（NFR-901）、L322-336（FR-905）、L437-442（CON-901）。

- [important][LLM-FIXABLE][C2/A3] **CON-902 "phase 5 算法主体字节级保持" 与 FR-905 manifest schema 升级的执行时序未澄清**：
  - CON-902 + FR-906 验收 #1 写 "phase 5 (apply + manifest) 的算法主体字节级保持原状（仅 type signatures 因 `_Target` 增 scope 字段而扩展）"。
  - FR-905 同时承诺 manifest schema 1→2 升级 by `VersionManager` 自动 migration。
  - 但 spec 未明确：(a) `VersionManager.migrate` 调用时机 — 是 `garage init` 入口的 phase 0（pipeline 之前预处理）？还是 phase 5 manifest write 内部？(b) phase 5 写出的 manifest 字段集合（schema_version、dst 形态、scope 新字段）已发生改变，"字节级保持" 的语义边界是 "phase 5 的核心循环 / 错误分支结构不变" 还是其他？仅说 "type signatures 扩展" 在 phase 5 这里似乎覆盖不足 — 写入 schema 与序列化形式都变了，并非只是签名扩展。
  - 修复指引：在 FR-906 / CON-902 / FR-905 之间加一条 ordering anchor，例如 "FR-905 migration 发生在 pipeline 入口（phase 0），写入 manifest 时 phase 5 直接按 schema 2 写"；并把 FR-906 验收 #1 中 "字节级保持原状" 改为 "phase 5 的核心循环结构 / 写入顺序 / 错误分支与 F007/F008 等价，仅写入的 schema 升至 2 + 字段集合按 FR-905 扩展"。这样 design 阶段 reviewer 不会因 "phase 5 字面字节级 vs 写出 schema 必然变" 的冲突把 design 拒回 spec。
  - 锚点：F009 spec L444-449（CON-902）、L337-345（FR-906）、L322-336（FR-905）、L83-85（§ 2.2 #11）。

- [important][LLM-FIXABLE][Q3/C2] **FR-903 交互式 per-host scope 选择缺 "全选 P / 全选 u" 快捷路径设计决策点**：
  - FR-903 + § 3.2 场景 #5 描述：用户选 N 个宿主后，对每个宿主独立提示 `[P/u]`。N=3（claude + cursor + opencode）时，用户需要回答 3 次 P/u；FR-903 验收 #2 默认全部回车 = 全 project。
  - 缺口：(a) 没有 "all P" / "all u" 一键快捷选项；(b) § 11 非阻塞 #5 留 "两轮 vs 一轮带 scope 后缀" 给 design，但没显式列出 "是否提供 all-project / all-user / per-host 三选一开关" 这第三个 design 决策点 — design 阶段 reviewer 可能反问 "为何没考虑批量"。
  - 修复指引：把 § 11 非阻塞 #5 wording 扩展为 "两轮 vs 一轮带 scope 后缀 vs 三选一开关（all-project / all-user / per-host），design 决定"；或在 FR-903 验收 / 边界中显式声明 "design 可选择是否引入批量快捷选项，spec 不强约束"。这是 LLM-FIXABLE wording 微调，不需要新业务输入。
  - 锚点：F009 spec L297-306（FR-903）、L141-149（§ 3.2 场景 #5）、L515（§ 11 非阻塞 #5）。

- [important][LLM-FIXABLE][C6/C2] **dogfood 不破坏的硬约束缺独立验收 anchor**：
  - § 2.2 #9 + § 3.2 场景 #12 + § 4.3 表 "F008 ADR-D8-2 dogfood 候选 C — 保留" + CON-901 都从语义上承诺 "本仓库自身 `garage init --hosts cursor,claude` 仍 project scope，与 F008 完全等价"。
  - 但没有任何独立 FR / NFR 验收给出可机械守门的检查，例如 "在 `cwd=/workspace` 跑 `garage init --hosts cursor,claude` 后产物（`.cursor/skills/` + `.claude/skills/` + `.garage/config/host-installer.json` 的 schema 2 形态）与 F008 closeout commit 的 dogfood baseline 在 (a) skill SKILL.md 字节、(b) agent 字节、(c) manifest schema 2 等价语义下 diff 为空（除可变 path 部分）"。
  - 风险：到 design / regression-gate 时缺 anchor，reviewer 与实施者对 "dogfood 不变" 的具体含义可能各自理解；本仓库 IDE 加载入口若被 F009 静默改变（如某 marker 文本变化）会延迟到 PR review 才发现。
  - 修复指引：在 NFR-901 验收追加一条独立守门，例如 "**Dogfood 不变性守门**：在 `cwd=/workspace` 跑 `garage init --hosts cursor,claude` 后，`.cursor/skills/` + `.claude/skills/` + `.claude/agents/` 下所有文件字节与 F008 closeout commit `bafbd1c` 父链的 dogfood baseline 字节级一致；`.garage/config/host-installer.json` 在 schema 2 升级后语义等价（旧 entry 全部 `scope: "project"` + dst absolute；其它字段一致）"；或单独抽一条 NFR-905。
  - 锚点：F009 spec L83（§ 2.2 #9）、L196-202（§ 3.2 #12）、L248（§ 4.3 表 dogfood 行）、L391-399（NFR-901）、L437-442（CON-901）。

### Minor

- [minor][LLM-FIXABLE][C7/A3] **FR-909 多 scope stdout 附加段未约束行结构，可能影响 F007 下游 grep 兼容**：
  - FR-909 验收 #1 已守门 "单 scope 时不附加（与 F007 字节级一致，CON-901）"。但混合 scope 时附加段（spec 默认 wording `(N_user user-scope, N_project project-scope)`）的行结构未约束 — 接续在 `Installed N skills...` 同一行 vs 新起一行直接影响 F007/F008 下游脚本既有 grep `Installed.*skills` 是否还能命中且字段顺序不变。
  - 修复指引：在 FR-909 验收追加 "附加段必须独占新行，F007 既有 grep `Installed.*skills, .* agents into hosts:` 在单 scope 与混合 scope 下均一行命中且字段顺序不变；附加段作为独立可 grep 的新行（如 `Scope distribution: N_user user-scope, N_project project-scope`）"；具体 wording 仍可由 design 收敛，但 "独占新行 + F007 既有 grep 不破坏" 应作为 spec 层不变量。
  - 锚点：F009 spec L367-373（FR-909）、L513（§ 11 非阻塞 #3）。

- [minor][LLM-FIXABLE][Q3/C2] **per-host scope override 语法 `<host>:<scope>` 与未来宿主 host_id 含 `:` 的兼容性边界缺显式记录**：
  - F007 既有三家 host_id（claude / opencode / cursor）都不含 `:`，FR-902 语法在当前注册表下无歧义。但 spec § 4.2 关键边界未声明 "未来引入新宿主时 host_id 不得含 `:` 字符" 这条约束，将给后续宿主扩展留隐性陷阱。
  - 修复指引：在 § 4.2 关键边界加一行约束 "未来在 host registry 引入新宿主时，`host_id` 不得含 `:` 字符以保留 FR-902 per-host scope override 语法 `<host>:<scope>` 的无歧义解析"；或在 § 11 非阻塞列入 design 注意点。LLM 可写，无业务输入。
  - 锚点：F009 spec L286-295（FR-902）、L221-231（§ 4.2）。

- [minor][LLM-FIXABLE][C7] **NFR-902 测试基线 "≥ 633 + 新增" 缺增量量级预估**：
  - F008 增量是 +47（633 = 586 + 47）。F009 design 阶段会更精确，但 spec 是否需给个量级预期供 task-board 早期估算？当前 NFR-902 仅写 "≥ 633 + 新增"，没有量级 anchor。
  - 修复指引：在 NFR-902 详细说明加一句 "新增测试预期量级约 30-60 个（覆盖三家 adapter user scope path × 2 method + flag 解析 + per-host 语法 + 交互两轮 + manifest 1→2 migration + 幂等分 scope + status 分组 + Path.home() RuntimeError + fixture 隔离），最终数由 design / tasks 阶段精确化" 作为 informational 锚点。这不是硬约束，仅供 task-board 早期估算。
  - 锚点：F009 spec L401-409（NFR-902）。

- [minor][LLM-FIXABLE][C2/C7] **manifest absolute path 跨用户不可移植性的预期未显式说明**：
  - § 11 非阻塞 #4 留 design 决定 "manifest serialization 时是否把 home 部分还原为 `~/...`"，但 spec 没显式说明 "manifest 在 git track 与否 / 跨用户 clone 场景的 F009 立场"。实测：本仓库 `.gitignore` L34 已排除 `.garage/config/host-installer.json`，dogfood 仓库不入 git；但下游用户场景多样，有人会 commit 该文件作为 "team baseline"。
  - 修复指引：在 ASM 段加一条 ASM-905（或在 § 4.2 加一行）："manifest 默认不入 git（与 dogfood 仓库 `.gitignore` 实测一致），跨用户 clone 不是 F009 必须支持的场景；下游用户若自行 commit manifest，跨用户 user-scope absolute path 不可移植由用户自行承担"。这是 LLM 可写的预期声明，避免 design / future bug 时被反问。
  - 锚点：F009 spec L514（§ 11 非阻塞 #4）、`.gitignore` L34 实测。

- [minor][LLM-FIXABLE][A6] **FR-903 non-TTY 退化路径是否在 stderr 提示 "scope 选择被跳过" 未约束**：
  - FR-903 验收 #4 写 "non-TTY 沿用 F007 FR-703 退化（`--hosts none` + stderr 提示），不进入第二轮 scope 提示"。但 stderr 提示是否提示 scope 选择被跳过 / 提示用户应显式传 `--scope` 未约束，影响 CI / Cloud Agent 用户调试体验。
  - 修复指引：在 FR-903 验收 #4 加一条 "non-TTY 退化时 stderr 提示文本应同时包含 `--hosts` 与 `--scope` 两个建议 flag（或显式说明 scope 默认 project 不需 flag），让 CI 用户从 stderr 直接看到完整非交互调用模板"。LLM 可写。
  - 锚点：F009 spec L297-306（FR-903 验收 #4）。

## 缺失或薄弱项

1. **CON-901/NFR-901 "字节级一致" 与 FR-905 manifest schema migration 的概念边界**（见 important #1）。spec 未显式枚举 manifest 是 "字节级一致" 的合法例外。
2. **CON-902 "phase 5 算法字节级保持" 与 FR-905 schema 升级的执行 ordering anchor**（见 important #2）。spec 未澄清 `VersionManager.migrate` 调用时机与 phase 5 写入 schema 2 的边界。
3. **FR-903 交互式批量快捷路径的 design 决策点未列**（见 important #3）。
4. **dogfood 不破坏的独立验收守门 anchor**（见 important #4）。
5. **per-host scope override 语法对 future host_id 命名的隐性约束未声明**（见 minor #2）。
6. **测试基线增量量级未给 informational anchor**（见 minor #3）。
7. **manifest 跨用户 / git track 立场未显式声明**（见 minor #4）。
8. **non-TTY 退化路径 stderr 提示完整性未约束**（见 minor #5）。

## 下一步

`hf-specify`（按本 review 的 4 important + 5 minor 做 1 轮定向回修；预计回修后即可 `通过`）

回修建议聚焦：
- 把 NFR-901 "字节级一致" 显式枚举 manifest 例外；旧测试 "0 改写" 松绑为 "0 语义退绿"（important #1）
- 把 CON-902 / FR-906 验收 #1 / FR-905 三处加 ordering anchor，澄清 migration 调用时机 + phase 5 字节级语义（important #2）
- 把 § 11 非阻塞 #5 wording 扩展三选一 design 决策点；FR-903 不强约束（important #3）
- 在 NFR-901 加 "Dogfood 不变性守门" 验收 anchor（或单独 NFR-905）（important #4）
- 5 条 minor 一并按修复指引微调

回修期间不需向真人提任何 USER-INPUT 问题——所有 finding 均 LLM-FIXABLE。8 项 § 11 非阻塞放权 design 与 spec 默认值合理，不需提前升级为 USER-INPUT。

## 记录位置

`docs/reviews/spec-review-F009-garage-init-scope-selection.md`

## 交接说明

- `规格真人确认`：本轮 verdict = `需修改`，不进入。
- `hf-specify`：父会话应把本 review 记录路径与 4 important + 5 minor 全部回传给负责 spec 修订的会话；预计 1 轮定向回修 + 1 轮 review 即可冻结进入 design。
- `hf-workflow-router`：route / stage / 证据无冲突，不需要 reroute（`reroute_via_router=false`）。
- 不修改 `task-progress.md`、不修改 F009 spec 文档、不 git commit / push（由父会话执行）。

---

## 复审 r2

- 复审时间: 2026-04-24
- 复审目标: 验证父会话在 commit `24cdb7f` 中针对 r1 的 4 important + 5 minor finding 是否全部闭合
- Reviewer: 同 r1 独立 reviewer subagent
- 复审范围: **仅** r1 finding 闭合状态 + 是否引入新风险；不重新执行 Q/A/C/G 全量 rubric

### 结论

通过

verdict 理由：r1 列出的 4 important + 5 minor 全部 LLM-FIXABLE finding 已全部闭合到 acceptance shape 层；NFR-901 manifest migration 边界澄清 + Dogfood 不变性硬门槛 + CON-902 phase 5 ordering anchor + § 11 非阻塞 #5 三选一扩展 + FR-909 grep 兼容守门 + § 4.1 host_id 命名约束 + NFR-902 增量量级 anchor + CON-904 跨用户立场 + FR-903 non-TTY stderr 字面要求全部落到位。回修过程未引入新设计泄漏、未引入新模糊词、未破坏 deferred backlog 范围、未发明业务事实；所剩仅 1 条**叙事 narrative gap** 新风险（FR-906 验收 #1 wording 与 CON-902 phase 5 enum 精度 gap），不属于 acceptance / 验收硬约束、不影响 design 启动判断，故判 `通过`，下一步 `规格真人确认`。

### 9 条 r1 finding 闭合状态

| # | r1 finding | 闭合状态 | 证据锚点（F009 spec 行号）|
|---|---|---|---|
| 1 | [important][LLM-FIXABLE][C2/C7] NFR-901 字节级一致 vs FR-905 manifest schema migration 边界 | **已闭合** | L397-399 新增 "明确例外（schema migration）" 段显式枚举允许差异（schema_version 1→2、dst relative→absolute、新增 scope 字段）；L402 验收 #2 "0 改写" → "0 语义退绿" + carry-forward LLM-FIXABLE wording 同步必须 commit message 声明 |
| 2 | [important][LLM-FIXABLE][C2/A3] CON-902 phase 5 字节级 vs FR-905 schema 升级 ordering anchor | **已闭合** | L450-461 CON-902 标题加 "（除 phase 2 scope 分流 + phase 5 schema migration 调用）"；显式 enum phase 2 (`_resolve_targets`) / phase 4 (`_decide_action` 比对 key 4→5 元组) / phase 5 (apply + manifest 写入 schema 2) 各自允许的最小改动；phase 1 (discover) + phase 3 (conflict) 严格不动；phase 5 内 `VersionManager.migrate_host_installer_manifest(prior, target_version=2)` 调用 ordering 锚定（在写入新 manifest 之前先迁移）；migration 失败 → ManifestMigrationError → CLI exit 1（具体 ManifestMigrationError 类型与退出码常量由 design 决定，但 spec 已锚定语义）|
| 3 | [important][LLM-FIXABLE][Q3/C2] FR-903 批量快捷路径 design 决策点 | **已闭合** | L528-532 § 11 非阻塞 #5 扩展为三选一（候选 A 两轮 / 候选 B 一轮带后缀 / 候选 C 两轮+all P/all u/per-host 三开关），显式声明 "design 决定，前提是 FR-903 验收 #1-#4 均满足（特别 default = project 兼容 F007/F008）" |
| 4 | [important][LLM-FIXABLE][C6/C2] dogfood 不破坏独立验收 anchor | **已闭合** | L404 NFR-901 验收 #4 新增 "Dogfood 不变性硬门槛" 条款：本仓库自身 `garage init --hosts cursor,claude` 后 `.cursor/skills/` + `.claude/skills/` + `.claude/agents/` 落盘 SHA-256 与 F008 dogfood baseline (`/opt/cursor/artifacts/f008_dogfood_init.log` 时点) 一致；manifest schema_version 允许 1→2 但 `files[].host` + `files[].scope: "project"` + `files[].content_hash` 必须保持稳定 |
| 5 | [minor][LLM-FIXABLE][C7/A3] FR-909 多 scope 附加段必须独立行 | **已闭合** | L366-374 FR-909 标题改 "stdout marker 派生（保持 F007 grep 兼容）"；需求陈述 "stdout 必须**在另一行**附加 scope 分布说明" + "不允许把附加内容塞进同一行的 F007 marker"；验收 #2 / #3 强约束 `grep -cE '^Installed [0-9]+ skills, [0-9]+ agents into hosts:'` 命中数 == 1（恰好 F007 marker 那一行） |
| 6 | [minor][LLM-FIXABLE][Q3/C2] per-host override 语法 host_id 不允许 `:` 字符约束 | **已闭合** | L211 § 4.1 表 per-host override 行加约束 "未来新增 host_id 不允许包含字面 `:` 字符（spec-review-F009 r1 minor #2 显式约束；当前 first-class 三家 claude/opencode/cursor 均符合，未来 host adapter 注册必须遵守此命名约束，由 design 在 ADR 锚定）" |
| 7 | [minor][LLM-FIXABLE][C7] NFR-902 增量量级 informational anchor + "0 语义退绿" | **已闭合** | L411 加 "预期增量量级（informational anchor，非硬约束）：参考 F008 +47 增量，F009 预期增量 ≥ 25（7 类新模块 × 平均 3-5 用例 + manifest migration + per-host syntax + dogfood 不变性 sentinel ≈ 30）；实际增量数由 design / hf-tasks 阶段精确定"；L413 验收 "0 退绿" → "0 语义退绿"，与 NFR-901 carry-forward 例外路径呼应 |
| 8 | [minor][LLM-FIXABLE][C2/C7] CON-904 跨用户可移植性立场 | **已闭合** | L470-476 CON-904 标题加 "+ 跨用户可移植性立场"；新增段显式声明 manifest 默认不入项目 git（F008 cycle 已在 `.gitignore` 排除 `.garage/config/host-installer.json`，是用户本地状态记录），是预期行为；明确不追求跨用户可移植——若 user A commit 后 user B clone manifest 含 `/home/A/...` 是预期不可移植行为，与 F009 不引入"跨用户共享 manifest"目标一致；`.gitignore` 现状无需调整 |
| 9 | [minor][LLM-FIXABLE][A6] FR-903 non-TTY 退化 stderr 字面要求 | **已闭合** | L306 FR-903 验收 #4 加 stderr 字面 "non-interactive shell detected; install no hosts (pass --hosts <list> to override)"（沿用 F007 FR-703 wording 字面一致），且显式声明 "不附加 F009-specific scope-related 提示文字（避免破坏 F007 FR-703 既有 stderr grep）"。注：r1 修复指引曾建议附加 `--scope` 提示，父会话选择保守方案保 F007 grep 兼容性 — 两种方案都满足 finding 闭合，保守方案为合理 trade-off |

### 新风险（不构成新 finding，但需父会话知晓）

- **[新风险/叙事 narrative gap][C2]** L343 FR-906 验收 #1 仍写 "phase 5 (apply + manifest) 的算法主体字节级保持原状（仅 type signatures 因 _Target 增 scope 字段而扩展）"，与 CON-902 (L450-461) 现在更精细枚举的 phase 5 允许差异（schema_version 1→2、dst absolute、新增 scope 字段、调用 VersionManager.migrate）有 wording 精度 gap。CON-902 是 normative 且更严格，FR-906 验收 #1 与之并不矛盾（schema 写入差异由 ManifestSerializer 内部完成被 CON-902 明确豁免），但 wording 未同步精细化。属于叙事一致性残留，不影响 design / design-review / hf-tasks 任一阶段的判断（CON-902 是真源）。建议父会话在 `规格真人确认` 节点顺手把 FR-906 验收 #1 末尾改为 "...phase 5 算法分支结构字节级不变，写入的 schema 升至 2 + 字段集合按 FR-905 + CON-902 phase 5 enum 扩展"，作为零成本一致性修复。**不阻塞 r2 verdict**。
- **[新风险/无]** 未发现新设计泄漏、未发现新模糊词、未发现 USER-INPUT 缺失、未发现 deferred backlog 范围溢出、未发现 8 项 § 11 非阻塞被 design 阶段无法消化的迹象、未发现 ASM/CON 关联失稳。

### 下一步

`规格真人确认`（interactive 模式下父会话向真人确认 spec；auto 模式下父会话写 approval record 后进入 `hf-design`）

接下来 `hf-design` 阶段必须收敛的 design 决策（spec 已显式放权 + § 4.2 关键边界 + § 11 非阻塞 7 项 + CON-902 phase 5 enum 作为可拒红线）：
1. § 11 非阻塞 #1 manifest schema 2 字段命名（`"project"`/`"user"` vs `"workspace"`/`"global"`）
2. § 11 非阻塞 #2 `Path.home()` RuntimeError 退出码（默认 1 vs 专用 3）
3. § 11 非阻塞 #3 stdout 多 scope 段确切格式（注：必须满足 FR-909 "另起一行 + F007 grep 不破坏" 约束）
4. § 11 非阻塞 #4 manifest absolute path 是否带 `~/` 前缀
5. § 11 非阻塞 #5 交互式两轮 vs 一轮 vs 三选一开关（注：必须满足 FR-903 验收 #1-#4 + CON-901 兼容）
6. § 11 非阻塞 #6 `HostInstallAdapter` Protocol 新增 method 命名（`_user` 后缀 sibling vs `scope=...` 单 method 带参数）
7. § 11 非阻塞 #7 `garage status` 按 scope 分组输出格式
8. ManifestMigrationError 类型 + 退出码常量定义（CON-902 phase 5 锚定语义已给出，design 决定具体实现）
9. § 4.1 host_id 命名 ADR 锚定（CON-902 phase 5 + § 4.1 minor #2 闭合后由 design 在 ADR 形式化）

### 复审记录位置

`docs/reviews/spec-review-F009-garage-init-scope-selection.md`（与 r1 同文件，本段为 `## 复审 r2` 追加段）

### 交接说明

- `规格真人确认`：本轮 r2 verdict = `通过`，父会话应执行 approval step（interactive 等待真人 / auto 写 approval record）；执行后由父会话同步 `task-progress.md` Current Stage 与规格状态字段（`草稿` → `已批准`）。
- `hf-specify`：r2 已通过，无需回修；建议父会话在 approval step 顺手把 L343 FR-906 验收 #1 wording 与 CON-902 phase 5 enum 同步精细化（zero-cost 叙事一致性修复，详见上面"新风险" #1）。
- `hf-workflow-router`：route / stage / 证据无冲突，不需要 reroute（`reroute_via_router=false`）。
- 不修改 F009 spec 文档（只读复审）、不修改 `task-progress.md`、不 git commit / push（由父会话执行）。
