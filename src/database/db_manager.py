from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database.base_model import Model
from database.data_input_orm import DataInputOrm


BASE_DIR = Path(__file__).parents[1].absolute()


engin = create_async_engine(
    f"sqlite+aiosqlite:///{BASE_DIR}/storage.db",
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
    import asyncio
    asyncio.run(delete_tables())
    asyncio.run(create_tables())
