# F012 Design: Pack Lifecycle 完整化

- 状态: 草稿（待 hf-design-review）
- 关联 spec: `docs/features/F012-pack-lifecycle-completion.md` (r2 已批准, `docs/approvals/F012-spec-approval.md`)
- 日期: 2026-04-25

## 0. 设计目标

把 F012 spec 14 FR + 4 NFR + 7 CON + 4 ASM + 6 HYP + 4 BLK 翻译成可拆 task 的代码层结构. 5 子部分都是单领域改动:

- **A** uninstall: `pack_install.py` 加 `uninstall_pack(workspace_root, pack_id)` + CLI subcommand
- **B** update: 同 module 加 `update_pack(workspace_root, pack_id)`, 复用 install 内部 helper
- **C** publish: 同 module 加 `publish_pack(workspace_root, pack_id, to_url, ...)` + sensitive_scan helper
- **D** knowledge export: 新 module `src/garage_os/knowledge/exporter.py` + `garage knowledge export --anonymize` CLI
- **E** F009 carry-forward: `manifest.py` 加 `@register_migration(1, 2)` decorator + VersionManager.SUPPORTED_VERSIONS 同步加 2

## 1. 架构概览

```
src/garage_os/
├── adapter/installer/
│   ├── pack_install.py (ext)
│   │   + uninstall_pack(workspace_root, pack_id, *, dry_run, yes, stderr) -> UninstallSummary
│   │   + update_pack(workspace_root, pack_id, *, yes, preserve_local_edits, stderr) -> UpdateSummary
│   │   + publish_pack(workspace_root, pack_id, to_url, *, yes, force, dry_run,
│   │                  no_update_source_url, commit_author, commit_message, stderr) -> PublishSummary
│   │   + sensitive_scan(pack_dir) -> list[SensitiveMatch]   (helper for publish)
│   └── manifest.py (ext)
│       + @register_migration(1, 2) on migrate_v1_to_v2
│
├── knowledge/
│   └── exporter.py (NEW)
│       + export_anonymized(workspace_root, *, output_dir, dry_run, stderr) -> ExportSummary
│       + ANONYMIZE_RULES: list[(name, pattern, replacement)]
│       + load_user_extra_rules() -> list[(name, pattern, replacement)]   (~/.garage/anonymize-patterns.txt)
│
├── platform/version_manager.py (ext)
│   + SUPPORTED_VERSIONS: List[int] = [1, 2]   (was [1])
│
└── cli.py (ext)
    + pack uninstall <pack-id> [--yes] [--dry-run]
    + pack update <pack-id> [--yes] [--preserve-local-edits]
    + pack publish <pack-id> --to <git-url> [--yes] [--force] [--dry-run]
                              [--no-update-source-url] [--commit-author "Name <email>"]
                              [--commit-message <msg>]
    + knowledge export --anonymize [--output <path>] [--dry-run]
```

依赖方向 (无环):
```
pack_install (ext) → manifest (ext) ← VersionManager
                  ↘ host_registry / hosts/* (既有, 不动)
exporter (NEW) → KnowledgeStore (既有, 不动)
cli (ext) → 上述全部
```

## 2. ADRs

### ADR-D12-1: 5 子部分共用同一 module 还是分开?

**Decision**: F012-A/B/C 三者都在 `pack_install.py` 同 module (与 F011 既有 `install_pack_from_url` + `list_installed_packs` 并列), 复用 PackInstallSummary 数据结构 pattern (UninstallSummary / UpdateSummary / PublishSummary). F012-D 在 `knowledge/exporter.py` (与 KnowledgeStore 同包, 自然位置). F012-E 在 manifest.py 顶部加一行 decorator + VersionManager.SUPPORTED_VERSIONS 加常数.

**Consequences**:
- (+) 单一职责: pack lifecycle 共一处, knowledge export 与 KnowledgeStore 同包
- (+) 复用 PackInstallError exception type 跨 install/uninstall/update/publish (统一 CLI catch)
- (-) `pack_install.py` 行数从 ~190 → ~600 (5x); 但仍 < 800, 接受 trade-off

### ADR-D12-2: uninstall 反向清磁盘的算法 (FR-1201 + CON-1203 atomic)

