
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated 
from backend.app.core.config import settings
from sqlalchemy.orm import Session
from fastapi import  Depends
engine = create_async_engine(settings.async_database_url, pool_pre_ping=True, future=True)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)



class Base(DeclarativeBase):
    """所有 ORM 模型的基类。"""



async def get_db():
    async with async_session_factory() as session:
        try: 
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

DBSessionDep = Annotated[Session,Depends(get_db)]