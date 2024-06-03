from typing import Annotated

from fastapi import APIRouter, Depends, Request

from src.schemas.data_input import DataInput
from src.database.repository import DataRepository


router = APIRouter(prefix='/data')


@router.post("")
async def save_data(data: Annotated[DataInput, Depends()], request: Request):
    print(data)
    data_id = await DataRepository.save_data(data)
    return {"ok": True, "data_id": data_id}


@router.get("")
async def save_data(data: Annotated[DataInput, Depends()], request: Request):
    datas = await DataRepository.find_all()
    return {"datas": datas}