**Decision**: 三步 transaction (类似 F009 manifest atomic write):
1. **Plan phase** (read-only): 从 `host-installer.json files[]` 过滤 `pack_id == <pack-id>` 的所有 entry, 列出每个 entry 的 `dst` 文件 + 反向推导 sidecar 子目录 (`references/ assets/ evals/ scripts/` 在 `dst.parent` 下) + 空的 host 父目录候选
2. **Confirm phase** (interactive 或 dry-run): 显示 plan 详情, prompt or print
3. **Execute phase** (commit): 按 plan 删文件 → 删 sidecar → 删空 host 父目录 → 删 `packs/<pack-id>/` → 重写 host-installer.json (drop entries + drop installed_packs[])
4. 任一步骤失败 → 回滚 (磁盘备份在 temp dir, 失败时 swap 回; manifest 备份在内存, 失败时不写回)

**Consequences**:
- (+) atomic: 无半完成状态
- (+) dry-run 复用 plan phase, 不进 execute
- (-) 备份 packs/<pack-id>/ 到 temp dir 增加 IO; 但与 update 一致 + 安全优先

### ADR-D12-3: update 算法 — 复用 install 内部 helper

**Decision**: `update_pack` 内部:
1. read `packs/<pack-id>/pack.json.source_url`
2. shallow clone 到 temp dir (复用 `install_pack_from_url` 的 git clone 逻辑, 抽出 `_clone_pack_to_tempdir(url) -> Path` helper)
3. 比对 version (read both pack.json)
4. 同 → no-op + stdout
5. 不同 → prompt or yes → 备份当前 `packs/<pack-id>/` 到 temp → 替换 → 调 `install_packs(workspace_root, hosts=已装 host list)` 自动同步 host 目录 (复用 F007 既有 install_packs, 它会按 host-installer.json 既有 file entry 走 update_from_source 路径)
6. 失败时 swap 回备份 (atomic 同 ADR-D12-2)

**Consequences**:
- (+) 复用 F011 install_pack_from_url 内部 helper (clone + verify), 不重写
- (+) 复用 F007 install_packs 的 host 目录同步, 自动走既有 mtime stability + sidecar copy
- (-) 必须先 abstract `_clone_pack_to_tempdir` helper (refactor F011 install_pack_from_url; 但内部调用方法只有自己, 重构成本低)

### ADR-D12-4: publish 算法 + sensitive scan + git push --force 风险检测

**Decision**:
1. **Sensitive scan** (FR-1208 + ADR-D12-1 helper): 用 `sensitive_scan(pack_dir) -> list[SensitiveMatch]`. 实现:
   ```python
   SENSITIVE_RULES = [
       ("password", re.compile(r"password\s*[:=]\s*\S+", re.IGNORECASE)),
       ("api_key", re.compile(r"api[_-]?key\s*[:=]\s*\S+", re.IGNORECASE)),
       ("secret", re.compile(r"secret\s*[:=]\s*\S+", re.IGNORECASE)),
       ("token", re.compile(r"token\s*[:=]\s*\S+", re.IGNORECASE)),
       ("private_key", re.compile(r"-----BEGIN (RSA|OPENSSH|PRIVATE) KEY-----")),
   ]
   TEXT_EXTENSIONS = frozenset({".md", ".py", ".txt", ".json", ".yaml", ".yml", ".toml",
                                ".sh", ".js", ".ts", ".ini", ".cfg", ".conf", ".env",
                                ".lock", ".gitignore"})
   ```
   仅扫 ext 在 allowlist 的文件; 其它跳过 + 计入 skipped_count.

2. **Force push 风险检测** (FR-1207 step 3):
   ```python
   result = subprocess.run(["git", "ls-remote", to_url], capture_output=True, text=True)
   remote_has_refs = bool(result.stdout.strip())
   if remote_has_refs and not yes:
       # 显示 remote head + 必须二次 prompt
       print(f"Remote {to_url} has existing refs:\n{result.stdout}\nReally overwrite? [y/N]:")
   ```

3. **Git author 决议**:
   ```python
   def _resolve_commit_author(commit_author: str | None) -> tuple[str, str]:
       if commit_author:
           # parse "Name <email>" format
           ...
       try:
           name = subprocess.run(["git", "config", "user.name"], ...).stdout.strip()
           email = subprocess.run(["git", "config", "user.email"], ...).stdout.strip()
           if name and email: return (name, email)
       except subprocess.CalledProcessError: pass
       return ("Garage", "garage-publish@local")
   ```

