from fastapi import APIRouter
from sqlalchemy import text
from backend.app.core.database import DBSessionDep
from backend.app.core.redis import AsyncRedisDep


router = APIRouter(tags=["health"])


@router.get("/health")
def health(db:DBSessionDep):
    print("health check")
    result= db.execute(text("SELECT 1"))
    print(result)
    return {"status": "ok", "database": f"connected: {result}"}



@router.get("/test-redis")
async def test_redis(redis:AsyncRedisDep):
    _=await redis.set("my_key", "Hello from WSL2 Redis!")
    value = await redis.get("my_key")
    return {"message": value}