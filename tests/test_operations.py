import pytest

from sqlalchemy import select, insert
from database.data_input_orm import DataInputOrm
from models.data_input import DataInput

from conftest import async_session_maker


class TestDataInput:
    @pytest.mark.parametrize(
        "text, url",
        [
            ('test text', 'https://test.url')
        ]
    )
    async def test_save_data(self, text, url):
        async with async_session_maker() as session:
            stmt = insert(DataInputOrm).values(text=text, url=url)
            await session.execute(stmt)
            await session.commit()

            query = select(DataInputOrm)
            result = await session.execute(query)
            obj = result.scalars().first()
            assert (obj.text, obj.url) == ('test text', 'https://test.url')

