from fastapi import Depends
from backend.app.core.config import settings 
import redis.asyncio as aioredis
from typing import Annotated 




redis_pool = aioredis.ConnectionPool(
        host=settings.REDIS_HOST, 
        port=settings.REDIS_PORT, 
        db=0, 
        decode_responses=True
    )

async def get_redis() -> aioredis.Redis:
   return await aioredis.Redis(connection_pool=redis_pool)

AsyncRedisDep = Annotated[aioredis.Redis,Depends(get_redis)]