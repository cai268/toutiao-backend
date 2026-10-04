# 头条简报后端

基于 FastAPI 的新闻资讯与 AI 问答后端，提供用户认证、新闻浏览、收藏、浏览历史、AI
对话、流式回答和会话记忆等能力，并附带一个可直接访问的静态 Web 页面。

## 功能概览

- 用户注册、登录、Token 认证、资料修改和密码修改。
- 新闻分类、分页列表、详情、浏览量统计和相关新闻推荐。
- 新闻收藏、收藏状态检查，以及浏览历史记录、删除和清空。
- 基于 DeepSeek 的 AI 对话，支持普通响应和 SSE 流式响应。
- AI 路由支持本地知识库 RAG、博查联网搜索、两者结合和直接回答。
- 使用 LangGraph SQLite Checkpointer 持久化多轮会话，支持会话查询与删除。
- MySQL 保存业务数据，Redis 缓存新闻数据，Chroma 和 SQLite 保存向量知识库。
- 内置静态前端，启动后可直接在浏览器中体验主要功能。

## 技术栈

| 类别 | 技术 |
| --- | --- |
| Web 框架 | FastAPI、Uvicorn |
| 数据校验 | Pydantic、pydantic-settings |
| ORM 与数据库 | SQLAlchemy Async、aiomysql、MySQL |
| 缓存 | Redis |
| AI 框架 | LangChain、LangGraph |
| 大模型 | DeepSeek |
| 向量检索 | Chroma、sentence-transformers、BGE |
| 联网搜索 | 博查 Web Search API |
| 会话记忆 | langgraph-checkpoint-sqlite |
| 前端 | 原生 HTML、CSS、JavaScript |

## 项目结构

```text
.
├── main.py                         # FastAPI 入口、路由注册和静态页面挂载
├── config/
│   ├── chat_conf.py                # AI、自建向量库和运行时配置
│   ├── db_conf.py                  # MySQL 异步连接与会话
│   └── redis_conf.py               # Redis 客户端与缓存工具
├── routers/
│   ├── users.py                    # 用户接口
│   ├── news.py                     # 新闻接口
│   ├── favorite.py                 # 收藏接口
│   ├── history.py                  # 浏览历史接口
│   └── AI_chat/
│       ├── chat.py                 # AI 普通对话和流式对话
│       ├── memory.py               # 会话记忆管理
│       └── health.py               # 健康检查
├── schemas/                        # Pydantic 请求与响应模型
├── models/                         # SQLAlchemy ORM 模型
├── crud/                           # 数据库操作
├── cache/                          # 新闻缓存
├── AI_core/
│   ├── pipeline.py                 # 对话、路由和流式输出管线
│   ├── agents.py                   # DeepSeek Agent 创建
│   └── executor.py                 # RAG 与联网搜索执行器
├── AI_models/
│   ├── build_kb.py                 # 从 MySQL 构建本地知识库
│   ├── memory/                     # LangGraph 会话持久化
│   ├── tools/                      # RAG 和联网搜索工具
│   └── vectorstore/                # Chroma 与父文档存储
├── AI_kb/
│   ├── local_doc_db/               # Chroma 与父文档 SQLite 数据库
│   └── SQlite/                     # AI 对话 Checkpointer
├── web/                            # 静态前端页面
├── 数据库原文件/02-数据库sql文件/database.sql
├── API接口规范文档.md
└── pyproject.toml
```

## 运行环境

- Python 3.13 或更高版本。
- MySQL 8.x，默认数据库名为 `news_app`。
- Redis 6.x 或更高版本。Redis 不可用时新闻缓存会降级，但 AI 会话不依赖 Redis。
- 可用且已配置额度的 DeepSeek API Key。
- 如需联网问答，需要博查 API Key。
- 本地 RAG 需要 BGE 向量模型。默认配置路径为
  `D:/AI_tool/embedding_models/BAAI/models/BAAI--bge-base-zh-v1.5/snapshots/master`，
  没有该模型时请通过环境变量修改路径。

