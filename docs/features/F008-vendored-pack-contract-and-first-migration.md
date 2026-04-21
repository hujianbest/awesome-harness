# F008: Vendored Pack 契约与首批迁移 — 把 `.agents/skills/` 下 5 vendored + 3 first-party 落地为 `packs/` 真实载荷

- 状态: 草稿
- 主题: 在 `packs/` 引入 vendored pack 契约（`pack.json` 增可选 `upstream` / `license` 字段），把当前 `.agents/skills/` 下 5 个 vendored pack（`harness-flow` / `architecture-designer` / `write-blog` / `ui-ux-pro-max` / `writing-skills`）+ 3 个 first-party skill（`find-skills` / `vision-obey` / `writing-docs`）按 F007 安装管道可分发的形态落地，让下游用户 `garage init --hosts ...` 第一次拿到真正可用的能力基座；保留 `.agents/skills/` 顶层扁平 symlink 投影层让本仓库 cursor / claude code 体验零变更。
- 日期: 2026-04-21
- 关联:
  - F007（Garage Packs 与宿主安装器）— 已批准；本 cycle 直接消费其安装管道、`pack.json` schema、`.garage/config/host-installer.json` 清单、conflict 检测；本 cycle 不动 F007 已建立的 `HostInstallAdapter` Protocol 与 manifest schema_version
  - F001 `CON-002` — 显式声明 "Skills 存放在 `packs/coding/skills/` 和 `packs/product-insights/skills/`"；本 cycle **修订** F001 这一具体约束（pack 命名空间不强制按 family，按 vendored vs first-party + upstream 身份组织）
  - F007 closeout 候选清单（`task-progress.md` / `RELEASE_NOTES.md`）— "F008 候选 — 把 `.agents/skills/` 30 个 HF skills 搬迁到 `packs/coding/skills/`" 在本 cycle hf-specify step 1 审计后被推翻为"5 vendored + 3 first-party 的契约+迁移"
  - `docs/soul/manifesto.md` — "挂载 Garage 几秒后 Agent 就变成你的 Agent"；本 cycle 让此承诺第一次有真实载荷可验证
  - `docs/soul/user-pact.md` § 1 能力不丢失、§ 2 宿主自由、§ 4 透明可审计
  - `docs/soul/design-principles.md` § 1 宿主无关原则、§ 2 文件即契约、§ 4 自描述
  - `docs/principles/skill-anatomy.md` — pack 内 skill 写作原则（本 cycle 不修改）

## 1. 背景与问题陈述

### 1.1 F007 留下的兑现缺口

F007 cycle 把 `packs/` 容器、安装管道、三家宿主 adapter、安装清单都铺好了，但 `packs/` 里**只有 1 个占位 sample skill `garage-hello`**。当前下游用户在自己的项目里执行 `garage init --hosts claude` 得到的几乎是空壳——`.claude/skills/garage-hello/SKILL.md` 一个 demo，`.garage/config/host-installer.json` 里 `installed_packs: ["garage"]` / `files: [1 个]`。这与 `docs/soul/manifesto.md` 的承诺存在**显著缺口**：

> 你打开任何一个 Agent 宿主，挂上你的 Garage 目录。几秒后，这个 Agent 就变成了**你的 Agent**——它知道你的编码风格、记得你上个月的架构决策、能调用你积累的 50 个 skills、知道怎么帮你写博客。

要兑现"50 个 skills、写博客、HF workflow、UI 设计"这些承诺，必须把 `.agents/skills/` 下既有能力实际进入 `packs/` 这条分发管道。

### 1.2 hf-specify Step 1 审计推翻原始假设

启动本 cycle 时（router decision 见 `task-progress.md` 上一轮记录），原始假设是"30 个 HF skill 是 Garage 自有内容，可机械搬到 `packs/coding/skills/`"。Step 1 进入 `.agents/skills/` 做 first-party vs vendored 审计后，事实推翻了这一假设：

| 实际身份 | 名字 | 上游 / 来源 | 关键证据 |
|---|---|---|---|
| **Vendored pack** | `harness-flow/` （整体子树） | HarnessFlow upstream | git log: `chore(skills): sync harness-flow to upstream 0dd0d12`；自带 `README.md` / `README.zh-CN.md` / `docs/principles/`；含 22 hf-* + using-hf-workflow 的 SKILL.md |
| **Vendored pack** | `architecture-designer` | `jeffallan/claude-skills` | `skills-lock.json` 显式记录 `source: jeffallan/claude-skills`；`SKILL.md` front matter 含 `license: MIT` / `metadata.author: github.com/Jeffallan` / `metadata.version: "1.1.1"` |
| **Vendored pack** | `write-blog/` （整体子树） | `KKKKhazix/khazix-skills` | 自带 `LICENSE`(MIT, copyright 数字生命卡兹克) + `README.md` 显式声明 upstream URL；含 4 子 skill (`blog-writing` / `humanizer-zh` / `hv-analysis` / `khazix-writer`) + `prompts/横纵分析法.md` |
| **Vendored pack**（推断） | `ui-ux-pro-max` | 无显式 upstream URL | 含 `data/`(csv 大型数据) + `scripts/`(Python) + 67 styles 等大型数据资产；明显非 Garage 自写 |
| **Vendored pack**（推断） | `writing-skills` | Anthropic skill 写作示例 | 自带 `anthropic-best-practices.md`（Anthropic 官方文档原文）+ `persuasion-principles.md` + `render-graphs.js` + `examples/`，明显是 Anthropic skill 教学包 |
| **First-party skill** | `find-skills` | Garage 自写 | git log "手动重构 Garage 项目结构"；只有 SKILL.md，无附加资产 |
| **First-party skill** | `vision-obey` | Garage 自写 | git log "T100执行完成"（Garage hf-task 编号）；显式服务 Garage `docs/soul/` 决策守护 |
| **First-party skill** | `writing-docs` | Garage 自写 | git log "添加 docs 编辑 skill"；description 字面量 "Use when adding, updating, or relocating Garage system documentation under docs/" |

并且：`.agents/skills/` 顶层 22 个 `hf-*` + `using-hf-workflow` 是 **git symlink (mode 120000)**，指向 `harness-flow/skills/<name>/`。它们是宿主（cursor / claude code）扁平化扫描方便用的"投影层"，不是独立源。

### 1.3 真正要解决的问题

由审计可知，F008 不是"机械搬运 30 个文件"，而是要回答 4 个真问题：

1. **vendored pack 怎么进 `packs/`？** F007 `pack.json` schema_version=1 当前 5 字段（`schema_version` / `pack_id` / `version` / `description` / `skills` / `agents`）没有声明 vendored 身份的字段；如果直接搬，pack 就丢失了"我来自外部上游、不可随意修改"的关键信息，下次 upstream 升级时 Garage 维护者无从判断哪些字节可改、哪些不能改，违反 `docs/soul/design-principles.md` § 4 自描述原则。
2. **first-party skill 怎么和 vendored 区分？** 3 个 first-party skill (`find-skills` / `vision-obey` / `writing-docs`) 服务 Garage 内部认知 / docs / soul 决策；它们与 vendored 的"我是外部 vendored 的，按上游一致"语义完全不同。直接和 vendored 混在同一个 pack 会让下游用户区分不出"哪些是 Garage 自己保证的、哪些只是 vendored 转发"。
3. **`.agents/skills/` 顶层 symlink 投影层怎么处理？** 本仓库 cursor / claude code session 当前依靠 `.agents/skills/<name>/SKILL.md` 一层扫描加载。如果迁移破坏这条路径，本仓库自身 dogfood 立刻失效；如果保留则需要让 symlink 指向新位置。
4. **vendored 升级（upstream sync）怎么不被 F008 写死？** 本 cycle 不可能也不应该建立完整 sync 工具链（那是单独 cycle）；但 spec 必须把"vendored 升级是后续 cycle 的能力"显式写下来，避免本 cycle 工件在未来变成 sync 工具的障碍。

