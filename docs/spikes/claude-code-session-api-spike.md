# Claude Code Session API 技术验证报告

**Spike ID**: ASM-EXT-001
**执行日期**: 2026-04-15
**执行者**: T1 技术验证 Spike
**验证假设**: Host Adapter 能读取 Claude Code 的 session 状态、写入检查点、恢复到指定状态

---

## 执行摘要

**结论**: ❌ **ASM-EXT-001 不成立**

Claude Code **不支持**原生的 session 状态管理 API。外部程序无法直接读取或恢复 Claude Code 的内部 session 状态。但**回退方案可行**：通过 artifact-first 文件系统方案可以实现状态持久化和传递。

---

## 验证结果

### 1. 能力探测：Claude Code 是否暴露 API 让外部程序读取当前 session 的上下文信息？

**结论**: ❌ **不支持**

**详细分析**:
- Claude Code 的 session 状态（conversation history、workspace path、当前上下文）存储在内存中
- **没有公开的 HTTP API、gRPC 接口或 SDK** 供外部程序访问
- 外部程序无法直接获取：
  - 当前对话历史
  - 工具调用的执行状态
  - 用户的权限设置
  - session 的内部状态机

**技术细节**:
```
Session 状态范围：
- 对话历史：内存存储，自动压缩
- 用户权限：运行时配置，不对外暴露
- 工具执行状态：内部异步处理，外部不可见
- 上下文窗口：动态管理，外部无法查询
```

---

### 2. 写入检查点：Claude Code 是否支持在 session 中间写入持久化状态？

**结论**: ⚠️ **部分支持**（通过文件系统）

**详细分析**:
- **没有原生的"checkpoint" API** 或状态快照机制
- **支持通过文件写入持久化状态**：
  - 使用 `Write` 工具写入任意文件到文件系统
  - Memory system（`MEMORY.md` 和 memory files）会在新 session 中自动加载
  - 文件写入会持久化到磁盘，不受 session 生命周期限制

**可用的持久化机制**:
```python
# 示例：通过文件系统写入状态
{
  "文件系统": "workspace 任意路径",
  "Memory System": "/.claude/projects/{project}/memory/",
  "自动加载": "MEMORY.md 在新 session 自动加载",
  "手动加载": "通过 Read 工具读取任意文件"
}
```

**限制**:
- 需要显式调用 Write 工具，无自动 checkpoint
- 状态序列化需要手动处理
- 不支持内存状态的直接快照

---

### 3. 恢复机制：新的 Claude Code session 能否读取上一 session 写入的状态？

**结论**: ⚠️ **部分支持**（仅通过文件系统）

**详细分析**:
- **不支持直接恢复 session 状态**：
  - 新 session 无法继承上一 session 的 conversation history
  - 无法恢复工具调用栈、用户权限等运行时状态
  - 内存状态完全隔离

- **支持通过文件系统传递状态**：
  - 新 session 可以读取上一 session 写入的文件
  - MEMORY.md 和 memory files 会在新 session 启动时自动加载
  - 可以通过状态文件（JSON、YAML 等）手动重建状态

**状态传递能力矩阵**:
| 状态类型 | 直接恢复 | 文件系统传递 |
|---------|---------|------------|
| 对话历史 | ❌ | ❌ |
| 用户变量 | ❌ | ✅ (手动序列化) |
| 检查点 | ❌ | ✅ (手动实现) |
| Artifact | ❌ | ✅ (直接读取) |
| Memory | ✅ | ✅ (自动加载) |

---

### 4. 限制识别：Claude Code 有哪些操作限制？

**结论**: ✅ **存在多个关键限制**

**详细分析**:

| 限制类别 | 具体限制 | 影响评估 |
|---------|---------|---------|
| **上下文窗口** | 会话消息会被自动压缩 | 无法通过外部 API 查询当前窗口使用率 |
| **Session 隔离** | 不同 session 完全隔离 | 无法跨 session 共享内存状态 |
| **工具权限** | 需要用户显式批准 | Host Adapter 无法绕过权限系统 |
| **API 暴露** | 无公开 API | 外部程序只能通过文件系统交互 |
| **并发控制** | 单 session 单线程执行 | 无法并行执行多个工具调用 |
| **超时机制** | 工具调用有 2-10 分钟超时 | 长时间运行的任务需要后台模式 |

**关键技术限制**:
```
1. 无进程间通信 (IPC) 机制
2. 无 WebSocket / Server-Sent Events 接口
3. 无状态查询 API（无法获取当前 session 信息）
4. 工具调用必须由 Claude Code 发起，无法反向调用
```

---

### 5. 回退策略：如果不支持原生 session 管理，纯 artifact-first 文件方案是否可行？

