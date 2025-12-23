# 数据库架构设计建议

## 📊 需求分析

### 当前功能需求
1. **视频生成历史记录**
   - 保存每次生成的视频信息
   - 提示词、首尾帧、任务ID、视频URL、生成时间等
   - 支持查询、筛选、下载历史视频

2. **知识库功能**（预留）
   - 剧本上传和管理
   - 人物一致性匹配
   - 场景一致性
   - 向量化存储（已有 Chroma 向量库）

3. **资产管理**（已有）
   - 图片资产上传
   - 分类管理
   - 人物-视图类型匹配

### 现有数据库情况
- ✅ **Chroma 向量数据库**：用于 RAG 视频关键帧向量存储
- ⚠️ **PostgreSQL**：README 中提到但未实际使用
- ⚠️ **知识库**：功能预留，未实现

---

## 🎯 架构建议：统一数据库 + 模块化设计

### 推荐方案：PostgreSQL 作为主数据库

**理由：**
1. ✅ **统一管理**：所有结构化数据在一个数据库中，便于维护和备份
2. ✅ **数据一致性**：事务支持，保证数据完整性
3. ✅ **查询效率**：SQL 查询性能优秀，支持复杂查询
4. ✅ **扩展性强**：易于添加新功能模块
5. ✅ **成熟稳定**：PostgreSQL 是生产级数据库
6. ✅ **成本可控**：可以使用免费的云数据库（如 Render、Supabase）

**架构设计：**

```
┌─────────────────────────────────────────┐
│         PostgreSQL 主数据库              │
├─────────────────────────────────────────┤
│  📹 视频生成历史表 (video_generations)   │
│  📦 资产管理表 (assets)                 │
│  📚 知识库表 (knowledge_base)           │
│  👤 用户表 (users) - 可选               │
│  🔗 关联表 (relations)                  │
└─────────────────────────────────────────┘
           │
           │ 配合使用
           ▼
┌─────────────────────────────────────────┐
│      Chroma 向量数据库（专用）           │
├─────────────────────────────────────────┤
│  🎬 视频关键帧向量 (video_frames)        │
│  📝 剧本向量 (scripts) - 未来扩展        │
└─────────────────────────────────────────┘
```

---

## 📋 数据库表设计

### 1. 视频生成历史表 (`video_generations`)

```sql
CREATE TABLE video_generations (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(255) UNIQUE NOT NULL,  -- 即梦 API 返回的任务ID
    prompt TEXT NOT NULL,                  -- 提示词
    negative_prompt TEXT,                  -- 负面提示词
    duration INTEGER NOT NULL,             -- 视频时长（秒）
    fps INTEGER DEFAULT 24,                -- 帧率
    width INTEGER DEFAULT 720,             -- 宽度
    height INTEGER DEFAULT 720,             -- 高度
    seed INTEGER,                          -- 随机种子
    first_frame_url TEXT,                  -- 首帧图片URL（base64或URL）
    last_frame_url TEXT,                   -- 尾帧图片URL（base64或URL）
    video_url TEXT,                        -- 生成的视频URL
    status VARCHAR(50) NOT NULL,         -- pending/processing/completed/failed
    error_message TEXT,                     -- 错误信息（如果有）
    created_at TIMESTAMP DEFAULT NOW(),    -- 创建时间
    completed_at TIMESTAMP,               -- 完成时间
    user_id INTEGER,                       -- 用户ID（如果有多用户）
    metadata JSONB                         -- 扩展元数据（JSON格式）
);

-- 索引
CREATE INDEX idx_video_generations_task_id ON video_generations(task_id);
CREATE INDEX idx_video_generations_status ON video_generations(status);
CREATE INDEX idx_video_generations_created_at ON video_generations(created_at DESC);
CREATE INDEX idx_video_generations_user_id ON video_generations(user_id);
```

### 2. 资产管理表 (`assets`)

```sql
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,       -- 文件名
    file_path TEXT NOT NULL,              -- 文件路径
    file_size BIGINT,                     -- 文件大小（字节）
    mime_type VARCHAR(100),              -- MIME类型
    character_name VARCHAR(100),          -- 人物名称
    view_type VARCHAR(50),                -- 视图类型（正视图、侧视图等）
    category VARCHAR(50),                -- 分类
    tags TEXT[],                          -- 标签数组
    uploaded_at TIMESTAMP DEFAULT NOW(),  -- 上传时间
    user_id INTEGER,                       -- 用户ID
    metadata JSONB                         -- 扩展元数据
);

-- 索引
CREATE INDEX idx_assets_character_name ON assets(character_name);
CREATE INDEX idx_assets_view_type ON assets(view_type);
CREATE INDEX idx_assets_category ON assets(category);
CREATE INDEX idx_assets_user_id ON assets(user_id);
```

### 3. 知识库表 (`knowledge_base`)