### 1.4 如果不在本 cycle 解决

- F007 安装管道的 ROI 卡死在"1 sample skill"，manifesto"几秒变成你的 Agent"承诺继续悬空
- `.agents/skills/` 这个目录身份继续模糊（混 vendored + first-party + symlink 三种语义），任何后续 cycle 想动 skill 都要先做一次同样的审计
- `F001 CON-002` 关于 `packs/coding/` 的旧约束继续被错误引用为"未兑现"（实际上它已不再是合理目标——按 family 命名空间组织 vendored pack 会破坏 upstream 身份）

## 2. 目标与成功标准

### 2.1 核心目标

把 F007 已建立的 `packs/` 容器扩展为可容纳 **vendored pack + first-party pack 两类身份**的目录契约，并完成首批迁移：

```
源（宿主无关 + 身份可冷读）：

packs/
├── garage/                       ← first-party；含 garage-hello (sample) + find-skills + vision-obey + writing-docs
├── harness-flow/                 ← vendored from HarnessFlow upstream；22 hf-* + using-hf-workflow
├── architecture-designer/        ← vendored from jeffallan/claude-skills
├── write-blog/                   ← vendored from KKKKhazix/khazix-skills
├── ui-ux-pro-max/                ← vendored
├── writing-skills/               ← vendored from Anthropic skill 教学
└── README.md                     ← 顶层 README + Packs Inventory（含每个 pack 的身份）

动作（F007 已建立，本 cycle 复用）：

garage init --hosts claude,cursor,opencode
└── 把 6 packs 全部物化到下游项目的对应宿主目录
└── .garage/config/host-installer.json 清单累加 6 个 pack 的全部 file entries

兼容（本 cycle 新增）：

.agents/skills/<name>/  ← 保留为 git symlink，指向 packs/<pack-id>/skills/<skill-id>/
                          → 本仓库 cursor / claude code 体验零变更
                          → packs/ 是唯一真实源，symlink 是宿主扁平化适配
```

本 cycle 收敛：

- `pack.json` schema_version=1 增 2 个**可选**字段：`upstream` (object) + `license` (string)；schema_version 不变（向后兼容 F007）
- `packs/<pack-id>/README.md` 强制（F007 已要求；本 cycle 为 5 个新 pack 各落 1 份）
- `packs/garage/` 扩展为含 4 个 skill（现有 `garage-hello` + 新加 `find-skills` / `vision-obey` / `writing-docs`）
- 5 个 vendored pack 通过 `git mv` 整体从 `.agents/skills/<name>/` 搬到 `packs/<name>/`
- `.agents/skills/` 重建为顶层 symlink 投影层（`.agents/skills/<skill-id>/` → `../../packs/<pack-id>/skills/<skill-id>/`）
- `AGENTS.md` 增 `## Packs Inventory` 子段
- `packs/README.md` 顶层 inventory 同步 + vendored pack 形态说明
- `docs/principles/skill-anatomy.md` 路径引用更新（`.agents/skills/` → `packs/<pack-id>/skills/`）
- `skills-lock.json` 字段含义对齐（明确这是 vendored skill 来源记录，而不是 first-party）

**显式不在本 cycle 内**（见 § 5）：

- vendored sync 自动化工具（`scripts/sync-vendored-packs.sh` 或等价）—— 这是后续 cycle 候选；本 cycle 仅在 `pack.json.upstream.rev` 字段记录当前固定版本，未来手工 `git subtree pull` 处理
- `pack.json` schema_version 升级到 2 —— 本 cycle 仅新增**可选**字段，schema_version 仍保持 1，向后兼容
- 把 vendored pack 内部某条 skill 单独抽到 first-party pack（如把 `harness-flow/skills/hf-design-review/` 提到 `packs/garage/skills/hf-design-review/` 做 Garage 风味改造）—— 这破坏 upstream 一致性，应作为单独探索性 cycle
- 新增 first-party skill —— 本 cycle 只搬迁现有 3 个，不创作新 skill
- `.cursor/skills/` / `.claude/skills/` 等 dogfood 安装产物的 git 提交 —— 本仓库 cursor / claude code 体验通过 `.agents/skills/` symlink 保留，不需要在 git 里物化宿主目录

### 2.2 成功标准

1. **零回归 dogfood 体验**：本 cycle 所有迁移完成后，本仓库 cursor / claude code session 在不修改任何 cursor/claude 配置的前提下，仍能 100% 加载现有 30 个 skill（Cursor 扫描 `.agents/skills/<name>/SKILL.md` 路径形态完全不变；只是 `<name>` 现在是 symlink）。判定：在 `.agents/skills/` 下 `find . -name SKILL.md -follow` 数量与本 cycle 启动前一致（30 个 SKILL.md），每个 SKILL.md 的字节内容与启动前 byte-for-byte 一致。
2. **下游 `garage init` 真正装出可用载荷**：在一个干净 clone 的 Garage 仓库里，`garage init --hosts claude` 一行命令必须把所有 6 个 pack 的 30 个 SKILL.md 物化到 `.claude/skills/<skill-id>/SKILL.md`，退出码 0，stdout 显式列出 `Installed 30 skills, 1 agents into hosts: claude`，且 `.garage/config/host-installer.json` 的 `installed_packs` 必须是 6 个 pack 全部、`files[]` 长度必须 = 30 SKILL.md + 1 sample agent + 任何被 install 的 pack-internal 资产（见 FR-805）。
3. **vendored pack 身份冷读**：任何新 Agent 仅读 `packs/harness-flow/pack.json` 一份文件，必须能回答 (a) 这个 pack 来自哪个 upstream、(b) 当前 pinned 在哪个 rev、(c) 它的 license。
4. **first-party 与 vendored 边界冷读**：任何 Agent 仅读 `packs/README.md` 顶层 Packs Inventory 表 + `AGENTS.md ## Packs Inventory` 子段，必须能在 5 分钟内回答"哪些 pack 是 Garage 自己保证的、哪些是 vendored 转发"。
5. **`.agents/skills/` symlink 不变量**：`.agents/skills/<name>/` 全部 30 个目录必须是 git mode 120000 (symlink)，target 指向 `packs/<pack-id>/skills/<skill-id>/`；`packs/` 才是真实文件源。判定：`git ls-tree HEAD .agents/skills/ | grep -v "^120000" | wc -l` 必须为 0（除根 README 类元文件外），即 0 个 mode 040000 (real tree)。
6. **不破坏 F007 契约 / 测试**：`HostInstallAdapter` Protocol、`HOST_REGISTRY`、`pipeline.install_packs()`、`MANIFEST_SCHEMA_VERSION = 1`、cli.py 全部 stdout/stderr 常量、F007 conflict 检测全部零修改；`uv run pytest tests/ -q` 在 F007 基线 586 测试上仅新增、不退绿。
7. **vendored pack 内 SKILL.md 字节零修改**：5 个 vendored pack 整体迁移采用 `git mv`，pack 内任何 SKILL.md / 附加资产文件的字节内容必须与迁移前完全一致（含 LICENSE、README、`docs/principles/` 等）。判定：对每个 vendored pack 的每个文件做 `git diff <before-rev>:<old-path> <after-rev>:<new-path>` 必须为空 diff（Git 自动识别 rename）。
8. **AGENTS.md 与文档可冷读链路**：`AGENTS.md` 顶部的 `## Packs Inventory` 子段必须列每个 pack 的 (id / 身份 / skill 数 / agent 数 / upstream)；`packs/README.md` 必须更新到反映 6 个 pack 现状；`docs/principles/skill-anatomy.md` 必须替换所有 `.agents/skills/` 路径引用为 `packs/<pack-id>/skills/`（如有）。

