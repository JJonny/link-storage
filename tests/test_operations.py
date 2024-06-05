import pytest

from sqlalchemy import select, insert
from src.database.models import DataInputOrm
from src.schemas.data_input import DataInput

from conftest import async_session_maker


async def test_save_data():
    async with async_session_maker() as session:
        stmt = insert(DataInputOrm).values(text='test text', url='https://test.url')
        await session.execute(stmt)
        await session.commit()

        query = select(DataInputOrm)
        result = await session.execute(query)
        obj = result.scalars().first()
        assert (obj.text, obj.url) == ('test text', 'https://test.url')

