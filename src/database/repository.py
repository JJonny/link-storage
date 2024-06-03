from uuid import UUID

from sqlalchemy import select

from src.database.models import DataInputOrm
from src.schemas.data_input import DataInput
from src.database.db import new_session


class DataRepository:

    @classmethod
    async def save_data(cls, data: DataInput) -> UUID:
        async with new_session() as session:
            data_dict = data.model_dump()

            record = DataInputOrm(**data_dict)
            session.add(record)
            await session.flush()
            await session.commit()
            return record.id

    @classmethod
    async def find_all(cls):
        async with new_session() as session:
            query = select(DataInputOrm)
            result = await session.execute(query)
            data_models = result.scalars().all()
            return data_models