### 2.3 非目标

- 不在本 cycle 实现 vendored pack 升级 / sync / lockfile / diff 工具链
- 不在本 cycle 修改任何 vendored pack 内的 SKILL.md / 附加资产 / README / LICENSE 内容
- 不在本 cycle 创作新 skill（无论 first-party 还是其它）
- 不在本 cycle 修改 F007 安装管道的 Python 代码逻辑（`src/garage_os/adapter/installer/`）
- 不在本 cycle 修改 `pack.json` schema_version 或既有必填字段
- 不在本 cycle 物化 `.cursor/skills/` / `.claude/skills/` 安装产物到 git（dogfood 通过 symlink 保留，安装产物按 F007 NFR-702 由用户在自己仓库 `garage init` 时生成）
- 不在本 cycle 拆分 vendored pack 内某条 skill 到 first-party pack（破坏 upstream 一致性）
- 不在本 cycle 引入对 `harness-flow/` 内 22 hf-* skill 的任何"Garage 风味"改造
- 不在本 cycle 重新设计 `.agents/skills/` 目录的 user-facing 含义（继续视为"宿主扁平化扫描入口"，仅是 symlink 投影层）

## 3. 用户角色与关键场景

### 3.1 用户角色

| 角色 | 关心什么 |
|---|---|
| **Garage 维护者**（本仓库开发者） | 本仓库 cursor / claude code session 不能因迁移失效；vendored pack 升级路径不被堵死；first-party 与 vendored 边界清晰，知道哪些字节可改、哪些不能改 |
| **下游用户**（在自己项目里 `garage init`） | `garage init --hosts ...` 一行真的能装出能用的能力基座；安装清单清晰；任何 SKILL.md 能追溯到 Garage 哪个 pack |
| **Agent 冷读者**（任何新 session） | 仅读 `packs/README.md` + `packs/<id>/pack.json` + `AGENTS.md` 三份文件就能完整回答"这个仓库有哪些 pack、各自身份、各自来源" |

### 3.2 关键场景

1. **Garage 维护者本仓库 dogfood**：维护者打开本仓库的 cursor session，cursor 扫描 `.agents/skills/`，看到 30 个目录全部是 symlink 指向 `packs/<pack-id>/skills/<skill-id>/`，cursor 跟随 symlink 加载 SKILL.md。维护者写代码 / 调用 hf-* skill 的体验**完全不变**。判定：`/skill hf-design` 等命令工作；`.agents/skills/hf-design/SKILL.md` 内容（通过 symlink 解析）字节级与启动前一致。
2. **下游用户首次安装**：用户在 `~/projects/my-app` 执行 `git clone <garage-repo>` 后 `cd my-app && cp -r <garage-repo>/packs ./packs && garage init --hosts claude,cursor`（或更直接的 `garage` 全局安装后调用）。CLI 输出 `Installed 30 skills, 1 agents into hosts: claude, cursor`，`.claude/skills/` 与 `.cursor/skills/` 各 30 个子目录，每个含 SKILL.md，且 SKILL.md front matter 末尾追加 `installed_by: garage` + `installed_pack: <pack-id>`（F007 ADR-D7-2 已建立的标记机制，本 cycle 复用）。
3. **下游用户审计某个 skill 来源**：用户在 `.claude/skills/blog-writing/SKILL.md` 看到 `installed_pack: write-blog`，于是 `cat .garage/config/host-installer.json | jq '.files[] | select(.dst | contains("blog-writing"))'` 拿到 `src: packs/write-blog/skills/blog-writing/SKILL.md` / `pack_id: write-blog`，再读 `packs/write-blog/pack.json` 拿到 `upstream.source: https://github.com/KKKKhazix/khazix-skills`，完整溯源链路冷读完成。
4. **Garage 维护者升级 vendored pack**（本 cycle 不实现，但场景必须不被堵死）：HarnessFlow 上游发布新 rev，维护者 `cd packs/harness-flow && git subtree pull --prefix=packs/harness-flow <upstream-url> main`（或等价手工动作），冲突按 git 标准流程解决；解决后手工把 `pack.json.upstream.rev` 字段从旧 sha 改到新 sha。本 cycle 不提供脚本，但目录结构必须支持这条路径。
5. **下游用户报告"某个 skill 不工作"**：用户 cursor session 加载 `architecture-designer` 出错。维护者读 `packs/architecture-designer/pack.json` 拿到 `upstream.source: jeffallan/claude-skills`，于是知道该 skill 不是 Garage 自维护的，建议用户去 upstream 仓库报告，或在 Garage 这一侧维护一个 patch（这是后续 cycle 能力，本 cycle 仅保留语义可能性）。
6. **新 Agent 5 分钟冷读全图**：任何新会话要回答"这个 Garage 仓库有哪些 pack"——读 `packs/README.md` 顶层 Packs Inventory 表（6 行）+ 每个 pack 的 `pack.json`（6 个文件）+ `AGENTS.md ## Packs Inventory` 段。3 处全部冷读完，回答完整。

## 4. 当前轮范围与关键边界

### 4.1 包含