```sql
CREATE TABLE knowledge_base (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,         -- 剧本/文档标题
    content TEXT NOT NULL,                -- 剧本内容
    file_path TEXT,                       -- 原文件路径
    file_type VARCHAR(50),               -- 文件类型（txt/md/docx）
    characters TEXT[],                    -- 提取的人物列表
    scenes JSONB,                         -- 场景信息（JSON格式）
    vector_id VARCHAR(255),              -- 向量数据库中的ID（关联 Chroma）
    created_at TIMESTAMP DEFAULT NOW(),  -- 创建时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间
    user_id INTEGER,                      -- 用户ID
    metadata JSONB                        -- 扩展元数据
);

-- 索引
CREATE INDEX idx_knowledge_base_title ON knowledge_base(title);
CREATE INDEX idx_knowledge_base_characters ON knowledge_base USING GIN(characters);
CREATE INDEX idx_knowledge_base_vector_id ON knowledge_base(vector_id);
```

### 4. 用户表 (`users`) - 可选

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),           -- 如果使用密码登录
    api_key VARCHAR(255) UNIQUE,         -- API密钥（用于API调用）
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- 索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_api_key ON users(api_key);
```

---

## 🔄 与现有系统的集成

### Chroma 向量数据库（保持不变）

- **用途**：专门用于向量检索
- **存储内容**：
  - 视频关键帧向量（已有）
  - 未来：剧本向量、场景向量
- **优势**：向量检索性能优秀，适合 RAG 场景

### PostgreSQL（新增）

- **用途**：结构化数据存储
- **存储内容**：
  - 视频生成历史
  - 资产管理
  - 知识库元数据
- **优势**：事务支持、复杂查询、数据一致性

---

## 🚀 实施步骤

### 阶段 1: 基础数据库搭建（当前）

1. **选择数据库服务**
   - 推荐：Render PostgreSQL（免费）、Supabase（免费）、Railway（免费额度）
   
2. **创建数据库表**
   - 先实现 `video_generations` 表
   - 实现基础的 CRUD 操作

3. **集成到后端 API**
   - 修改 `generate_video` 接口，保存生成记录
   - 添加查询历史记录的接口

### 阶段 2: 历史记录功能（优先）

1. **保存生成记录**
   - 生成视频时自动保存到数据库
   - 更新视频状态（pending → processing → completed）

2. **查询历史记录**
   - 列表查询（分页、筛选）
   - 详情查询
   - 下载历史视频

3. **前端展示**
   - 在"资产管理"页面添加"历史记录"标签
   - 显示生成历史列表
   - 支持筛选和搜索

### 阶段 3: 知识库功能（后续）

1. **剧本管理**
   - 上传剧本文件
   - 提取人物和场景信息
   - 存储到 PostgreSQL

2. **向量化**
   - 将剧本内容向量化
   - 存储到 Chroma 向量库
   - 在 PostgreSQL 中保存关联关系

---

## 💡 为什么选择统一数据库？

### ✅ 优势

1. **便于管理**
   - 一个数据库连接，统一备份和恢复
   - 统一的数据库管理工具

2. **数据一致性**
   - 事务支持，保证数据完整性
   - 外键约束，保证关联关系

3. **查询效率**
   - SQL JOIN 查询，关联数据查询方便
   - 索引优化，查询性能好

4. **扩展性强**
   - 添加新功能只需添加新表
   - 不影响现有功能

5. **成本可控**
   - 免费云数据库足够使用
   - 按需扩展

### ⚠️ 注意事项

1. **向量数据仍用 Chroma**
   - PostgreSQL 的向量扩展（pgvector）也可以，但 Chroma 更专业
   - 保持现有 RAG 功能不变

2. **数据分离**
   - 结构化数据 → PostgreSQL
   - 向量数据 → Chroma
   - 文件存储 → 对象存储（如 S3、OSS）或本地文件系统

---

## 📝 推荐的技术栈

### 数据库
- **PostgreSQL**：主数据库（结构化数据）
- **Chroma**：向量数据库（向量检索）

### ORM/数据库工具
- **SQLAlchemy**：Python ORM，便于数据库操作
- **Alembic**：数据库迁移工具

### 云服务选择
1. **Render PostgreSQL**（推荐）
   - 免费额度：90天免费试用
   - 简单易用，与 Render 后端部署集成方便

2. **Supabase**（推荐）
   - 免费额度：500MB 数据库
   - 提供 REST API 和实时功能

3. **Railway**
   - 免费额度：$5/月
   - 简单易用

---

## 🎯 总结

**推荐方案：统一 PostgreSQL 数据库 + Chroma 向量库**

- ✅ 统一管理，便于维护
- ✅ 数据一致性强
- ✅ 查询效率高
- ✅ 扩展性强
- ✅ 成本可控

**实施优先级：**
1. 🔥 **视频生成历史记录**（立即实施）
2. 📦 **资产管理优化**（已有基础，可增强）
3. 📚 **知识库功能**（后续开发）

---

## ❓ 需要确认的问题

1. **是否需要多用户支持？**
   - 如果只是单用户，可以简化用户表设计

2. **视频文件存储方式？**
   - 本地文件系统？
   - 对象存储（S3、OSS）？
   - 只保存 URL？

3. **数据库服务选择？**
   - Render PostgreSQL？
   - Supabase？
   - 其他？

请告诉我你的选择，我可以开始实施！

