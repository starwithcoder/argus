
from backend.app.core.config import settings
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from fastapi import Request,Depends
from typing import Annotated






class DatabaseManager():
    

    def __init__(self,url:str) -> None:
        self._url:str = url
        self._engine:AsyncEngine | None = None 
        self._async_session_factory:async_sessionmaker[AsyncSession]|None = None



    async def connect(self):
        if self._engine is not None:
            return 
        
        self._engine = create_async_engine(
            self._url, 
            echo=settings.DEBUG,
            pool_pre_ping=True
            )
        self._async_session_factory = async_sessionmaker(
            self._engine, 
            expire_on_commit=False
            )

    async def close(self):
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
        if self._async_session_factory is not None:
            self._async_session_factory = None
    
    @property
    def url(self) -> str:
        return self._url

    
    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
       if self._async_session_factory is None:
           raise RuntimeError("Database is not connected")
       return self._async_session_factory

    @staticmethod
    async def get_db(request:Request):
        database_manager:DatabaseManager = request.app.state.database_manager
        factory:async_sessionmaker[AsyncSession] = database_manager.session_factory
        async with factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e
            finally:
            
                await session.close()


AsyncDSBSession = Annotated[AsyncSession, Depends(DatabaseManager.get_db)]


class Base(DeclarativeBase):
    """所有 ORM 模型的基类。"""