| 能力 | 描述 |
|---|---|
| `pack.json` schema 扩展（向后兼容） | `schema_version` 仍为 1；新增可选字段 `upstream: { source: string, rev: string, sync_method?: string }` 与 `license: string`；缺省时表示 first-party + 由 Garage 决定 license（默认 MIT or 跟随项目根 LICENSE） |
| `packs/garage/` 扩展 | 现有 `garage-hello` (sample) + 新加 `find-skills` / `vision-obey` / `writing-docs` 三个 first-party skill；`pack.json.skills` 从 `["garage-hello"]` 改为 4 个；不带 `upstream` 字段 |
| `packs/harness-flow/` 落地 | 整体 `git mv` 从 `.agents/skills/harness-flow/` → `packs/harness-flow/`；新加 `pack.json` 含 `upstream`（source 指向 HarnessFlow upstream，rev 锁当前 sha 即 commit `92526b6` 关联的 upstream `0dd0d12`）+ `license` |
| `packs/architecture-designer/` 落地 | 整体 `git mv`；新加 `pack.json` 含 `upstream` (source: jeffallan/claude-skills，rev: 从 `skills-lock.json.architecture-designer.computedHash` 取) + `license: MIT` |
| `packs/write-blog/` 落地 | 整体 `git mv`；新加 `pack.json` 含 `upstream` (source: KKKKhazix/khazix-skills，rev: 暂留 `null` 或 git log 推测) + `license: MIT`；保留 `LICENSE` / `README.md` / `prompts/` 子目录原样 |
| `packs/ui-ux-pro-max/` 落地 | 整体 `git mv`；新加 `pack.json` 含 `upstream`（source `null` + 注明 "upstream URL unknown, treated as vendored, license inferred from absent attribution") + `license` 字段值 `unknown` 或保守按 MIT 处理（待 step 7 开放问题） |
| `packs/writing-skills/` 落地 | 整体 `git mv`；新加 `pack.json` 含 `upstream` (source: Anthropic skill 教学，具体 URL 待 review 阶段补) + `license` (Anthropic 文档版权，附 attribution 字段) |
| `.agents/skills/` 顶层 30 个 symlink | 全部重建为 git symlink (mode 120000)，target 指向 `../../packs/<pack-id>/skills/<skill-id>/`；现有顶层 23 个 symlink 已经是这种形态（指向 `harness-flow/skills/...`），本 cycle 把 target 改为新位置 + 新加 7 个 symlink（4 个 first-party 移入 garage pack 的 + 3 个 vendored 单 skill pack） |
| `packs/README.md` 更新 | 顶层 Packs Inventory 表 6 行；新增 "Vendored Pack" 段说明 vendored 形态、`upstream` 字段语义、维护者升级路径；既有 "Dogfood 与下游用法" 段微调（30 个 skill 替代之前 1 个 sample） |
| 每个 pack 的 `packs/<id>/README.md` | 6 个 pack 各落 1 份 README（已有 `packs/garage/README.md` 需扩；其它 5 个新建）；模板：身份 / upstream / skill 列表 / license / 维护者注意事项 |
| `AGENTS.md` 更新 | 增 `## Packs Inventory` 子段（在现有 `## Packs & Host Installer` 之后）；表 6 行 `(id / 身份 / skill 数 / agent 数 / upstream)`；既有路径引用 `.agents/skills/...` 全部更新为 `packs/<pack-id>/skills/...` |
| `docs/principles/skill-anatomy.md` 更新 | 替换所有 `.agents/skills/` 路径引用为 `packs/<pack-id>/skills/`（grep 后逐处确认） |
| `skills-lock.json` 更新 | 现有 `architecture-designer` entry 保留；新增 5 个 vendored pack entry（vendored 但 lock 信息暂为 `rev` 字段；详细 schema 在 design 阶段决定） |
| F007 NFR-701 grep 守护扩张 | F007 既有 grep 测试 `packs/` 不出现 `.claude/` / `.cursor/` / `.opencode/` / `claude-code` 字面量，本 cycle 自动覆盖 5 个新 pack（无需新测试，新 pack 落入 grep 路径即生效） |
| 测试新增 | (a) `pack_discovery` 能识别 6 个 pack；(b) `garage init --hosts <list>` E2E smoke 在干净仓库装出 30 个 SKILL.md；(c) `.agents/skills/` symlink 健康度（30 个全部是 symlink 且 target 可解析）；(d) vendored pack 字节零修改契约测试（pre-migration content_hash vs post-migration content_hash 相等） |

### 4.2 关键边界

- **vendored pack 字节不可改**：本 cycle 任何 vendored pack 的 SKILL.md / 附加资产 / README / LICENSE / 子目录文件必须 byte-for-byte 与 `.agents/skills/` 启动前一致（`git mv` 自动保证；CI 用 content_hash 比对守护）
- **`pack.json` 是 Garage 维护文件**：每个 pack 根的 `pack.json` 是 Garage 添加的元描述，不属于 vendored 内容，可由 Garage 自由维护；vendored pack 升级时 `pack.json.upstream.rev` 是唯一需要更新的字段
- **symlink 是 git-tracked**：`.agents/skills/<name>/` 是 git 真 symlink（mode 120000），不是 OS-level symlink；clone 仓库时 git 自动恢复；本 cycle 验证 symlink 在 macOS / Linux 两类 OS 上均能正常解析（Windows 不在 Garage 当前支持矩阵）
- **first-party pack 仅扩 `packs/garage/`**：本 cycle 不创建 `packs/find-skills/` / `packs/vision-obey/` / `packs/writing-docs/` 三个独立 first-party pack；3 个 first-party skill 全部归并到 `packs/garage/`（理由：避免单 skill 单 pack 碎片；`packs/garage/` 是 Garage 自有能力的统一入口）
- **本仓库自身不提交 dogfood 安装产物**：本 cycle 不在本仓库 git 提交 `.cursor/skills/` 或 `.claude/skills/` 任何安装产物；本仓库 cursor 用 `.agents/skills/` symlink 投影层，不需要安装步骤
- **`garage` CLI 行为零变化**：本 cycle 仅修改文件 layout 与 `pack.json` 字段（向后兼容），不修改 `src/garage_os/adapter/installer/` 任何 Python 代码；F007 既有 CLI flag / stdout 常量 / 退出码 / 安装清单 schema 全部不动
- **`pack.json` 新字段必须 lenient parsing**：F007 既有 `pack_discovery` 代码读 `pack.json` 时如果发现未知字段（即未来加的字段），必须忽略不报错；本 cycle 验证 F007 既有解析逻辑确实是 lenient（如非则在 design 阶段补一个最小修复，但仍力争 0 Python 修改）

### 4.3 与 F001 / F007 的边界

| 既有契约 | F008 影响 |
|---|---|
| `F001 CON-002` 约束 "Skills 存放在 `packs/coding/skills/`" | **修订**：本 cycle 改为按 `vendored vs first-party + upstream 身份` 命名 pack，而不是按 family 命名空间；`packs/coding/` 这一具体名字不再适用，`F001 CON-002` 应在 finalize 阶段同步修订 |
| F007 `pack.json` schema_version=1 必填字段 | **保留全部 5 必填字段**；仅新增 2 可选字段（`upstream` / `license`）；schema_version 不变 |
| F007 `HostInstallAdapter` Protocol + `HOST_REGISTRY` | **零修改**；本 cycle 不动 Python 代码 |
| F007 `MANIFEST_SCHEMA_VERSION = 1` + `.garage/config/host-installer.json` schema | **零修改**；本 cycle 不动安装清单 schema |
| F007 conflict 检测（同名 skill 跨 pack 退出码 2） | **必须在新 6 packs 下零冲突**；判定：`grep -r "^name:" packs/*/skills/*/SKILL.md \| awk '{print $2}' \| sort \| uniq -d` 应为空（含 30 个 unique skill name + 0 重复） |
| F007 安装标记 `installed_by: garage` + `installed_pack: <pack-id>` | **复用**；F007 既有逻辑会自动给新 pack 打标记，不需要改 |
| F007 `_recommend_experience` / `KnowledgeStore` / Memory（F003-F006） | **零回归**；本 cycle 不读写知识/经验存储 |

## 5. 范围外内容（显式 deferred backlog）

下列项目真实存在且会发生，但**显式不在 F008**；按"延后到下一个 cycle"处理：

