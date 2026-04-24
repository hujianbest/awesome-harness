# Tasks Review — F009 `garage init` 双 Scope 安装 + 交互式 Scope 选择

- 评审对象：`docs/tasks/2026-04-23-garage-init-scope-selection-tasks.md`（草稿 r1，6 个 task：T1 adapter / T2 pipeline / T3 manifest / T4 cli / T5 tests / T6 docs）
- 上游已批准工件：
  - 规格：`docs/features/F009-garage-init-scope-selection.md`（已批准 r2，10 FR + 4 NFR + 4 CON + 4 ASM + § 4.2 多重约束 + § 11 8 项非阻塞）
  - 设计：`docs/designs/2026-04-23-garage-init-scope-selection-design.md`（已批准 r2，11 ADR + 6 task + 9 INV + 11 测试文件 + 7 失败模式）
  - 批准记录：`docs/approvals/F009-{spec,design}-approval.md`
  - 评审记录：`docs/reviews/{spec,design}-review-F009-garage-init-scope-selection.md`
- 评审者：独立 reviewer subagent（被父会话派发）
- 评审日期：2026-04-24
- Revision: r1
- 评审依据：`packs/coding/skills/hf-tasks-review/SKILL.md` + `references/review-checklist.md` + `references/review-record-template.md`

## Precheck

| 项 | 结果 | 证据 |
|---|---|---|
| 上游 spec 已批准 | ✅ | `docs/approvals/F009-spec-approval.md` 存在；spec header `状态: 已批准` |
| 上游 design 已批准 | ✅ | `docs/approvals/F009-design-approval.md` 存在；design header `状态: 已批准` |
| 任务计划草稿可定位 | ✅ | `docs/tasks/2026-04-23-garage-init-scope-selection-tasks.md` 存在，6 个 task 完整 |
| route/stage/profile 一致 | ✅ | task-progress.md `Current Stage: hf-tasks` + `Workflow Profile: full` + `Pending Reviews And Gates: hf-tasks-review` |
| AGENTS.md F009 路径约定 | ✅ | spec 路径符合 `docs/features/F009-*.md` AHE 约定 |

→ Precheck **通过**，进入正式审查。

## 多维评分（0-10，任一关键维度 < 6 不得通过）

| ID | 维度 | 分数 | 备注 |
|---|---|---|---|
| TR1 | 可执行性 | 8 | 6 task 全部可冷启动推进；无"实现某模块"式大任务；T1/T3/T4 单 task 触碰 4-5 个文件但意图收敛单一 |
| TR2 | 任务合同完整性 | 6 | 每 task 均含 Acceptance / Files / Verify / 完成条件；但 T3 类型命名 (`ManifestFileEntryV2`) 与既有 `ManifestFileEntry` 关系未明、T3 migration 失败的安全语义未守门、T4 carry-forward 目标识别错误（详见 finding F-T3-2 / F-T3-3 / F-T4-1） |
| TR3 | 验证与测试设计种子 | 6 | 11 个新增测试文件 enum 完整、fail-first 适用点显式标注；但 T5 baseline JSON 录制方式存在两段相互矛盾描述（finding F-T5-1） |
| TR4 | 依赖与顺序正确性 | 9 | 串行 T1→T2→T3→T4→T5→T6 与 design § 10.1 一致；无循环依赖；关键路径合理；P=1..6 无歧义 |
| TR5 | 追溯覆盖 | 7 | § 4 追溯表覆盖全部 FR-901..910 + NFR-901..904 + CON-901..904 + § 4.2；但 § 4.2 仅整行映射"全 ADR / 全 PR"，未每条单独 enum（finding F-Trace-1，minor）|
| TR6 | Router 重选就绪度 | 9 | § 8 选择规则明确串行 + § 9 队列投影 + 每 task 含 Selection Priority + 初始队列状态；router 可稳定重选下一 task |

任一维度均 ≥ 6/10，未触发硬下限。但 TR2/TR3 触及 6/10 下限，存在多条可定向修订的 finding。

## 发现项

### F-T3-1：ManifestFileEntryV2 命名与既有 ManifestFileEntry 兼容关系未明

- **severity**: important
- **classification**: LLM-FIXABLE
- **rule_id**: TR2 / TA3
- **证据**：
  - task plan § 3.2 T3 行 + § 5 T3 acceptance 写 `Manifest dataclass files[] 元素改为 ManifestFileEntryV2`
  - design § 9 + § 11.1 INV-F9-7 仅写 "Manifest dataclass 字段扩展"，未引入 `V2` 后缀类
  - 既有 `src/garage_os/adapter/installer/manifest.py` 现有 `ManifestFileEntry` 被 `pipeline.py` import：`from garage_os.adapter.installer.manifest import (..., ManifestFileEntry, ...)`（pipeline.py:39）
  - 既有 `tests/adapter/installer/test_manifest.py` 用 `ManifestFileEntry` 构造测试 fixture
