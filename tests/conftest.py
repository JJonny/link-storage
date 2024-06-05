import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.database.models import Model, DataInputOrm
from src.main import app

engin_test = create_async_engine(
    "sqlite+aiosqlite:///../../storage_test.db",
)
async_session_maker = async_sessionmaker(engin_test, expire_on_commit=False)


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engin_test.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    yield
    async with engin_test.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


app = TestClient(app)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
