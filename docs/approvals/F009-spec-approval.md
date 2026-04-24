# Approval Record - F009 Spec

- Artifact: `docs/features/F009-garage-init-scope-selection.md`
- Approval Type: `specApproval`
- Approver: cursor cloud agent (auto-mode policy approver)
- Date: 2026-04-23
- Workflow Profile / Execution Mode: `full` / `auto`
- Workspace Isolation: `in-place`（工作分支 `cursor/f009-init-scope-selection-bf33`；PR #24）

## Evidence

- **Round 1 review**: `docs/reviews/spec-review-F009-garage-init-scope-selection.md`（R1 段） — `需修改`
  - 0 critical / 4 important + 5 minor 全部 LLM-FIXABLE，USER-INPUT = 0
  - F-1 [important][C2/C7] NFR-901 字节级 vs FR-905 manifest schema migration 边界模糊
  - F-2 [important][C2/A3] CON-902 phase 5 字节级 vs schema 升级 ordering anchor 缺
  - F-3 [important][Q3/C2] FR-903 交互式批量快捷 design 决策点未列入 § 11
  - F-4 [important][C6/C2] dogfood 不破坏缺独立可机械守门 anchor
  - F-5 [minor][C7/A3] FR-909 多 scope stdout 附加段未约束行结构
  - F-6 [minor][Q3/C2] per-host override 语法对 host_id 命名约束未声明
  - F-7 [minor][C7] NFR-902 增量量级缺 anchor
  - F-8 [minor][C2/C7] manifest 跨用户 / git track 立场未声明
  - F-9 [minor][A6] FR-903 non-TTY 退化 stderr 提示完整性未约束
- **Round 1 follow-up commit**: `24cdb7f` "f009(spec): r1 spec-review 通过定向回修 (4 important + 5 minor 全部 LLM-FIXABLE)"
  - F-1 闭合：NFR-901 加 "明确例外 (schema migration)" 段 + 验收 #2 "0 改写" → "0 语义退绿" + carry-forward 显式说明
  - F-2 闭合：CON-902 严格 enum 5 phase 各自允许的最小改动；phase 5 内 VersionManager.migrate 调用 ordering anchor + ManifestMigrationError → exit 1；phase 1+phase 3 严格不动作为 design reviewer 可拒红线
  - F-3 闭合：§ 11 非阻塞 #5 扩展为三选一（A 两轮 / B 一轮带后缀 / C 两轮+all P/all u/per-host 三个开关）
  - F-4 闭合：NFR-901 验收新增 "Dogfood 不变性硬门槛" 条款（SHA-256 字节级与 F008 dogfood baseline 一致）
  - F-5 闭合：FR-909 验收强约束附加段必须在另一行 + F007 既有 grep `^Installed [0-9]+ skills, [0-9]+ agents into hosts:` 命中数 == 1
  - F-6 闭合：§ 4.1 包含表 per-host override 行加 host_id 不允许 `:` 字符约束 + design ADR 锚定
  - F-7 闭合：NFR-902 加 "预期增量 ≥ 25" informational anchor + 验收 #1 加 "实际增量预期 ≥ 25" + "0 退绿" → "0 语义退绿"
  - F-8 闭合：CON-904 加 "跨用户可移植性立场" 段（manifest 默认不入项目 git，与 F008 dogfood `.gitignore` 政策一致）
  - F-9 闭合：FR-903 验收 #4 加 stderr 字面要求（沿用 F007 FR-703 wording，不附加 F009-specific scope 提示文字）
- **Round 2 review**: `docs/reviews/spec-review-F009-garage-init-scope-selection.md`（R2 段） — **`通过`**
  - 0 critical / 0 important / 0 minor
  - r1 全部 9 条 finding 闭合（9 closed / 0 open / 0 regressed）
  - 1 条 narrative gap（FR-906 验收 #1 wording 未与 CON-902 phase 5 enum 精度同步）reviewer 标记 informational，不阻塞 verdict
  - `needs_human_confirmation=true`（reviewer 指 spec 真人确认环节由 auto-mode 父会话写 record）；不存在 USER-INPUT 类阻塞
  - `reroute_via_router=false`
- **Narrative gap 顺手清理**（在 approval 前由父会话直接修文，r2 reviewer 已识别为非阻塞）：FR-906 验收 #1 末尾 wording 与 CON-902 phase 5 enum 精度同步，明确"phase 1 + phase 3 严格不变 + phase 2 / 4 / 5 按 CON-902 enum 允许的最小改动"
- **Auto-mode policy basis**: `AGENTS.md` 未限制 coding cycle 内 spec 子节点 auto resolve；本 cycle 由 router 路由为 `auto`，approval step 在 record 落盘后即可解锁下游 `hf-design`

## Decision

**Approved**. Spec 状态由 `草稿` → `已批准（auto-mode approval）`。下一步 = `hf-design`，输入为：

- 本 F009 spec（已批准）
- F007 已落 packs/ 目录契约 + `garage init --hosts ...` 安装管道 + manifest schema 1（本 cycle 升级到 schema 2）
- F008 已落 packs/ 内容物（22+3+4=29 skill）+ ADR-D8-2 候选 C dogfood + ADR-D8-9 EXEMPTION_LIST（本 cycle 严禁修改）
- 三家 first-class adapter `hosts/{claude,opencode,cursor}.py`（本 cycle 各加 user scope path 解析）

design 阶段需在 § 11 非阻塞 1-7 + r1 finding F-2 升级出的 ManifestMigrationError 类型 + r1 finding F-6 升级出的 host_id 命名 ADR = 共 9 项 ADR 决策中给出 ADR：
1. manifest schema 2 字段命名（`"project"`/`"user"` vs `"workspace"`/`"global"`）
2. `Path.home()` 抛 RuntimeError 的退出码
3. stdout 多 scope 段格式
4. manifest absolute path 是否带 `~/` 前缀
5. 交互式 UX 三选一（A 两轮 / B 一轮带后缀 / C 两轮+all P/all u/per-host）
6. HostInstallAdapter Protocol 新增 method 命名（`target_skill_path_user` vs `target_skill_path(scope=...)`）
7. `garage status` 输出格式
8. ManifestMigrationError 类型与退出码常量
9. host_id 命名约束（不允许字面 `:` 字符）

每项 ADR 必须能通过 spec § 11 阻塞性 / 非阻塞性 + NFR-901 字节级 + CON-902 phase 5 enum + CON-904 跨用户立场 等多重约束的检查。

## Hash & 锚点

- Spec 初稿提交: `2e23ca9` "f009(spec): 起草 garage init 双 scope (project/user) + 交互式 scope 选择规格"
- r1 回修提交: `24cdb7f` "f009(spec): r1 spec-review 通过定向回修 (4 important + 5 minor 全部 LLM-FIXABLE)"
- approval 提交（含 narrative gap 清理 + 状态 → 已批准）: 本 commit

## 后续 (informational, 不阻塞 approval)

- § 11 非阻塞性开放问题 9 条由 design 阶段消化（包括 r1 升级出的 ManifestMigrationError 类型 + host_id 命名 ADR）
- `RELEASE_NOTES.md` 新增 F009 段 + `packs/README.md` "Install Scope" 段 + `docs/guides/garage-os-user-guide.md` 同步由 hf-tasks T?(docs) 阶段完成（FR-910 验收）
- F008 cycle "5 类 minor LLM-FIXABLE 残留" 与 F009 cycle 正交，本 cycle 不顺手清理