- **问题**：task plan 把新类型命名为 `ManifestFileEntryV2` 但未说明：
  1. 是新类替换既有 `ManifestFileEntry`（删除老类，所有 import 改名）
  2. 还是同名扩展字段（直接给 `ManifestFileEntry` 加 `dst absolute` + `scope` 字段）
  3. 还是双类并存（schema 1 用旧类，schema 2 用 V2，read_manifest 按 schema_version 分流）
  这个澄清直接影响 T3 commit 的最终代码形态、既有 `pipeline.py` import 是否需要改、carry-forward 工作量。
- **修订建议**：T3 acceptance + Files 段显式声明命名策略（推荐："直接给既有 `ManifestFileEntry` 加 `dst: str (absolute POSIX)` + `scope: Literal['project','user']` 字段；read_manifest 在 schema_version=1 时 migrate 后构造同一个 `ManifestFileEntry`，无双类并存"）；并把 task plan § 3.2 T3 行 `ManifestFileEntryV2` 改为 `ManifestFileEntry (字段扩展)`。

### F-T3-2：Migration 失败时旧 manifest 不被覆盖语义未守门

- **severity**: minor
- **classification**: LLM-FIXABLE
- **rule_id**: TR2 / TA2
- **证据**：
  - spec FR-905 验收 #4：`Given migration 失败（如旧 manifest JSON 损坏），Then 退出码 1，stderr 含 'Manifest migration failed: ...'，旧 manifest 不被覆盖`
  - spec CON-904：`migration 失败时退出码 1 + 旧 manifest 不被覆盖`
  - task plan T3 acceptance 仅含 "ManifestMigrationError(ValueError): JSON 损坏或字段缺失时抛"，但**未守门**"旧 manifest 文件保持原状不被覆盖"
  - design § 14 F2 已说明缓解策略
- **问题**：FR-905 安全语义"failed migration 不写入新 manifest"是用户数据安全的硬边界，task acceptance 必须显式守门避免实施期遗漏。
- **修订建议**：在 T3 acceptance 增加一条："migration 失败（ManifestMigrationError 抛出）时 `host-installer.json` 文件保持 schema 1 字节级不变，由 fixture 测试 + assertion `read 文件 SHA-256 == 原 SHA-256` 守门"；并在 T3 测试种子加 "test_migration_failure_preserves_old_manifest"。

### F-T4-1：carry-forward 目标对象错误（test_cli.py 实测无 manifest schema_version assertion）

- **severity**: important
- **classification**: LLM-FIXABLE
- **rule_id**: TR2 / TR5
- **证据（grep 实测）**：
  - `tests/test_cli.py` 内全部 `schema_version` 出现位置：行 457/505/563/640/703/777（全部是 `candidate_store.store_candidate({"schema_version": "1", ...})` — 与 F009 manifest 完全无关）+ 行 3175/3218/3260（全部是 `pack.json` 构造 — 受 CON-903 保护，本 cycle 不变）
  - test_cli.py:3038-3046 manifest 断言仅查 `installed_hosts` 和 `installed_packs`，**未断言** `manifest["schema_version"]`
  - 反观 `tests/adapter/installer/test_manifest.py` 实测 6 处 `schema_version=1` 硬编码 + `assert MANIFEST_SCHEMA_VERSION == 1`（行 47, 55, 77, 100, 121, 154, 171）— 这才是真正需要 carry-forward 的目标
- **问题**：task plan T3 acceptance "既有 test_manifest.py 0 退绿（如有 schema_version=1 hard-coded assertion，allow carry-forward 放宽到 in (1, 2)）" + T4 acceptance "既有 test_cli.py::TestInitWithHosts 100% 通过；如有 schema_version assertion 必要时 carry-forward 修复"，把 carry-forward **错误地**列在 T4（test_cli.py），而 grep 实测显示 T3（test_manifest.py）才是真正且唯一的目标。这会导致：
  - T4 commit 写"carry-forward test_cli.py"但实际无修改 → commit message 描述与 diff 不符 → reviewer 困惑
  - T3 commit 真正修改 test_manifest.py 但 acceptance 表达模糊（"如有 ... 必要时"），实施期可能漏掉
