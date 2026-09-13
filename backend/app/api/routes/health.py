from fastapi import APIRouter
from sqlalchemy import text

from backend.app.core.database import AsyncDSBSession
from backend.app.core.redis import AsyncRedisDep
from backend.app.core.milvus import AsyncMilvusDep

router = APIRouter(tags=["health"])



@router.get("/health")
def health(db:AsyncDSBSession):
    print("health check")
    result= db.execute(text("SELECT 1"))
    print(result)
    return {"status": "ok", "database": f"connected: {result}"}



@router.get("/test-redis")
async def test_redis(redis:AsyncRedisDep):
    _=await redis.set("my_key", "Hello from WSL2 Redis!")
    value = await redis.get("my_key")
    return {"message": value}


@router.get("/test-milvus")
async def test_milvus(milvus:AsyncMilvusDep):
    
    databases:list[str] =  milvus.list_databases()
    print("Milvus 连接成功！")
    print("当前数据库列表：", databases)
    return {"status": "ok", "databases": databases}

