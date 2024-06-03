import datetime
from typing import Annotated
from uuid import UUID

from sqlalchemy import text, types, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.database.db import engin


idpk = Annotated[
    UUID, mapped_column(types.Uuid, primary_key=True, init=False, server_default=text('gen_random_uuid()'))
]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Model(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class DataInputOrm(Model):
    __tablename__ = 'data_input'

    text: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    # created_at: Mapped[created_at]


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