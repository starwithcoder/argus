
import redis.asyncio as aioredis
from redis.asyncio.connection import ConnectionPool
from fastapi import Request,Depends
from typing import Annotated, TypeAlias


class RedisManager:
    def __init__(self,host:str,port:int,db:int ):
        self.host: str = host
        self.port: int = port
        self.db: int = db
        self.pool:None|aioredis.ConnectionPool = None
        

    async def connect(self):
        if self.pool is not None:
            return 
        self.pool = aioredis.ConnectionPool(
            host=self.host, 
            port=self.port, 
            db=self.db, 
            decode_responses=True
        )

    async def close(self):
        if self.pool is not None:
            await self.pool.disconnect()
            self.pool = None
        

    @property
    def redis_pool(self) -> aioredis.ConnectionPool:
        if self.pool is None:
            raise RuntimeError("Redis pool is not connected")
        return self.pool


    @staticmethod
    async def get_redis(request:Request) -> aioredis.Redis:
        redis_manager:RedisManager = request.app.state.redis_manager
        redis_pool: ConnectionPool = redis_manager.redis_pool
        return await aioredis.Redis(connection_pool=redis_pool)



AsyncRedisDep: TypeAlias = Annotated[aioredis.Redis,Depends(RedisManager.get_redis)]
