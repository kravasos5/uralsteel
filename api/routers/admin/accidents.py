from http import HTTPStatus
from typing import Type

from fastapi import APIRouter

from dependencies import UOWDep, GetIdDEP, error_raiser_if_none, AccServiceDEP, \
    is_author_and_accident_object, make_object_broken
from schemas.accidents import AccidentReadDTO, AccidentsUpdatePatchDTO, \
    AccidentReadShortDTO, AccidentsCreateUpdateDTO


router = APIRouter(
    prefix='/accident',
)


@router.get('/accidents')
async def get_accidents(uow: UOWDep, service: AccServiceDEP, offset: int = 0, limit: int = 100):
    """Получение отчётов инцидентов"""
    accidents = await service.retrieve_all(uow, offset, limit)
    return accidents


@router.post('/create', response_model=AccidentReadShortDTO)
async def create_accident(uow: UOWDep, service: AccServiceDEP, accident_data: AccidentsCreateUpdateDTO):
    """Создание происшествия"""
    # проверка есть ли такой автор и агрегат
    await is_author_and_accident_object(uow, accident_data.author_id, accident_data.object_id, service)
    new_accident = await service.create_one(uow, accident_data)
    # отметить объект отчёта сломанным
    await make_object_broken(uow, service, accident_data.object_id)
    return new_accident


@router.get('/{object_id}')
async def get_crane(uow: UOWDep, service: AccServiceDEP, object_id: GetIdDEP):
    """Получение происшествия"""
    accident = await service.retrieve_one_by_id(uow, object_id)
    await error_raiser_if_none(accident)
    return accident


@router.put('/update/{object_id}', response_model=AccidentReadShortDTO)
async def update_crane_put(
        uow: UOWDep,
        service: AccServiceDEP,
        object_id: GetIdDEP,
        accident_data: AccidentsCreateUpdateDTO
):
    """Обновление происшествия методом put"""
    # проверка есть ли такой автор и агрегат
    await is_author_and_accident_object(uow, accident_data.author_id, accident_data.object_id, service)
    updated_acc = await service.update_one(uow, accident_data, id=object_id)
    await error_raiser_if_none(updated_acc)
    return updated_acc


@router.patch('/update/{object_id}', response_model=AccidentReadShortDTO)
async def update_crane_patch(
        uow: UOWDep,
        service: AccServiceDEP,
        object_id: GetIdDEP,
        accident_data: AccidentsUpdatePatchDTO
):
    """Обновление происшествия методом put"""
    # проверка есть ли такой автор и агрегат
    await is_author_and_accident_object(uow, accident_data.author_id, accident_data.object_id, service)
    updated_acc = await service.update_one(uow, accident_data, id=object_id)
    await error_raiser_if_none(updated_acc)
    return updated_acc


@router.delete('/delete/{object_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_crane(uow: UOWDep, service: AccServiceDEP, crane_id: GetIdDEP):
    """Удаление происшествия по id"""
    deleted_acc = await service.delete_one(uow, id=crane_id)
    await error_raiser_if_none(deleted_acc)