| 项 | 为什么本 cycle 不做 | 期望落点 |
|---|---|---|
| Vendored pack 升级 / sync 自动化（`scripts/sync-vendored-packs.sh` 或等价） | 复杂工具链；本 cycle 收敛在"契约 + 首批迁移"；手工 `git subtree pull` 已能满足升级路径 | F009 候选（与 garage uninstall / update 合并 cycle） |
| `garage uninstall --hosts <list>` + `garage update --hosts <list>` | F007 已显式 deferred；F008 完成后下游用户首次拥有真实可 uninstall / update 的载荷，价值才完整体现 | F009 候选 |
| 把 vendored pack 内某条 skill 单独抽到 first-party pack 做"Garage 风味"改造（如 fork `hf-design-review`） | 破坏 upstream 一致性；需要单独设计 fork-vs-vendored 边界 | 单独探索性候选 |
| 创作新 first-party skill | 本 cycle 仅搬迁现有 3 个，不创作 | 任何后续 cycle 按需 |
| `pack.json` schema_version 升级到 2 | 本 cycle 仅新增**可选**字段，schema_version 仍保持 1；当未来出现破坏性 schema 变更（如 `upstream` 改为必填）时再 bump | 触发条件出现时单独 cycle |
| 全局安装到 `~/.claude/skills/` | F007 已显式 deferred | 单独候选 |
| 新增宿主（Codex / Gemini CLI / Windsurf / Copilot） | F007 已铺好 adapter 注册模式；本 cycle 完成后 30 个 skill 在新 host 自动可用 | F008+ 增量候选 |
| Pack Marketplace / 远程分发 / lockfile 版本管理 | Stage 2 范围外 | Stage 3+ 候选 |
| `.agents/skills/` symlink 投影层是否长期存在 | 本 cycle 保留为零回归；未来如果所有维护者都改用 `garage init` dogfood，可考虑废弃 | 单独决策（社区使用习惯成熟后再说） |
| 物化 `.cursor/skills/` / `.claude/skills/` 安装产物到本仓库 git | dogfood 通过 symlink 已解决；物化等于加 git 噪音 | 不计划做 |

## 6. 功能需求

### FR-801 `pack.json` schema 向后兼容扩展（vendored 身份字段）

- **优先级**: Must
- **来源**: 用户请求（hf-specify Q1' 修订决策选 A）；`docs/soul/design-principles.md` § 4 自描述原则
- **需求陈述**: 系统必须把 `pack.json` schema_version=1 扩展为接受 2 个新的可选字段——`upstream: { source: string, rev: string, sync_method?: string }` 与 `license: string`，不修改任何既有必填字段（`schema_version` / `pack_id` / `version` / `description` / `skills[]` / `agents[]`）。
- **验收标准**:
  - Given `packs/garage/pack.json` 仍然没有 `upstream` 字段，When `pack_discovery` 读取它，Then 必须正确识别为 first-party pack（无 upstream 即视为 first-party），不报错。
  - Given `packs/harness-flow/pack.json` 含 `upstream: { source: "<url>", rev: "<sha>", sync_method: "manual-subtree" }` + `license: "MIT"`，When `pack_discovery` 读取它，Then 必须正确把这 2 个字段透传到 pack metadata，可被任何 Agent 冷读拿到 `upstream.source` / `upstream.rev` / `license` 三个值。
  - Given `pack.json` 含未来才会加的字段（如 `tags: [...]`），When `pack_discovery` 读取它，Then 必须**忽略**未知字段而不是报错（lenient parsing）。

### FR-802 `packs/garage/` 扩展为 4 skill first-party pack

- **优先级**: Must
- **来源**: 用户请求（hf-specify 审计后 3 个 first-party skill `find-skills` / `vision-obey` / `writing-docs` 全部归 garage pack）
- **需求陈述**: 系统必须把现有 3 个 first-party skill (`find-skills` / `vision-obey` / `writing-docs`) `git mv` 到 `packs/garage/skills/<skill-id>/`，更新 `packs/garage/pack.json.skills` 从 `["garage-hello"]` 改为 `["garage-hello", "find-skills", "vision-obey", "writing-docs"]`，更新 `packs/garage/README.md` 反映 4 skill 现状。
- **验收标准**:
  - Given 迁移完成，When `find packs/garage/skills -name SKILL.md \| wc -l`，Then 输出必须为 4。
  - Given 任何 SKILL.md 在迁移前后，When 比对 `packs/garage/skills/<id>/SKILL.md` 的 SHA-256 与迁移前 `.agents/skills/<id>/SKILL.md` 的 SHA-256，Then 两者必须相等（byte-for-byte 一致）。
  - Given `packs/garage/pack.json`，When 任何 Agent 冷读，Then 必须看到 `skills: ["garage-hello", "find-skills", "vision-obey", "writing-docs"]`，且**没有** `upstream` 字段（first-party pack 标识）。

### FR-803 5 个 vendored pack `git mv` 落地 `packs/<id>/`

- **优先级**: Must
- **来源**: hf-specify 审计；`docs/soul/manifesto.md` "几秒变成你的 Agent"
- **需求陈述**: 系统必须把 5 个 vendored pack 整体从 `.agents/skills/<name>/` `git mv` 到 `packs/<name>/`，并为每个 pack 新建 `pack.json`（含 `upstream` + `license` + 标准必填字段）和 `README.md`：
  - `harness-flow/`（22 hf-* + using-hf-workflow + docs/principles/）
  - `architecture-designer/`
  - `write-blog/`（4 子 skill + LICENSE + prompts/）
  - `ui-ux-pro-max/`（含 data/ + scripts/）
  - `writing-skills/`（含 anthropic-best-practices.md / persuasion-principles.md / examples/ / render-graphs.js）
- **验收标准**:
  - Given 迁移完成，When `ls packs/`，Then 必须列出至少 6 个目录：`garage`、`harness-flow`、`architecture-designer`、`write-blog`、`ui-ux-pro-max`、`writing-skills`。
  - Given 5 个 vendored pack 内任意文件 `<f>`，When 对比迁移前 `.agents/skills/<old-path>/<f>` 与迁移后 `packs/<pack-id>/<new-path>/<f>` 的 SHA-256，Then 两者必须相等（vendored 字节零修改不变量）。
  - Given 5 个 vendored pack 各自 `pack.json`，When 任何 Agent 冷读，Then 必须能读到 `upstream.source` / `upstream.rev` / `license` 三个字段（值可以是 `null` 或 `"unknown"` 但字段必须存在）。
  - Given 5 个 vendored pack 各自 `README.md`，When 任何用户冷读，Then 必须能在 1 分钟内回答 (a) 这个 pack 来自哪里、(b) 含哪些 skill、(c) 升级方法。

### FR-804 `.agents/skills/` symlink 投影层重建

- **优先级**: Must
- **来源**: hf-specify Q2' 修订决策选 A（保留 symlink 让本仓库 cursor 体验零变更）
- **需求陈述**: 系统必须把 `.agents/skills/` 下所有 30 个 skill 子目录全部重建为 git symlink (mode 120000)，target 为 `../../packs/<pack-id>/skills/<skill-id>/`（相对路径），让本仓库 cursor / claude code session 加载 skill 的路径形态完全不变。
- **验收标准**:
  - Given 迁移完成，When `git ls-tree HEAD .agents/skills/`，Then 30 个 skill 入口必须全部为 mode 120000 (symlink)，0 个 mode 040000 (real tree)；`.agents/skills/` 根下可保留少量 mode 100644 文件（如 README）但不得有任何 040000 子树。
  - Given 任意 `.agents/skills/<skill-id>/SKILL.md`，When 通过 symlink 解析，Then 必须读到 `packs/<pack-id>/skills/<skill-id>/SKILL.md` 的真实内容，且 SHA-256 与迁移前 `.agents/skills/<skill-id>/SKILL.md`（彼时为 real tree 或旧 symlink）一致。
  - Given 干净 clone 本仓库到 macOS / Linux，When `find .agents/skills -name SKILL.md -follow`，Then 必须能解析全部 30 个 SKILL.md（symlink 跟随成功）。
  - Given 本仓库 cursor session 加载 `hf-design` skill，When 调用 `/skill hf-design` 或等价命令，Then 必须正常工作，与迁移前体验完全一致。

