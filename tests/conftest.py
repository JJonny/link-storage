import asyncio
import pytest

from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from httpx import AsyncClient
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator

from core.config import config
from database.base_model import Model
from database.data_input_orm import DataInputOrm
from main import app
from utils.user_constants import ACCESS_TOKEN_TTL, USER_ROLES, PERMISSIONS

TEST_BASE_DIR = Path(__file__).parent.absolute()

engin_test = create_async_engine(
    f"sqlite+aiosqlite:///{TEST_BASE_DIR}/storage_test.db",
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


@pytest.fixture(scope='session')
def create_token() -> bytes:
    payload = {}
    now = datetime.now(timezone.utc)
    expire = datetime.timestamp(now + timedelta(hours=ACCESS_TOKEN_TTL))
    payload["type"] = "access"
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = "123-456"
    payload["perms"] = [{USER_ROLES.admin: PERMISSIONS.admin_permissions}]

    yield jwt.encode(payload, config.JWT_SECRET)
