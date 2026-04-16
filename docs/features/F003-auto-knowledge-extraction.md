# F003: 自动知识提取

- 状态: 草稿
- 主题: 让 Garage 从执行产出中自动提取和积累知识
- 日期: 2026-04-17
- 关联: F001（Phase 1 引擎）、F002（Garage Live — CLI + 真实执行）
- 成长策略: Stage 2 "记忆体" 的核心能力

## 1. 背景与问题陈述

F002 让 Garage OS 引擎真正跑起来了：

```
garage run → 创建 Session → 调用 Claude Code → 产出 output → 记录 Experience
```

但存在一个关键缺口：**知识积累仍是手动的。**

具体问题：

1. **Experience 有数据，但无知识**：每次 skill 执行后，系统自动记录了结构化的 ExperienceRecord（task_type、skill_ids、duration、outcome 等），但这些都是"元数据"，不是可复用的知识
2. **KnowledgeIntegration.extract_from_session() 需要人工准备**：调用方需要自己把 experience_data 组装好（包括 knowledge_type、decision_topic、pattern_description 等），系统不做任何提取
3. **Claude Code 的输出未被利用**：`garage run` 捕获了 Claude Code 的完整输出（可能包含决策理由、技术方案、踩坑记录），但这些输出直接丢弃了
4. **知识库为空**：.garage/knowledge/ 下没有真实数据，知识查询无内容可返回

growth-strategy.md 定义了 Stage 2 "记忆体" 的核心能力：

> - 知识库自动积累（技术决策、问题解法、最佳实践）
> - 经验按场景检索（遇到类似问题自动推荐历史解法）
> - 会话上下文持续化（跨会话保持项目状态）

F003 是实现 Stage 2 的第一步：**让系统从执行产出中自动提取知识。**

## 2. 目标与成功标准

### 2.1 核心目标

在 skill 执行完成后，自动从 Claude Code 的输出中提取有价值的知识条目，写入知识库。

```
garage run → 执行 skill → 捕获 output → 分析 output →
  → 提取 KnowledgeEntry（decision / pattern / solution）→ 写入知识库
  → 丰富 ExperienceRecord（补充 lessons_learned、key_patterns）
```

### 2.2 成功标准

1. **自动提取**：skill 执行后，系统能自动产出至少一个 KnowledgeEntry，不需要用户手动构造
2. **质量可接受**：提取的知识条目 topic 清晰、content 有实质内容（不是空壳）
3. **类型正确**：能区分 decision（决策）、pattern（模式）、solution（解法）三种类型
4. **Experience 丰富**：key_patterns 和 lessons_learned 从输出中自动填充
5. **可查询**：`garage knowledge search` 能找到自动提取的知识
6. **可重复**：多次执行不会重复插入相同知识

### 2.3 非目标

- 不做 LLM 驱动的智能提取（调用另一个 LLM 来分析输出）— 那是后续优化
- 不做跨会话的上下文持续化 — 那是 Stage 2 后续
- 不做知识的自动去重和合并 — 先积累，后整理
- 不改 F001/F002 已有的模块接口 — 只扩展不破坏

## 3. 用户角色与关键场景

### 3.1 用户角色

- **Solo Creator**：执行 skill 后，Garage 自动记住有价值的知识

### 3.2 关键场景

1. **执行后自动提取**：`garage run some-skill` 执行完毕，系统自动分析输出，提取 0-N 条知识
2. **查看新知识**：`garage knowledge list` 能看到最近自动提取的知识条目
3. **搜索相关知识**：下次执行类似任务时，`garage knowledge search` 能找到历史经验

## 4. 范围

### 4.1 包含

| 功能 | 描述 |
|------|------|
| 知识提取器（KnowledgeExtractor） | 分析 skill 执行输出，提取 KnowledgeEntry |
| 输出结构化协议 | 定义 skill 输出中的知识标记格式 |
| 自动提取流程 | 集成到 `garage run` 的 session 生命周期 |
| Experience 丰富 | 从输出中提取 key_patterns 和 lessons_learned |
| CLI 展示 | `garage knowledge` 展示提取来源（source_session） |

### 4.2 不包含

- LLM 驱动的智能分析
- 跨会话上下文
- 知识评分和质量过滤
- 知识自动去重
- Web UI

## 5. 功能需求

### FR-301: 知识提取器（KnowledgeExtractor）

- **FR-301a**: 新增 `KnowledgeExtractor` 类，负责从 skill 执行输出中提取结构化知识
- **FR-301b**: 采用**规则 + 标记协议**方式提取：skill 输出中可以用约定标记（如 `<!-- GARAGE:DECISION -->`）声明知识类型，提取器识别标记并提取
- **FR-301c**: 无标记时，使用启发式规则从输出中提取（识别 "decision:" / "pattern:" / "solution:" 等关键词模式）
- **FR-301d**: 提取结果为 `List[KnowledgeEntry]`，每条包含 type、topic、content、tags

