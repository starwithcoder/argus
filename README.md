# AI Agent Platform

全栈智能体项目骨架：Vue 前端 + FastAPI 后端，使用 MySQL / Redis / Milvus 作为存储与向量检索，并集成 LangChain、LangGraph、OpenAI Agents SDK 构建智能体。

## 技术栈

| 层 | 技术 |
| --- | --- |
| 前端 | Vue 3 + Vite + Pinia + Vue Router + Axios |
| 后端 | FastAPI + Uvicorn + SQLAlchemy + Pydantic |
| 关系库 | MySQL 8.0 |
| 缓存 | Redis 7 |
| 向量库 | Milvus 2.4 (standalone) |
| 智能体 | LangChain / LangGraph / OpenAI Agents SDK |

## 目录结构

```
.
├── backend/            # FastAPI 后端
│   ├── app/
│   │   ├── core/       # 配置与连接(Mysql/Redis/Milvus)
│   │   ├── api/        # 路由
│   │   ├── models/     # ORM 模型
│   │   ├── schemas/    # Pydantic 模型
│   │   ├── services/   # 业务逻辑
│   │   ├── agents/     # 智能体(LangChain/LangGraph/OpenAI)
│   │   └── main.py     # 入口
│   ├── requirements.txt
│   └── .env.example
├── frontend/           # Vue 前端
│   ├── src/
│   ├── package.json
│   └── .env.example
├── docker-compose.yml  # MySQL/Redis/Milvus 基础设施
└── README.md
```

## 快速开始

### 1. 启动基础设施(MySQL/Redis/Milvus)

```bash
docker compose up -d
```

- MySQL:  `127.0.0.1:3306`  (user/appuser, pwd/apppassword, db/appdb)
- Redis:  `127.0.0.1:6379`
- Milvus: `127.0.0.1:19530`
- Attu (Milvus UI): http://localhost:8000

### 2. 启动后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # 填入 OPENAI_API_KEY 等
uvicorn app.main:app --reload --port 8000
```

API 文档: http://localhost:8000/docs

### 3. 启动前端

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

前端默认: http://localhost:5173

## 说明

- 智能体模块 (`backend/app/agents/`) 已搭好 LangChain / LangGraph / OpenAI Agents 的接口与依赖，
  目前为占位实现，填入 `OPENAI_API_KEY` 后即可接入真实模型。
- 数据库建表脚本 / 迁移（Alembic）待后续业务功能确定后补充。