### FR-805 `garage init --hosts <list>` 在新 6 packs 下端到端可用

- **优先级**: Must
- **来源**: § 2.1 核心目标；F007 安装管道契约延伸；§ 2.2 成功标准 #2
- **需求陈述**: 当用户在迁移完成后的 Garage 仓库或 clone 副本下执行 `garage init --hosts <list>` 时，系统必须能识别全部 6 个 pack，把它们的所有 SKILL.md 与 agent.md 按 F007 既有安装管道物化到目标宿主目录，安装清单 `installed_packs[]` 长度为 6，`files[]` 长度为全部被安装资产之和。
- **验收标准**:
  - Given 干净 clone 仓库 + 没有 `.claude/skills/`，When `garage init --hosts claude`，Then 退出码 0，`.claude/skills/` 下出现至少 30 个子目录（30 个 unique skill），stdout 含 `Installed 30 skills, 1 agents into hosts: claude` 形式提示。
  - Given 上一步完成后，When `cat .garage/config/host-installer.json | jq '.installed_packs \| length'`，Then 输出必须为 `6`。
  - Given 上一步完成后，When `cat .garage/config/host-installer.json | jq '.files[] | .pack_id' | sort -u`，Then 输出必须包含全部 6 个 pack id：`garage`、`harness-flow`、`architecture-designer`、`write-blog`、`ui-ux-pro-max`、`writing-skills`。
  - Given `garage init --hosts claude,cursor` 全部成功后，When 比对 `.claude/skills/hf-design/SKILL.md` 与 `.cursor/skills/hf-design/SKILL.md`，Then 两者去除 F007 安装标记 (`installed_by: garage` 等 front matter 字段) 后字节一致。
  - Given `garage init --hosts none`（或任何不安装宿主的路径），When 命令运行，Then 退出码仍为 0，且 `.garage/config/host-installer.json.installed_packs[]` 必须包含 6 个 pack id（pack 已被发现，仅未物化），`installed_hosts: []`。

### FR-806 同名 skill 跨 pack 冲突保护（F007 既有契约延伸验证）

- **优先级**: Must
- **来源**: F007 FR-704 验收 #4 既有契约；本 cycle 6 packs 下首次大规模验证
- **需求陈述**: 系统必须保证当前 6 packs 下不存在同名 skill；若未来某 cycle 引入同名冲突，F007 既有 conflict 检测必须以退出码 2 + stderr 列出冲突 source/dest。
- **验收标准**:
  - Given 6 packs 全部落地，When `find packs/*/skills -maxdepth 2 -name SKILL.md \| xargs grep -l "^name: " \| xargs -I{} sh -c 'grep "^name: " {} \| head -1' \| awk '{print $2}' \| sort \| uniq -c \| awk '$1 > 1'`，Then 输出必须为空（0 重复）。
  - Given 故意创建一个同名 skill（如 `packs/coding-fake/skills/hf-design/SKILL.md`），When `garage init --hosts claude`，Then 必须退出码 2 + stderr 列出冲突。

### FR-807 `AGENTS.md` 增 `## Packs Inventory` 子段

- **优先级**: Must
- **来源**: hf-specify Q5 默认建议；`docs/soul/design-principles.md` § 5 约定可发现
- **需求陈述**: 系统必须在 `AGENTS.md` 已有 `## Packs & Host Installer` 段之后增 `## Packs Inventory` 子段，以表格列出 6 个 pack 的 (pack id / 身份: first-party 或 vendored / skill 数 / agent 数 / upstream URL 或 `—`)。
- **验收标准**:
  - Given `AGENTS.md` 更新完成，When 任何新 Agent 仅读 `AGENTS.md`，Then 必须能在 5 分钟内回答 "本仓库有哪些 pack、各自身份、各自 upstream"。
  - Given Inventory 表，When grep `vendored\|first-party`，Then 必须命中至少 6 处（每行 1 处身份标记）。
  - Given Inventory 表 6 行的 `skill 数` 列加总，Then 必须等于 30。

### FR-808 `packs/README.md` 顶层 Inventory 与 vendored 形态说明

- **优先级**: Must
- **来源**: § 2.2 成功标准 #4；F007 NFR-103 5 分钟冷读链
- **需求陈述**: 系统必须更新 `packs/README.md` 顶层 Packs Inventory 表反映 6 packs 现状，并新增 "Vendored Pack" 段说明 vendored 形态、`upstream` 字段语义、维护者升级路径（手工 `git subtree pull` + 手工更新 `pack.json.upstream.rev`）。
- **验收标准**:
  - Given `packs/README.md` 更新完成，When 任何 Agent 冷读它，Then 必须能回答 (a) 6 个 pack 各自身份、(b) `upstream` 字段三个 sub-field 含义、(c) 维护者升级 vendored pack 的标准动作（即使本 cycle 不提供工具）。
  - Given Vendored Pack 段，When 任何维护者读它，Then 必须明确知道"vendored 内字节不可改 / pack.json 可改"这条边界。

### FR-809 `docs/principles/skill-anatomy.md` 路径引用更新

- **优先级**: Should
- **来源**: hf-specify Step 1 审计；目录约定一致性
- **需求陈述**: 当 `docs/principles/skill-anatomy.md` 含任何 `.agents/skills/<name>/` 形式的路径示例或引用时，系统必须把它们更新为 `packs/<pack-id>/skills/<skill-id>/` 形式，与本 cycle 落地的目录契约一致；若该文档无任何相关引用，本 FR 自然满足。
- **验收标准**:
  - Given `docs/principles/skill-anatomy.md` 更新完成，When `grep '\.agents/skills/' docs/principles/skill-anatomy.md`，Then 输出必须为空（0 处旧路径引用）。
  - Given 该文档更新后，When 任何 skill 写作者参照它创作新 skill，Then 必须能从文档示例直接推断出 "新 skill 应写到 `packs/<pack-id>/skills/<skill-id>/SKILL.md`" 而不是 `.agents/skills/`。

### FR-810 `skills-lock.json` 字段语义对齐

- **优先级**: Should
- **来源**: 既有 `skills-lock.json` 含 `architecture-designer`，需对齐为 vendored pack lock 含义
- **需求陈述**: 系统必须更新 `skills-lock.json` 反映新增 5 个 vendored pack 的 lock 信息（至少含 `source` / `sourceType` / `computedHash` 或等价 `rev` 字段）；若 lock 文件 schema 与新 vendored pack 形态不完全匹配，可在本 cycle 仅追加新 entry 而不修改既有 entry，详细 schema 调整延后到 design 阶段决定。
- **验收标准**:
  - Given `skills-lock.json` 更新完成，When 任何 Agent 读它，Then 必须能回答 "这 5 个 vendored pack 的 upstream 来源 + 当前 pinned 版本是什么"。
  - Given `skills-lock.json` 与 `pack.json.upstream.rev` 字段，When 比对同一 pack 的两处 rev 信息，Then 两者必须一致（design 阶段决定哪个是真相源；本 cycle 只要求两处不冲突）。

## 7. 非功能需求

### NFR-801 零回归：dogfood 体验不变

