import datetime
from typing import Annotated
from uuid import UUID

from sqlalchemy import text, types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


idpk = Annotated[
    UUID, mapped_column(types.Uuid, primary_key=True, init=False, server_default=text('gen_random_uuid()'))
]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Model(DeclarativeBase):
    id: Mapped[idpk]


class DataInputOrm(Model):
    __tablename__ = 'data_input'

    text: Mapped[str]
    url: Mapped[str]
    created_at: Mapped[created_at]