from pymilvus import MilvusClient  
from backend.app.core.config import settings

from fastapi import Request,Depends
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
from typing import Annotated
from backend.app.core.database import DatabaseManager




def get_milvus_client(url:str) -> MilvusClient:
   
    return MilvusClient(uri=url)



class MilvusManager():
    
    def __init__(self,url:str) -> None:
        self._url:str = url
        self._client:MilvusClient | None = None 

    async def connect(self):
        if self._client is not None:
            return 
        
        self._client = MilvusClient(uri=self._url)

    async def is_connected(self):
        if self._client is None:
            return False
        return True

    async def close(self):
        if self._client is not None:
            self._client.close()
            self._client = None
    
    @property
    def client(self) -> MilvusClient:
        if self._client is None:
            raise RuntimeError("Milvus is not connected")
        return self._client

    @staticmethod
    async def get_milvus(request:Request):
        try:
            milvus_manager:MilvusManager = request.app.state.milvus_manager
            milvus_client:MilvusClient = milvus_manager.client
            return milvus_client
        except Exception as e:
            raise e

AsyncMilvusDep=Annotated[MilvusClient,Depends(MilvusManager.get_milvus)]