- **优先级**: Must
- **来源**: § 2.2 成功标准 #1
- **需求陈述**: 本仓库 cursor / claude code session 在不修改任何宿主配置的前提下，必须能继续正常加载所有 30 个 skill；用户体验与本 cycle 启动前完全一致。
- **验收标准**:
  - Given 迁移完成，When `find .agents/skills -name SKILL.md -follow \| wc -l`，Then 输出必须为 30。
  - Given 任意 skill `<id>`，When 比对 `<id>` 的 SKILL.md 内容（迁移后通过 symlink 解析）vs 迁移前（real tree 或旧 symlink 解析），Then 字节级一致。
  - Given 维护者打开 cursor session，When 调用任意 hf-* skill 或 first-party skill，Then 行为与迁移前完全一致。

### NFR-802 零回归：F007 测试基线

- **优先级**: Must
- **来源**: § 2.2 成功标准 #6
- **需求陈述**: 本 cycle 不得引入 F007 既有测试失败；`uv run pytest tests/ -q` 在 F007 基线 586 测试上仅新增、不退绿。
- **验收标准**:
  - Given 本 cycle 全部代码 + 文件迁移完成，When `uv run pytest tests/ -q`，Then 退出码 0，passed ≥ 586；新增测试数 ≥ 4（FR-805 的 6 packs 端到端 + FR-804 symlink 健康度 + vendored 字节零修改契约 + AGENTS.md inventory 一致性各 1 个）。
  - Given F007 既有 mypy / ruff 基线，When 本 cycle 完成后再次跑相同检查，Then 不引入新错误。

### NFR-803 零回归：F007 Python 代码

- **优先级**: Must
- **来源**: 本 cycle 范围边界 § 4.2
- **需求陈述**: 本 cycle 不得修改 `src/garage_os/adapter/installer/` 任何 Python 源代码；F007 既有 `HostInstallAdapter` Protocol、`HOST_REGISTRY`、`pipeline.install_packs()`、`MANIFEST_SCHEMA_VERSION` 全部 byte-for-byte 不动。
- **验收标准**:
  - Given 本 cycle 完成，When `git diff main..HEAD src/garage_os/adapter/installer/`，Then 输出必须为空（除非 design 阶段发现 lenient parsing 不存在需要最小修复——届时回到 spec 修订）。
  - Given `pack.json.MANIFEST_SCHEMA_VERSION` sentinel，When 检查 `src/garage_os/adapter/installer/manifest.py` 顶部常量，Then 必须仍为 `1`。

### NFR-804 vendored 字节零修改不变量

- **优先级**: Must
- **来源**: § 2.2 成功标准 #7；§ 4.2 关键边界
- **需求陈述**: 5 个 vendored pack 内任何文件（SKILL.md / 附加资产 / README / LICENSE / 子目录文件）必须 byte-for-byte 与迁移前一致；唯一允许 Garage 维护的是 pack 根的 `pack.json`（vendored 内不存在 `pack.json`，本 cycle 新建于 pack 根目录与 vendored 子树平级）。
- **验收标准**:
  - Given 任意 vendored pack 内文件 `<f>`，When 比对迁移前 `.agents/skills/<old>/<f>` 与迁移后 `packs/<pack-id>/<new>/<f>` 的 SHA-256，Then 两者必须相等。
  - Given 自动化 contract test，When 本 cycle 完成后跑 `pytest tests/contract/test_vendored_byte_invariant.py`（新增），Then 该测试必须通过（对 5 个 vendored pack 的所有文件做 hash 比对）。

### NFR-805 安装产物不污染本仓库 git

- **优先级**: Must
- **来源**: § 4.2 关键边界；F007 NFR-702 mtime 不变 & 安装产物属于用户 cwd
- **需求陈述**: 本 cycle 任何提交不得包含 `.claude/skills/` / `.cursor/skills/` / `.opencode/skills/` 任何安装产物；本仓库 cursor 体验通过 `.agents/skills/` symlink 解决，不需要安装。
- **验收标准**:
  - Given 本 cycle 任何 commit，When `git diff main..HEAD --stat`，Then 不得出现任何 `.claude/` / `.cursor/` / `.opencode/` 路径下的文件变更。
  - Given `.gitignore`，When 检查（按需更新），Then 必须含 `.claude/skills/`、`.cursor/skills/`、`.opencode/skills/`、`.opencode/agent/`、`.claude/agents/` 这些条目（防止维护者本地 dogfood 产物误提交）。

### NFR-806 安装清单 schema 不变

- **优先级**: Must
- **来源**: F007 manifest schema_version=1 sentinel；本 cycle 范围边界 § 4.3
- **需求陈述**: 本 cycle 不得修改 `.garage/config/host-installer.json` schema；`MANIFEST_SCHEMA_VERSION = 1` 必须保持；新 6 packs 安装出的 manifest 必须能被 F007 既有 manifest reader 正常解析。
- **验收标准**:
  - Given `garage init --hosts all` 完成，When `cat .garage/config/host-installer.json | jq '.schema_version'`，Then 必须为 `1`。
  - Given 同一 manifest 文件，When F007 既有解析逻辑读它，Then 必须能正确还原 `installed_hosts` / `installed_packs` / `files[]` 三个核心字段。

### NFR-807 Cross-OS symlink 兼容性

- **优先级**: Should
- **来源**: § 2.3 非目标隐含；solo creator 跨 macOS / Linux 使用
- **需求陈述**: `.agents/skills/` 下的 git symlink 必须在 macOS 与 Linux 两类 OS 上均能 git clone 后自动恢复并被 cursor / claude code 正常解析；Windows 不在本 cycle 验证范围（与 Garage 当前支持矩阵一致）。
- **验收标准**:
  - Given 干净 clone 到 macOS，When `ls -la .agents/skills/hf-design`，Then 必须显示为 symlink。
  - Given 干净 clone 到 Linux，When 同上，Then 同上。

## 8. 外部接口与依赖

### IFR-801 F007 安装管道接口（消费方）

- **来源**: F007 完成；本 cycle 复用而非修改
- **接口**: `pipeline.install_packs(target_root: Path, hosts: list[str], force: bool) -> InstallResult`
- **本 cycle 行为**: 仅作为消费方调用；不修改接口签名或语义；本 cycle 验证它在 6 packs 下行为正确。

### IFR-802 vendored pack upstream sync（未实现，仅声明边界）

- **来源**: § 5 deferred backlog
- **接口**: 本 cycle 不提供任何脚本或 CLI；维护者按 git 标准动作 `git subtree pull --prefix=packs/<pack-id> <upstream-url> <branch>`
- **本 cycle 行为**: spec 明确"升级动作存在 + 是手工的"，不引入工具；相关脚本作为 F009+ 候选。

## 9. 约束与兼容性要求

### CON-801 `pack.json` schema_version 保持 1

- **优先级**: Must
- **来源**: F007 ADR-D7-X（schema 变更需显式版本 bump）
- **约束**: 本 cycle 仅可向 `pack.json` 新增**可选**字段；不得修改任何既有必填字段含义；不得 bump `schema_version`；F007 `MANIFEST_SCHEMA_VERSION` 同样不动。

### CON-802 vendored pack 内字节不可改

- **优先级**: Must
- **来源**: vendored 一致性 + 升级路径不被堵死（§ 4.2）
- **约束**: 本 cycle 任何对 vendored pack 内文件（除 pack 根新建的 `pack.json` 与 `README.md`）的字节修改都被视为违反约束；CI 用 content_hash 守护。