**结论**: ✅ **完全可行**

**详细分析**:
- ✅ **文件系统完全可用**：`Read`/`Write` 工具可操作任意路径
- ✅ **Memory System 自动加载**：MEMORY.md 在新 session 自动加载
- ✅ **状态序列化可控**：可以用 JSON/YAML 存储任意结构化状态
- ✅ **检查点可实现**：通过定期写入状态文件实现 checkpoint
- ✅ **状态恢复可编程**：新 session 读取状态文件并重建

**Artifact-First 方案架构**:
```
┌─────────────────┐
│  Claude Code    │
│  Session N      │
└────────┬────────┘
         │ Read/Write
         ▼
┌─────────────────────────────┐
│  File System (Workspace)    │
│  ├── .checkpoints/          │
│  │   ├── checkpoint-001.json │
│  │   └── checkpoint-002.json │
│  ├── .state/                │
│  │   └── current-state.json │
│  └── MEMORY.md (auto-load)  │
└─────────────────────────────┘
         ▲
         │ Read
         │
┌────────┴────────┐
│  Claude Code    │
│  Session N+1    │
└─────────────────┘
```

**实现要点**:
1. **状态序列化**：将需要持久化的状态转换为 JSON/YAML
2. **检查点策略**：定期写入 `.checkpoints/` 目录
3. **恢复机制**：新 session 读取最新检查点文件
4. **内存管理**：使用 MEMORY.md 存储跨 session 的元信息
5. **并发控制**：使用文件锁避免竞态条件

**示例状态文件格式**:
```json
{
  "version": "1.0",
  "timestamp": "2026-04-15T10:30:00Z",
  "checkpoint_id": "cp-001",
  "state": {
    "conversation_context": {...},
    "user_variables": {...},
    "task_stack": [...],
    "artifacts": [...]
  }
}
```

---

## 结论与建议

### 主结论

❌ **ASM-EXT-001 假设不成立**

Claude Code **不支持**原生的 session 状态管理 API。外部 Host Adapter 无法：
- 直接读取当前 session 的状态
- 写入或恢复内存中的检查点
- 跨 session 共享运行时状态

### 回退方案

✅ **推荐使用 Artifact-First 文件系统方案**

**实施方案**:
1. **状态持久化层**：
   - 使用 `.garage/state/` 存储运行时状态
   - 使用 `.garage/checkpoints/` 存储检查点
   - 使用 `MEMORY.md` 存储元信息

2. **Host Adapter 设计调整**：
   - 不再依赖 Claude Code 的内部 API
   - 通过文件系统与 Claude Code 交互
   - 实现独立的状态管理服务

3. **检查点机制**：
   - Claude Code 定期写入状态文件
   - Host Adapter 监控文件变化
   - 新 session 读取最新状态文件恢复

### 风险评估

| 风险项 | 严重程度 | 缓解措施 |
|-------|---------|---------|
| 状态同步延迟 | 中 | 使用文件系统事件监听（inotify） |
| 并发冲突 | 中 | 实现文件锁机制 |
| 状态序列化开销 | 低 | 使用高效的二进制格式 |
| 磁盘空间 | 低 | 实现检查点轮转清理 |

### 后续行动

1. ✅ **接受回退方案**：进入 T2 阶段，设计基于文件系统的 Host Adapter
2. 📝 **更新设计文档**：标记 ASM-EXT-001 为"不成立"，记录回退方案
3. 🔧 **实现状态管理模块**：开发 artifact-first 的状态持久化层
4. 🧪 **编写集成测试**：验证跨 session 状态传递的可靠性

---

## 附录

### A. Claude Code 工具能力清单

| 工具名称 | 能力 | 是否可用于状态管理 |
|---------|-----|------------------|
| Read | 读取任意文件 | ✅ 状态恢复 |
| Write | 写入任意文件 | ✅ 状态持久化 |
| Edit | 编辑已有文件 | ✅ 状态更新 |
| Bash | 执行 shell 命令 | ⚠️ 可用但需权限 |
| Glob | 文件模式匹配 | ✅ 状态发现 |
| Grep | 内容搜索 | ✅ 状态查询 |

### B. Memory System 机制

```
Memory System 结构：
/.claude/projects/{project}/memory/
├── MEMORY.md          # 索引文件（自动加载）
├── user_*.md          # 用户信息
├── feedback_*.md      # 反馈记忆
├── project_*.md       # 项目信息
└── reference_*.md     # 外部引用

加载机制：
- Session 启动时自动加载 MEMORY.md
- MEMORY.md 引用的其他 memory 文件按需加载
- 超过 200 行后的内容会被截断
```

---

**报告结束**
