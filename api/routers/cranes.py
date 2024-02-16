from fastapi import APIRouter

from dependencies import UOWDep
from services.cranes import CranesService

router = APIRouter(
    prefix="/cranes",
    tags=["cranes"],
)


@router.get('/data')
def get_cranes_data(uow: UOWDep) -> dict:
    """Получить положения кранов и их картинки"""
    # проверка на авторизацию
    # написать схему ответа
    data = CranesService().get_cranes_pos_info(uow)
    return data
