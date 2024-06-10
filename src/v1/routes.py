from typing import Annotated

from fastapi import APIRouter, Depends, Request

from models.data_input import DataInput
from database.repository import DataRepository
from utils.user_constants import ACTION
from utils.decorators import auth_required


router = APIRouter(prefix='/data')


@router.post("")
@auth_required(ACTION.save_data)
async def data(data_: Annotated[DataInput, Depends()]):
    data_id = await DataRepository.save_data(data_)
    return {"ok": True, "data_id": data_id}


@router.get("")
async def get_all_data():
    datas = await DataRepository.find_all()
    return {"datas": datas}
