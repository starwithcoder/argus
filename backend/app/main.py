
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import health
from backend.app.core.config import settings
from contextlib import asynccontextmanager

from backend.app.core.database import DatabaseManager
from backend.app.core.redis import RedisManager
from backend.app.core.milvus import MilvusManager
from backend.app.core.logging import setup_logging, get_logger
from backend.app.api.middleware.logging_middleware import RequestLoggingMiddleware

@asynccontextmanager

async def lifespan(app: FastAPI): 

    # 0. 初始化日志
    setup_logging()
    logger = get_logger(__name__)
    logger.info("Application startup ...")

    # 1. 初始化 Redis 连接池
    redis_manager = RedisManager(
        settings.REDIS_HOST, 
        settings.REDIS_PORT, 
        settings.REDIS_DB
        )
    await redis_manager.connect()
    app.state.redis_manager = redis_manager

    # 2. 初始化 MySQL 异步引擎
    database_manager = DatabaseManager(
        settings.async_database_url
        )
    await database_manager.connect()
    app.state.database_manager = database_manager

    #3. 初始化 Milvus 客户端
    milvus_manager = MilvusManager(settings.milvus_uri)
    await milvus_manager.connect()
    app.state.milvus_manager = milvus_manager
    yield

    logger.info("Application shutdown ...")

    # 1. 关闭 Redis 连接池
    await redis_manager.close()
    
    # 2. 关闭 MySQL 异步引擎
    await database_manager.close() 

    # 3. 关闭 Milvus 客户端
    await milvus_manager.close()

def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(RequestLoggingMiddleware)

    app.include_router(health.router, prefix=settings.API_V1_PREFIX)

    return app

app = create_app()




@app.get("/")
def root():
        return {"name": settings.PROJECT_NAME, "status": "ok"}



import uvicorn

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)