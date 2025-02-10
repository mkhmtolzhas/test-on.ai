from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .config import settings, Settings

class Database:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.engine = create_async_engine(settings.database_url)
        self.session = async_sessionmaker(self.engine, class_=AsyncSession)

    async def get_session(self):
        async with self.session() as session:
            yield session

    async def close(self):
        await self.engine.dispose()


    

database = Database(settings)

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]

class Base(DeclarativeBase):
    pass