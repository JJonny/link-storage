import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


engin = create_async_engine(
    "sqlite+aiosqlite:///storage.db",
    echo=True,
)


new_session = async_sessionmaker(engin, expire_on_commit=False)