推荐使用 [uv](https://docs.astral.sh/uv/) 管理依赖：

```powershell
uv sync
```

## 配置

在项目根目录创建或修改 `.env`：

```dotenv
DEEPSEEK_API_KEY=your_deepseek_api_key
BOCHA_API_KEY=your_bocha_api_key
```

常用可选配置：

```dotenv
APP_NAME=multi-agent-assistant
ENVIRONMENT=development
LOG_LEVEL=INFO
CHAT_MODEL=deepseek-v4-pro
EMBEDDING_MODEL_NAME=D:/path/to/bge-base-zh-v1.5
EMBEDDING_DEVICE=cpu
```

| 变量 | 是否必需 | 说明 |
| --- | --- | --- |
| `DEEPSEEK_API_KEY` | 是 | DeepSeek 对话和问题分析模型密钥 |
| `BOCHA_API_KEY` | 否 | 博查联网搜索密钥；未配置时联网搜索会返回配置提示 |
| `CHAT_MODEL` | 否 | DeepSeek 模型名称，默认 `deepseek-v4-pro` |
| `EMBEDDING_MODEL_NAME` | RAG 必需 | 本地 BGE 模型目录 |
| `EMBEDDING_DEVICE` | 否 | 向量模型运行设备，默认 `cpu` |
| `LOG_LEVEL` | 否 | 日志级别 |

注意：

- MySQL 连接目前直接写在 `config/db_conf.py` 的 `DATABASE_URL` 中，默认值为
  `mysql+aiomysql://root:abcyhlll1129@localhost:3306/news_app?charset=utf8mb4`。
  启动前请按本机实际用户名和密码修改，建议后续改为从环境变量读取。
- `main.py` 直接启动时固定监听 `127.0.0.1:8000`。如需其他地址或端口，请使用 Uvicorn
  命令行参数，或修改 `main.py`。
- 不要提交真实 API Key。如果 `.env` 已被 Git 跟踪，可执行
  `git rm --cached .env` 将其移出版本控制，并确保 `.gitignore` 中包含 `.env`。

## 初始化数据库

1. 启动 MySQL。
2. 导入项目提供的 SQL 文件：

```powershell
Get-Content -Raw -Encoding UTF8 "数据库原文件\02-数据库sql文件\database.sql" |
  mysql --default-character-set=utf8mb4 -u root -p
```

3. 确认数据库 `news_app` 中已创建 `user`、`user_token`、`news_category`、`news`、
   `favorite`、`history`、`related_news` 等数据表。

Redis 默认连接信息：

| 配置 | 默认值 |
| --- | --- |
| 地址 | `localhost` |
| 端口 | `6379` |
| 数据库 | `1` |

## 构建本地知识库

AI 的本地 RAG 数据来自 MySQL 中的新闻表。第一次运行、新闻数据更新后，或更换向量模型后，
需要重建知识库：

```powershell
uv run python -m AI_models.build_kb
```

脚本会重新生成以下文件：

```text
AI_kb/local_doc_db/chroma.sqlite3
AI_kb/local_doc_db/parent_documents.sqlite3
```

仓库中已经包含示例知识库文件。如果当前数据库内容与示例一致，可以直接启动。

## 启动项目

开发模式：

```powershell
uv run python main.py
```

或使用 Uvicorn：

```powershell
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

启动后可访问：

| 地址 | 说明 |
| --- | --- |
| `http://127.0.0.1:8000/` | 静态前端首页 |
| `http://127.0.0.1:8000/docs` | Swagger API 文档 |
| `http://127.0.0.1:8000/redoc` | ReDoc API 文档 |
| `http://127.0.0.1:8000/api/health/health` | 健康检查 |

当前 CORS 白名单仅包含 `http://localhost:6000` 和 `http://127.0.0.1:6000`。如果使用其他
前端地址，请修改 `main.py` 中的 `allow_origins`。

## 认证与响应

除注册、登录、新闻查询和健康检查外，其余用户相关接口都需要认证：

```http
Authorization: Bearer <token>
```

Token 为用户登录或注册后返回的 UUID，有效期 5 小时。业务接口通常返回：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

发生业务或系统异常时，响应中的 `code` 为对应的 HTTP 状态码，错误信息位于 `message`。

## 接口总览

完整示例可参考 `API接口规范文档.md`。以下路由以当前源码为准：

### 用户

| 方法 | 路径 | 认证 | 说明 |
| --- | --- | --- | --- |
| `POST` | `/api/users/register` | 否 | 注册，Body 为 `username`、`password` |
| `POST` | `/api/users/login` | 否 | 登录 |
| `GET` | `/api/users/info` | 是 | 获取当前用户信息 |
| `PUT` | `/api/users/update` | 是 | 更新昵称、头像、性别和简介 |
| `PUT` | `/api/users/password` | 是 | 修改密码 |

修改密码请求示例：

```json
{
  "old_password": "old-password",
  "new_password": "new-password",
  "new_password_confirm": "new-password"
}
```

### 新闻

| 方法 | 路径 | 查询参数 | 说明 |
| --- | --- | --- | --- |
| `GET` | `/api/news/categories` | `skip`、`limit` | 获取新闻分类 |
| `GET` | `/api/news/list` | `category_id`、`page`、`page_size` | 分页获取新闻列表 |
| `GET` | `/api/news/detail` | `ID` | 获取新闻详情并增加浏览量 |

示例：

```http
GET /api/news/list?category_id=1&page=1&page_size=10
GET /api/news/detail?ID=1
```

### 收藏

注意当前源码使用的路由前缀是 `/api/favority`。

| 方法 | 路径 | 参数 | 说明 |
| --- | --- | --- | --- |
| `GET` | `/api/favority/check` | `news_id` | 检查收藏状态 |
| `POST` | `/api/favority/add` | `news_id` | 添加收藏 |
| `POST` | `/api/favority/remove` | `news_id` | 取消收藏 |
| `GET` | `/api/favority/list` | `page`、`page_size` | 收藏列表 |
| `DELETE` | `/api/favority/clear` | 无 | 清空收藏 |

添加或取消收藏的请求体：

```json
{
  "news_id": 1
}
```

### 浏览历史

| 方法 | 路径 | 参数 | 说明 |
| --- | --- | --- | --- |
| `POST` | `/api/history/add` | `newsId` | 新增或刷新浏览记录 |
| `GET` | `/api/history/list` | `page`、`page_size` | 浏览历史列表 |
| `DELETE` | `/api/history/delete/{history_id}` | 路径参数 | 删除单条历史 |
| `DELETE` | `/api/history/clear` | 无 | 清空历史 |

新增浏览记录的请求体：

```json
{
  "newsId": 1
}
```

### AI 对话与会话记忆

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `POST` | `/api/chat` | 普通 AI 回答 |
| `POST` | `/api/chat/stream` | SSE 流式 AI 回答 |
| `GET` | `/api/memory` | 获取当前用户的会话列表 |
| `GET` | `/api/memory/{dialog_id}/messages` | 获取指定会话消息 |
| `DELETE` | `/api/memory/{dialog_id}` | 删除指定会话 |

普通对话请求：

```json
{
  "message": "介绍一下今天的科技新闻",
  "dialog_id": "demo-dialog",
  "mode": "auto"
}
```

`mode` 支持以下取值：

| 模式 | 说明 |
| --- | --- |
| `auto` | 由分析 Agent 自动路由 |
| `rag` | 仅查询本地向量知识库 |
| `web` | 仅使用博查联网搜索 |
| `both` | 同时查询本地知识库和联网搜索 |
| `direct` | 不检索，由模型直接回答 |

流式接口返回 `text/event-stream`，事件类型包括：

| 事件 | 说明 |
| --- | --- |
| `status` | 当前处理状态 |
| `meta` | 路由、检索问题和会话元信息 |
| `token` | 增量回答内容 |
| `done` | 完整回答和最终元信息 |
| `error` | 处理失败信息 |

## AI 处理流程

```text
用户问题
  -> ChatPipeline
  -> Analyzer Agent（auto 模式）
  -> Executor
       -> RAG：Chroma 子块检索 -> 父文档 SQLite 回填
       -> Web：博查搜索
       -> Both：组合两类检索结果
       -> Direct：跳过检索
  -> DeepSeek Output Agent
  -> LangGraph Checkpointer 保存会话
  -> 普通 JSON 或 SSE 流式响应
```

会话 ID 按 `user:{user_id}:dialog:{dialog_id}` 隔离，因此不同用户即使使用相同
`dialog_id`，也不会共享会话记录。

## 常见问题

### 数据库连接失败

检查 MySQL 是否启动、数据库是否已导入，以及 `config/db_conf.py` 中的用户名、密码、端口
是否正确。当前连接地址不是从 `.env` 读取。

### Redis 连接失败

检查 `localhost:6379` 和 DB `1` 是否可用。缓存读取异常通常不会阻断业务，但会降低新闻
查询性能。

### 提示知识库不存在

确认 `AI_kb/local_doc_db/chroma.sqlite3` 和
`AI_kb/local_doc_db/parent_documents.sqlite3` 存在；否则执行：

```powershell
uv run python -m AI_models.build_kb
```

### 向量模型加载失败

确认 `EMBEDDING_MODEL_NAME` 指向已下载的 BGE 模型目录。Windows 路径建议使用正斜杠 `/`
或双反斜杠 `\\`。

### AI 返回配置或服务错误

确认 `.env` 中存在有效的 `DEEPSEEK_API_KEY`。联网模式的搜索失败通常与
`BOCHA_API_KEY`、网络连接或额度有关。

### 接口参数与旧文档不一致

项目早期文档中的收藏前缀、部分查询参数和请求字段可能与当前实现不一致。开发时优先查看
`/docs` 生成的 OpenAPI 文档，或直接参考本文档的接口总览。

## 开发说明

- 新增业务接口时，按 `router -> schema -> crud -> model` 分层添加。
- AI 功能集中在 `AI_core` 和 `AI_models`，业务路由只负责认证、依赖注入和响应封装。
- 当前仓库没有自动化测试；修改数据库或 AI 链路后，建议至少验证
  `/api/health/health`、用户认证、新闻查询、RAG 对话和流式对话。