4. **Publish steps** (FR-1207 step 5): tempdir → `git init` → copy pack files (skip `.git/`) → `git add .` → `git -c user.email=... -c user.name=... commit -m <msg>` → `git remote add origin <to-url>` → `git push --force origin main`

**Consequences**:
- (+) sensitive scan 模块化, 测试 fixture 5 类敏感词 ↔ 5 类 SENSITIVE_RULES 1:1
- (+) git ls-remote 检测让用户在覆盖前看到 remote head
- (+) git author 决议支持 user-pact "你做主" + 配置友好

### ADR-D12-5: knowledge export 脱敏 + KnowledgeStore mixed strategy

**Decision** (FR-1211 + Mi-5 fix):
1. **Metadata pass**: `KnowledgeStore.list_entries()` 拿全部 KnowledgeEntry → tarball 内 `manifest.json` (entry id / topic / tags / type / date 索引)
2. **Content pass**: 用 entry id 推 file path `.garage/knowledge/<kind-dir>/<id>.md` → filesystem read raw bytes → split front matter + body → 仅对 body 走脱敏 (front matter 字段 id/topic/tags/date 是 meta 不动) → write tarball 内 `<kind>/<id>.md`
3. **Anonymize rules**:
   ```python
   ANONYMIZE_RULES = [
       ("email", re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"), "<REDACTED>"),
       ("password", re.compile(r"(?P<key>password\s*[:=]\s*)\S+", re.IGNORECASE), r"\g<key><REDACTED>"),
       ("api_key", re.compile(r"(?P<key>api[_-]?key\s*[:=]\s*)\S+", re.IGNORECASE), r"\g<key><REDACTED>"),
       ("sha1_hash", re.compile(r"\b[a-f0-9]{40}\b"), "<REDACTED:sha1>"),
       ("private_key", re.compile(r"-----BEGIN (RSA|OPENSSH|PRIVATE) KEY-----.*?-----END \\1 KEY-----", re.DOTALL), "-----REDACTED-----"),
   ]
   ```
   `load_user_extra_rules()` 读 `~/.garage/anonymize-patterns.txt` (一行一条 regex, `#` 注释), append 到 ANONYMIZE_RULES.
4. **Output**: `<output>/knowledge-<ISO ts>.tar.gz` (default `~/.garage/exports/`)

**Consequences**:
- (+) Mixed strategy 让 metadata 走 KnowledgeStore (类型安全), body 走 filesystem (字节级保留 markdown 结构)
- (+) ANONYMIZE_RULES 5 类与 SENSITIVE_RULES 5 类 1:1 (FR-1212 + FR-1208 同 schema, 易测)
- (+) tarball 内含 manifest.json 让接收方能 list 内容不必解 tarball

### ADR-D12-6: F009 carry-forward — 注册策略

**Decision** (FR-1214 + M-1 fix):
- 在 `manifest.py` 模块顶部 (function definition 之后) 加:
  ```python
  from garage_os.platform.version_manager import register_migration
  
  @register_migration(1, 2)
  def _migrate_v1_to_v2_for_registry(data: dict, target_version: VersionInfo) -> dict:
      """Wrapper to adapt manifest.migrate_v1_to_v2 to VersionManager API.
      
      VersionManager.register_migration expects (data: dict, target_version: VersionInfo) -> dict
      while manifest.migrate_v1_to_v2 has (Manifest, workspace_root) -> Manifest signature.
      This wrapper bridges the two for cycle-time registry but read_manifest fast-path 仍 bypass.
      """
      # data is the raw JSON dict; rebuild as Manifest, migrate, serialize back
      ...
  ```
- 同时改 `VersionManager.SUPPORTED_VERSIONS = [1, 2]` (line 146)
- F009 既有 `read_manifest` 内部分支 (auto-detect schema 1 → migrate) 不动 — 双源一致, 但 read_manifest 仍走 fast-path (避免双跳 wrapper 开销)

**Consequences**:
- (+) `_MIGRATION_REGISTRY[(1, 2)]` 正确填充 (满足 SM-1205 acceptance)
- (+) F009 既有 read_manifest 行为字节级不变 (CON-1202)
- (-) 引入一个 wrapper 函数 (_migrate_v1_to_v2_for_registry) 略增复杂度; 测试覆盖

### ADR-D12-7: 5 子部分串行 commit (T1-T5)

