from fastapi import APIRouter

from dependencies import UOWDep
from services.dynamic import ActiveDynamicTableService

router = APIRouter(
    prefix="/ladles",
    tags=["ladles"],
)


@router.get('/time')
def get_time(uow: UOWDep) -> dict:
    """Получение информации о времени в форме времени на странице ковшей."""
    # проверка на авторизацию
    # написать схему ответа
    data = ActiveDynamicTableService().get_ladle_timeform()
    return data


# @router.get('/time')
# def get_time(uow: UOWDep) -> dict:
#     """Получение информации о положении ковшей на странице"""
#     # проверка на авторизацию
#     # написать схему ответа
#     data = ActiveDynamicTableService().get_ladle_timeform()
#     return data