- **修订建议**：
  1. T3 acceptance 把 "如有 schema_version=1 hard-coded assertion，allow carry-forward 放宽" 改为强表述："必须把 test_manifest.py 的 `assert MANIFEST_SCHEMA_VERSION == 1` 改为 `== 2`（schema 升级直接结果，非 carry-forward），且 6 处 `Manifest(schema_version=1, ...)` 构造保留作为 schema 1 兼容测试，新增镜像构造测 schema 2"
  2. T4 acceptance 移除 "carry-forward 修复 test_cli.py 既有 schema_version assertion" 表述，改为 "既有 test_cli.py::TestInitWithHosts 100% 通过，无需 schema_version carry-forward（grep 实测无 manifest schema_version 断言）"
  3. § 10 风险表 F7 行同步修订：carry-forward 目标限定在 T3 / test_manifest.py
  4. § 1 执行原则 "carry-forward wording 修复（如 schema_version assertion）允许但需 commit message 显式声明" 保留措辞（仍适用 T3）

### F-T5-1：Dogfood baseline JSON 录制方式自相矛盾

- **severity**: important
- **classification**: LLM-FIXABLE
- **rule_id**: TR3 / TA4
- **证据**：
  - task plan § 5 T5 测试种子 (a)：`baseline JSON 由 T5 commit 一次性生成（人工 enum 30 文件 SHA-256，参考 packs/ 内容物 + marker injection 规则）`
  - task plan § 10 风险表 T5 行：`T5 commit 一次性人工 enum + 由 hf-test-driven-dev executor 在 fixture 里实跑 install 后 read SHA-256 写入 JSON`
  - design § 18 非阻塞 #1：`dogfood SHA-256 baseline 录制方式（人工生成静态 fixture vs 测试 setUp 时计算）— hf-tasks 决定`
- **问题**：task plan 在两段（测试种子 vs 风险表）给出**两种相互矛盾**的录制方式：
  - 方式 A：人工 enum，独立于运行时 marker 注入（独立验证，能 catch marker 实施 bug）
  - 方式 B：fixture 实跑 install 后 read SHA-256（自我验证，可能掩盖 marker 实施 bug，但减少人工录入错误）
  这两种方式语义不同，sentinel 守门强度不同。design § 18 #1 已显式说"hf-tasks 决定"，task plan 必须在此处给出 **唯一选择 + 理由**，而非两段都列。
- **修订建议**：T5 acceptance + 测试种子 + § 10 风险表 三处统一选定**方式 A（人工 enum 静态 fixture）**：理由是 dogfood sentinel 的核心语义是"独立第三方验证 marker 注入未漂移"，自我验证（B）会让 marker bug 同时污染 baseline 与实测两侧导致永远 GREEN。同时给出 baseline JSON 文件位置 + 30 文件 enum 来源（packs/ 内容物 × 三家 adapter target_skill_path/agent_path）+ commit 落地步骤。

### F-T1-1：resolve_hosts_arg 返回类型变更对既有测试的影响未声明

- **severity**: minor
- **classification**: LLM-FIXABLE
- **rule_id**: TR2 / TR5
- **证据**：
  - 既有 `host_registry.resolve_hosts_arg(arg: str) -> list[str]`（host_registry.py:99）
  - task plan T1 § 3.2 改为 `list[tuple[str, str | None]]`
  - 既有 `tests/adapter/installer/test_host_registry.py` 测试 `resolve_hosts_arg` 返回值 shape（grep 实测：tests/adapter/installer/test_host_registry.py 是该函数唯一直接测试者）
  - F009 spec CON-901 守的是用户面行为（stdout/stderr/退出码/落盘），不是 Python API 签名 — 故签名变更不违反 CON-901
- **问题**：task plan T1 acceptance 列了"既有 F007 target_skill_path / target_agent_path / render method 签名零变更"，但**没显式列出**"既有 test_host_registry.py 测试需要按返回类型变更同步更新（如 `resolve_hosts_arg('claude') == ['claude']` 改为 `== [('claude', None)]`）"。这种 in-cycle 同步更新不属于 carry-forward wording 修复（属于 API 演化），但应在 acceptance 显式声明避免被误判违反 CON-901。
- **修订建议**：T1 acceptance 增加一条："既有 test_host_registry.py 中针对 `resolve_hosts_arg` 返回值的 assertion 同步按新二元组格式更新（in-cycle API 演化，非 carry-forward；commit message 显式声明）；既有用户面行为（stdout/stderr/退出码）字节级不变"。

### F-T5-2：user scope 集成测试未显式列出 3 家 adapter 各自 monkeypatch 守门

- **severity**: minor
- **classification**: LLM-FIXABLE
- **rule_id**: TR3 / TR5
- **证据**：
  - spec FR-904 验收：claude `~/.claude/...` + opencode `~/.config/opencode/...` (XDG) + cursor `~/.cursor/...`
  - design § 13 边界澄清："`test_full_init_user_scope.py`：fixture 用 monkeypatch `Path.home()` 指向 tmp_path 内子目录，跑 `garage init --hosts all --scope user`"
  - task plan T5 acceptance：`fixture monkeypatch Path.home() 到 tmp_path/home，跑 garage init --hosts all --scope user，验证三家宿主目录 + manifest schema 2 含 scope: "user" entry 87+ 条`
