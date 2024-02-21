from fastapi import APIRouter, Depends

from dependencies import UOWDep, oauth2_scheme
from services.cranes import CranesService
from utils.utilities import Base64Converter

router = APIRouter(
    prefix='/cranes',
    tags=['cranes'],
    dependencies=[Depends(oauth2_scheme)],
)


@router.get('/data')
def get_cranes_data(uow: UOWDep) -> dict:
    """Получить положения кранов и их картинки"""
    # проверка на авторизацию
    # написать схему ответа
    data = CranesService().get_cranes_pos_info(uow)
    data['cranes_info'] = Base64Converter.key_to_base64(data['cranes_info'], is_nested=True)
    return data
