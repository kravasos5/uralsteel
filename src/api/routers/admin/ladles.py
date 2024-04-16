from http import HTTPStatus

from fastapi import APIRouter

from dependencies import UOWDep, GetIdDEP, error_raiser_if_none
from schemas.ladles import LadlesReadDTO, LadlesCreateUpdateDTO, LadlesUpdatePatchDTO
from services.ladles import LadlesService

router = APIRouter(
    prefix='/ladle',
)


@router.get('/ladles', response_model=list[LadlesReadDTO])
async def get_ladles(uow: UOWDep, offset: int = 0, limit: int = 100):
    """Получение ковшей"""
    ladles = await LadlesService().retrieve_all(uow, offset, limit)
    return ladles


@router.post('/create', response_model=LadlesReadDTO)
async def create_ladle(uow: UOWDep, ladle_data: LadlesCreateUpdateDTO):
    """Создание ковша"""
    new_ladle = await LadlesService().create_one(uow, ladle_data)
    return new_ladle


@router.get('/{object_id}', response_model=LadlesReadDTO)
async def get_ladle(uow: UOWDep, object_id: GetIdDEP):
    """Получение ковша"""
    ladle = await LadlesService().retrieve_one_by_id(uow, object_id)
    await error_raiser_if_none(ladle)
    return ladle


@router.put('/update/{object_id}', response_model=LadlesReadDTO)
async def update_ladle_put(
        uow: UOWDep,
        object_id: GetIdDEP,
        ladle_data: LadlesCreateUpdateDTO
):
    """Обновление ковша методом put"""
    updated_ladle = await LadlesService().update_one(uow, ladle_data, id=object_id)
    await error_raiser_if_none(updated_ladle, 'Ladle')
    return updated_ladle


@router.patch('/update/{object_id}', response_model=LadlesReadDTO)
async def update_ladle_patch(
        uow: UOWDep,
        object_id: GetIdDEP,
        ladle_data: LadlesUpdatePatchDTO
):
    """Обновление ковша методом patch"""
    updated_ladle = await LadlesService().update_one(uow, ladle_data, id=object_id)
    await error_raiser_if_none(updated_ladle, 'Ladle')
    return updated_ladle


@router.delete('/delete/{object_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_ladle(uow: UOWDep, object_id: GetIdDEP):
    """Удаление ковша по id"""
    deleted_ladle = await LadlesService().delete_one(uow, id=object_id)
    await error_raiser_if_none(deleted_ladle)