**Decision**: 5 sub-commit, 单线递进, P=1..5 唯一无冲突 (与 F010 T1-T7 + F011 T1-T5 同 cycle 结构):
- T1: F012-A uninstall (pack_install + cli + tests)
- T2: F012-B update (复用 T1 helper + cli + tests)
- T3: F012-C publish + sensitive_scan (pack_install + cli + tests)
- T4: F012-D knowledge export --anonymize (新 module + cli + tests)
- T5: F012-E F009 carry-forward (manifest + version_manager + tests) + docs sync + finalize

**Consequences**:
- (+) 每 task 单文件域 + 单测试文件; auto mode 可每 task 独立 verify + commit
- (+) 串行依赖小 (T2 用 T1 abstracted helper; T3-T5 互不依赖)

## 3. 测试矩阵

### INV
- INV-F12-1: F011 既有 install + ls 行为字节级不变 (CON-1201; 测既有测试 0 退绿)
- INV-F12-2: F009/F010/F011 baseline 859 → ≥ 859 + 增量 (CON-1202)
- INV-F12-3: uninstall 反向清干净 (HYP-1201 + SM-1201)
- INV-F12-4: update atomic + 滚回 (HYP-1202 + FR-1205)
- INV-F12-5: publish 隐私自检 5 类 (FR-1208 + SM-1204)
- INV-F12-6: publish push to file:// remote 可工作 (HYP-1203 + SM-1203)
- INV-F12-7: anonymize 5 类规则 (HYP-1204 + SM-1204)
- INV-F12-8: VersionManager 注册 (1, 2) (FR-1214 + HYP-1205 + SM-1205)
- INV-F12-9: uninstall 不动 sync-manifest.json (HYP-1206 + CON-1205)

### 测试文件
- `tests/adapter/installer/test_pack_uninstall.py` (T1)
- `tests/adapter/installer/test_pack_update.py` (T2)
- `tests/adapter/installer/test_pack_publish.py` + `test_sensitive_scan.py` (T3)
- `tests/knowledge/test_exporter.py` (T4)
- `tests/adapter/installer/test_manifest_migration_registry.py` (T5)
- `tests/test_cli.py::TestPackUninstallCommand` / `TestPackUpdateCommand` / `TestPackPublishCommand` / `TestKnowledgeExportCommand` (T1-T4)

## 4. Commit 分组 (T1-T5)

按 NFR-904 commit 可审计:

| Task | P | 描述 |
|---|---|---|
| **T1** | 1 | A: uninstall_pack + CLI + tests |
| **T2** | 2 | B: update_pack (refactor _clone_pack_to_tempdir helper) + CLI + tests |
| **T3** | 3 | C: publish_pack + sensitive_scan helper + CLI + tests |
| **T4** | 4 | D: knowledge/exporter.py + CLI + tests |
| **T5** | 5 | E: F009 carry-forward (manifest + version_manager) + docs sync + RELEASE_NOTES + finalize |

## 5. 风险 + 缓解

| 风险 | 严重度 | 缓解 |
|---|---|---|
| HYP-1203 (file:// publish) 在 git 旧版本不工作 | 中 | manual smoke Track 4 实测; failed 时降级 deferred |
| HYP-1204 脱敏召回不足 | 低 | B5 user 自管 ~/.garage/anonymize-patterns.txt; SM-1204 仅追求 5 类 fixture 命中 |
| _migrate_v1_to_v2_for_registry wrapper 与 read_manifest fast-path 双源不一致 | 中 | 单元测试同时调两路径, assert 同结果 |
| update 失败时备份恢复失败 (二次失败) | 中 | tempdir 备份 + atomic swap; 即使二次失败 stderr 显式告知用户手动干预路径 |

## 6. 评审前自检 (供 hf-design-review)

- [x] 7 个 ADR 含 Status / Context / Decision / Consequences
- [x] 架构图 (sync push + ingest pull pattern 不适用; 改为 5 子部分模块图)
- [x] 9 个 INV 与 spec FR/NFR/CON 一一对应
- [x] 测试文件按 task 拆 + enum
- [x] 5 sub-commit 分组 (T1-T5)
- [x] 风险表 + 缓解
- [x] 复用 F011 PackInstall pattern + F007 install_packs + F009 manifest migration + F003 KnowledgeStore (CON-1202 守门)
- [x] CON-1207 不修 F010 carry-forward (FR-1214 仅修 F009 carry-forward)
- [x] 真实 API name 锚点持续 (8/8 from spec r2 review)
