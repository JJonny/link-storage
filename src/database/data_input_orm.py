from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.base_model import Model


class DataInputOrm(Model):
    __tablename__ = 'data_input'

    text: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)


