import uuid
from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


idpk = Annotated[
    uuid.UUID, mapped_column(primary_key=True, default=uuid.uuid4)
]


class Model(DeclarativeBase):
    id: Mapped[idpk]
