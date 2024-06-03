import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.database.models import Model


engin = create_async_engine(
    "sqlite+aiosqlite:///storage.db",
    echo=True,
)


new_session = async_sessionmaker(engin, expire_on_commit=False)


async def create_tables():
    async with engin.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engin.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


if __name__ == '__main__':
    asyncio.run(create_tables())