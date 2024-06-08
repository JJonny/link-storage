from typing import Annotated

from fastapi import APIRouter, Depends, Request

from models.data_input import DataInput
from database.repository import DataRepository


router = APIRouter(prefix='/data')


@router.post("")
async def data(data_: Annotated[DataInput, Depends()]):
    data_id = await DataRepository.save_data(data_)
    return {"ok": True, "data_id": data_id}


@router.get("")
async def get_all_data():
    datas = await DataRepository.find_all()
    return {"datas": datas}