### CON-803 不修改 F007 Python 代码

- **优先级**: Must
- **来源**: § 4.2、§ 4.3、NFR-803
- **约束**: 本 cycle 不修改 `src/garage_os/adapter/installer/` 任何文件（除非 design 阶段证明 lenient parsing 不存在必须修复，届时回 spec 修订）。

### CON-804 `.agents/skills/` 必须保持 symlink 形态

- **优先级**: Must
- **来源**: NFR-801 零回归 dogfood
- **约束**: 本 cycle 完成后 `.agents/skills/` 下所有 skill 子目录必须是 git mode 120000 (symlink)；不允许 real tree 与 symlink 混合。

### CON-805 `F001 CON-002` 修订

- **优先级**: Should
- **来源**: § 1.3、§ 4.3
- **约束**: F001 关于 `packs/coding/skills/` 的具体命名空间约束在本 cycle finalize 阶段同步修订为 "按 vendored vs first-party + upstream 身份组织 pack"，避免 F001 与 F008 之间存在已知矛盾约束。

## 10. 假设与失效影响

### ASM-801 vendored pack 内 SKILL.md 不依赖原 `.agents/skills/<name>/` 路径

- **假设**: vendored SKILL.md 内部不会以 hard-coded 方式引用 `.agents/skills/...` 路径（否则迁移到 `packs/...` 后 SKILL.md 内部链接会失效）。
- **失效影响**: 若失效，需在迁移前/后做 grep 扫描，对违反假设的字符串做 case-by-case 处理（但 vendored 字节不可改约束意味着只能在 design 阶段决定是否例外）。
- **缓解**: design 阶段先做 `grep -r "\.agents/skills" packs/` 扫描；若命中，回 spec 决策（可能引入"vendored pack 内 path placeholder"机制）。

### ASM-802 `pack_discovery` 是 lenient parsing

- **假设**: F007 既有 `pack_discovery` 代码读 `pack.json` 时遇到未知字段会忽略，不报错。
- **失效影响**: 若失效，本 cycle 无法在不改 Python 代码的前提下加 `upstream` / `license` 字段，需在 design 阶段补一个最小 lenient 修复（违反 NFR-803 但可控）。
- **缓解**: design 阶段第一步验证假设；若失效，最小修复 = 改 1 个 dataclass `**kwargs` 接受 + 测试新增 1 个 ignore-unknown-fields case。

### ASM-803 git symlink 在所有支持平台上工作

- **假设**: macOS、Linux 上的 git clone 自动恢复 mode 120000 symlink；cursor / claude code 跟随 symlink 加载 SKILL.md。
- **失效影响**: 若 cursor 不跟随 symlink，本仓库 dogfood 体验失效，需要回退到 NFR-801 备选方案（用 `.cursor/settings.json` 配置额外扫描路径）。
- **缓解**: hf-test-driven-dev 阶段做端到端验证（在 cursor 内实际加载 hf-design）。

### ASM-804 `harness-flow/` 整体子树是当前唯一 sync 单位

- **假设**: harness-flow 上游不会突然把 22 hf-* + using-hf-workflow 之外的资产（如新增 docs/principles/）改动到与 Garage 自有 `docs/principles/skill-anatomy.md` 冲突。
- **失效影响**: 若失效，下次升级 harness-flow 会引入 docs/principles 双份冲突。
- **缓解**: pack 内 `docs/principles/` 维持 vendored 字节不变；Garage 自有 `docs/principles/skill-anatomy.md` 是项目根 first-party 文档，二者已天然分离；本 cycle 不需特殊处理。

## 11. 开放问题（区分阻塞 / 非阻塞）

### OQ-801（非阻塞）`ui-ux-pro-max` 与 `writing-skills` 的精确 upstream URL

- **现状**: 两个 pack 均无显式 upstream URL；`ui-ux-pro-max` 看起来是大型数据资产 vendored，`writing-skills` 看起来是 Anthropic skill 教学包。
- **本 cycle 临时方案**: `pack.json.upstream.source` 暂填 `null` 或 `"unknown"`；附 `note` 字段说明 "upstream URL 待考证"。
- **后续**: 本 cycle 完成后，git log / 向用户求证 / 通过文件特征反查；不阻塞本 cycle 落地。

### OQ-802（非阻塞）`skills-lock.json` schema 是否需要扩展

- **现状**: 现有 schema 简单（`source` / `sourceType` / `computedHash`）；vendored pack 多了 `rev` / `license` 等维度。
- **本 cycle 临时方案**: 只追加新 entry，复用现有字段；schema 详细调整在 design 阶段决定。
- **后续**: 若发现 schema 不够用，design 阶段决定是否本 cycle 内做最小扩展或延后到 F009。

### OQ-803（非阻塞）`packs/garage/` 的 sample skill `garage-hello` 去留

- **现状**: F007 cycle 落了 `garage-hello` 作为占位 sample；本 cycle 后 `packs/garage/` 已有 4 个真实 skill。
- **本 cycle 临时方案**: 保留 `garage-hello`（不删），让 first-time user `garage init` 后能看到一个最小 demo + 3 个真实 first-party skill。
- **后续**: 若用户反馈 `garage-hello` 无价值，下个 cycle 评估是否删除。

### OQ-804（非阻塞）vendored pack 的 LICENSE 在分发后是否需要 attribution

- **现状**: `write-blog/LICENSE` 是 MIT；MIT 要求保留 copyright notice 在分发副本中。`harness-flow` / `architecture-designer` / `writing-skills` 的 license 文本未必随 SKILL.md 一起分发。
- **本 cycle 临时方案**: 各 vendored pack 的 LICENSE 文件随 vendored 子树整体保留在 `packs/<pack-id>/`；安装到下游宿主时仅安装 SKILL.md / agent.md（F007 既有行为），LICENSE 不安装到下游。
- **后续**: 若用户或 license 守护者反馈需要在下游 `.claude/skills/<name>/LICENSE` 也物化 license 文件，作为单独 cycle 增强 F007 安装管道。

## 12. 术语与定义

| 术语 | 定义 |
|---|---|
| **first-party pack** | 由 Garage 维护者创作和维护的 pack；`pack.json` **不含** `upstream` 字段；维护者拥有完全修改权 |
| **vendored pack** | 整体来自外部 upstream 的 pack；`pack.json` 含 `upstream` 字段（source + rev）；vendored 内字节不可由 Garage 维护者修改，升级通过手工 `git subtree pull` |
| **vendored 子树** | vendored pack 内除 `pack.json` 与 Garage 添加的 `README.md` 之外的所有文件，构成不可修改边界 |
| **symlink 投影层** | `.agents/skills/<skill-id>/` 这层 git symlink，指向 `packs/<pack-id>/skills/<skill-id>/`，作为宿主扁平化扫描的适配层 |
| **packs inventory** | `AGENTS.md ## Packs Inventory` 子段 + `packs/README.md` 顶层表，集中描述 6 packs 身份的可发现入口 |
| **upstream rev** | vendored pack 在 upstream 仓库中的 commit sha 或 tag；记录在 `pack.json.upstream.rev`，作为升级时的 base reference |
| **dogfood** | Garage 维护者用 Garage 自己的能力开发 Garage 本身；本 cycle 通过 `.agents/skills/` symlink 投影层实现，不需要 `garage init` 安装 |
