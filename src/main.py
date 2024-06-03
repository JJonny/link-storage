from fastapi import FastAPI, Request
from pydantic import BaseModel

from src.models.data_input import DataInput


app = FastAPI()


@app.post('/data')
async def save_data(data: DataInput, request: Request):
    print(data.text, data.url)
