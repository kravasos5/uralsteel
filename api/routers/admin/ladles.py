from http import HTTPStatus

from fastapi import APIRouter

from dependencies import UOWDep, GetIdDEP, error_raiser_if_none
from schemas.ladles import LadlesReadDTO, LadlesCreateUpdateDTO, LadlesUpdatePatchDTO
from services.ladles import LadlesService

router = APIRouter(
    prefix="/admin/ladle",
    tags=["admin"],
)


@router.get('/ladles', response_model=list[LadlesReadDTO])
def get_ladles(uow: UOWDep, offset: int = 0, limit: int = 100):
    """Получение ковшей"""
    ladles = LadlesService().retrieve_all(uow, offset, limit)
    return ladles


@router.post('/create', response_model=LadlesReadDTO)
def create_ladle(uow: UOWDep, ladle_data: LadlesCreateUpdateDTO):
    """Создание ковша"""
    new_ladle = LadlesService().create_one(uow, ladle_data)
    return new_ladle


@router.get('/{object_id}', response_model=LadlesReadDTO)
def get_ladle(uow: UOWDep, object_id: GetIdDEP):
    """Получение ковша"""
    ladle = LadlesService().retrieve_one_by_id(uow, object_id)
    error_raiser_if_none(ladle)
    return ladle


@router.put('/update/{object_id}', response_model=LadlesReadDTO)
def update_ladle_put(
        uow: UOWDep,
        object_id: GetIdDEP,
        ladle_data: LadlesCreateUpdateDTO
):
    """Обновление ковша методом put"""
    updated_ladle = LadlesService().update_one(uow, ladle_data, id=object_id)
    error_raiser_if_none(updated_ladle, 'Ladle')
    return updated_ladle


@router.patch('/update/{object_id}', response_model=LadlesReadDTO)
def update_ladle_patch(
        uow: UOWDep,
        object_id: GetIdDEP,
        ladle_data: LadlesUpdatePatchDTO
):
    """Обновление ковша методом patch"""
    updated_ladle = LadlesService().update_one(uow, ladle_data, id=object_id)
    error_raiser_if_none(updated_ladle, 'Ladle')
    return updated_ladle


@router.delete('/delete/{object_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_ladle(uow: UOWDep, object_id: GetIdDEP):
    """Удаление ковша по id"""
    deleted_ladle = LadlesService().delete_one(uow, id=object_id)
    error_raiser_if_none(deleted_ladle)
