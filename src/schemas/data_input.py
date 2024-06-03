from pydantic import BaseModel


class DataInput(BaseModel):
    text: str
    url: str
