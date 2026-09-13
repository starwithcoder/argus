from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import health
from backend.app.core.config import settings
from contextlib import asynccontextmanager
from backend.app.core.database import engine
from backend.app.core.redis import redis_pool


@asynccontextmanager

async def lifespan(_app: FastAPI): 

    # 1. 初始化 Redis 连接池
    # 2. 初始化 MySQL 异步引擎
   
    yield
   
   # 1. 关闭 Redis 连接池
    await redis_pool.disconnect()
    
    # 2. 关闭 MySQL 异步引擎
    await engine.dispose()  

def create_app():
    app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG,lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix=settings.API_V1_PREFIX)

    return app

app = create_app()

@app.get("/")
def root():
        return {"name": settings.PROJECT_NAME, "status": "ok"}



import uvicorn

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)