### FR-302: 输出标记协议

- **FR-302a**: 定义 skill 输出中的知识标记格式：

```
<!-- GARAGE:KNOWLEDGE:decision -->
topic: <主题>
tags: <标签逗号分隔>
<知识正文，markdown 格式>
<!-- /GARAGE:KNOWLEDGE -->
```

- **FR-302b**: 支持三种类型标记：`decision`、`pattern`、`solution`
- **FR-302c**: 一个输出中可以包含多个知识块
- **FR-302d**: 标记是可选的（skill 不标记也能工作，只是不会自动提取）

### FR-303: Experience 丰富

- **FR-303a**: 从 skill 输出中提取 `key_patterns`（关键技术模式）
- **FR-303b**: 从 skill 输出中提取 `lessons_learned`（经验教训）
- **FR-303c**: 提取规则：识别 `## Lessons` / `## Key Patterns` / `## Takeaways` 等 section
- **FR-303d**: 丰富后的数据更新到已有的 ExperienceRecord

### FR-304: 集成到 garage run

- **FR-304a**: `garage run` 执行完 skill 后，自动调用 KnowledgeExtractor
- **FR-304b**: 提取的知识通过 KnowledgeStore 写入知识库
- **FR-304c**: ExperienceRecord 通过 ExperienceIndex 更新（补充 key_patterns、lessons_learned）
- **FR-304d**: 在终端输出中显示提取摘要（如 "Extracted 2 knowledge entries: 1 decision, 1 pattern"）

### FR-305: CLI 知识管理增强

- **FR-305a**: `garage knowledge list` 显示知识的来源 session
- **FR-305b**: `garage knowledge search` 支持按来源 session 过滤
- **FR-305c**: `garage knowledge show <id>` 显示完整知识条目（含来源信息）

## 6. 非功能需求

| NFR | 要求 | 验证方式 |
|-----|------|----------|
| 性能 | 知识提取耗时 < 100ms（纯文本解析，无 LLM 调用） | 基准测试 |
| 可靠性 | 提取失败不阻塞主流程（skill 执行结果不受影响） | 错误注入测试 |
| 兼容性 | 不破坏 F001+F002 已有的 343 个测试 | 全量回归 |
| 可扩展 | KnowledgeExtractor 可被替换为 LLM 驱动的实现 | 接口抽象 |

## 7. 约束

- 沿用 F001/F002 的技术栈（Python 3.11+, uv）
- 知识提取采用规则解析，不调用外部 LLM
- 不引入新的外部依赖（仅使用 Python 标准库）
- 提取器设计为可替换组件（Strategy 模式），方便后续升级

## 8. 依赖

- F001 Phase 1 所有模块（已完成）
- F002 Garage Live（已完成）

## 9. 技术方案概述

### 9.1 KnowledgeExtractor 接口

```python
class KnowledgeExtractor(Protocol):
    """从 skill 执行输出中提取知识的协议。"""

    def extract(self, output: str, context: ExtractionContext) -> ExtractionResult:
        """分析 skill 输出，提取知识和经验。

        Args:
            output: skill 执行的完整输出文本
            context: 提取上下文（session_id, skill_name, domain 等）

        Returns:
            ExtractionResult 包含提取的知识条目和经验补充数据
        """
        ...
```

### 9.2 默认实现：RuleBasedExtractor

采用两阶段提取：

1. **标记提取**：扫描 `<!-- GARAGE:KNOWLEDGE:xxx -->` 标记，精确提取
2. **启发式提取**：识别常见 section 标题（`## Decision`、`## Pattern`、`## Solution`）和关键词模式

### 9.3 数据流

```
Claude Code output
       │
       ▼
KnowledgeExtractor.extract(output, context)
       │
       ├──→ List[KnowledgeEntry]  ──→ KnowledgeStore.store()
       │
       └──→ ExperienceEnrichment   ──→ ExperienceIndex.update()
```

### 9.4 新增文件

- `src/garage_os/knowledge/extractor.py` — KnowledgeExtractor 协议 + RuleBasedExtractor 实现
- `src/garage_os/knowledge/extractor_types.py` — ExtractionContext、ExtractionResult 等类型
- `tests/knowledge/test_extractor.py` — 提取器单元测试

## 10. 开放问题

1. 知识 ID 生成策略：用 uuid 还是基于内容的 hash（hash 可以天然去重）？
2. 提取的知识默认 status 是 `active` 还是 `draft`（需要用户确认后才激活）？
3. 是否需要 `garage knowledge confirm` 命令让用户审核自动提取的知识？
4. 启发式提取的精度可能不高，是否只做标记提取，启发式留给后续？