- **问题**：task plan acceptance 只整体说"三家宿主目录"，未 enum 验证：
  1. claude → tmp_path/home/.claude/skills/{29 SKILL.md}
  2. opencode → tmp_path/home/.config/opencode/skills/{29 SKILL.md}（XDG default，spec/design 明确选 XDG）
  3. cursor → tmp_path/home/.cursor/skills/{29 SKILL.md}（无 agent surface）
  monkeypatch `Path.home()` 是否完整覆盖 OpenCode XDG 解析（`Path.home() / ".config/opencode/..."`）依赖实施时正确传递。
- **修订建议**：T5 acceptance 拆条 enum 三家落盘路径，每家独立断言 + 数量 + 关键文件存在性；并显式守门 "OpenCode XDG default `~/.config/opencode/skills/` 而非 dotfiles `~/.opencode/skills/`"（与 design ADR-D9 OpenCode XDG 选择一致）。

### F-Trace-1：§ 4 追溯表对 spec § 4.2 多重约束未逐条 enum

- **severity**: minor
- **classification**: LLM-FIXABLE
- **rule_id**: TR5
- **证据**：
  - spec § 4.2 enum 8 条关键边界（CON-902 phase 1+3 严格 / manifest schema 单向 / Path.home() stdlib / OpenCode 默认 XDG / 不动 Protocol 既有签名 / 不动 packs/ / 不动 EXEMPTION_LIST / dogfood 不受影响 / scope 不引入新优先级）
  - task plan § 4 追溯表底行只有 `§ 4.2 F009 边界（全部）| 全 ADR | 全 PR | 各 task acceptance + INV` — 整行映射
- **问题**：粗粒度映射使 reviewer / 实施期 executor 无法快速核对 8 条边界是否每条都有 task / acceptance / verify 落地。例如"OpenCode 默认 XDG"是否在 T1 / T5 显式守门？"scope 不引入新优先级"是否在 T2 / T3 显式守门？
- **修订建议**：把 § 4.2 8 条边界单独 enum 成 8 行，每行映射 (task / acceptance 锚点 / verify 命令)。可与 § 4 现有 11 行追溯表合并为单表或独立子表。

## 缺失或薄弱项

无致命缺失。以下属于 informational anchor，未上升到 finding：

- task plan 未显式回应 "为什么不拆 sub-commit"（与 F008 9 sub-commit 对比）— 6 task 一对一是合理选择（每 task 意图收敛单一），但显式说明会让 NFR-904 git diff 可审计性论证更完整
- T6 RELEASE_NOTES 5 项 TBD 占位字段已显式 enum（manual_smoke_wall_clock / pytest_total_count / installed_packs_from_manifest / commit_count_per_group / release_notes_quality_chain）— 充分；与 F008 finalize 同精神

## 结论

**需修改**

理由：
- 6 task 整体结构、依赖、追溯、router 重选就绪度均达标
- 但存在 3 条 important + 4 条 minor 的可定向修订 finding，其中：
  - F-T3-1（ManifestFileEntryV2 命名）影响 T3 commit 的最终代码形态
  - F-T4-1（carry-forward 目标对象错误）已被 grep 实测证伪，不修订会导致 T4 commit message 与 diff 失真
  - F-T5-1（baseline 录制方式自相矛盾）影响 dogfood sentinel 的守门强度
- 全部 7 条 finding 均 LLM-FIXABLE，可由 hf-tasks 在原 task plan 上定向修订，无需推翻整体结构
- 不属于 route/stage/上游证据冲突 → 不需 router 重编排

## 下一步

`hf-tasks`（回修 task plan，针对 7 条 finding 定向修订；修订完成后再次派发 hf-tasks-review 复审）

## 记录位置

`docs/reviews/tasks-review-F009-garage-init-scope-selection.md`

## 交接说明

- `hf-tasks`：用于本次回修，按 finding 表逐条修订 task plan r1 → r2，commit message 显式列出修订点
- 复审时重点核查：
  1. F-T3-1 是否选定单一命名策略（推荐字段扩展同一 ManifestFileEntry）
  2. F-T3-2 migration 失败旧 manifest 不被覆盖是否在 T3 acceptance 显式守门
  3. F-T4-1 carry-forward 目标是否从 T4/test_cli.py 迁移到 T3/test_manifest.py
  4. F-T5-1 baseline 录制是否选定方式 A（人工 enum 静态 fixture）并三处一致
  5. F-T1-1 / F-T5-2 / F-Trace-1 minor 是否一并修订
- 修订后再次走 `hf-tasks-review` → 通过则 `任务真人确认` → `hf-test-driven-dev`
