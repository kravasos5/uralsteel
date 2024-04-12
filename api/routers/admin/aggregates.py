from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, UploadFile, File

from dependencies import UOWDep, GetIdDEP, error_raiser_if_none, AggregatesServiceDEP, AggFieldsDEP, AggFieldsPatchDEP
from schemas.aggregates import AggregatesReadDTO, AggregatesCreateUpdateDTO, AggregatesUpdatePatchDTO
from utils.utilities import Base64Converter, PhotoAddToSchema

router = APIRouter(
    prefix='/aggregate',
)


path: str = 'photos/aggregates/'


@router.get('/aggregates', response_model=list[AggregatesReadDTO])
async def get_aggregates(uow: UOWDep, service: AggregatesServiceDEP, offset: int = 0, limit: int = 100):
    """Получение агрегатов"""
    aggregates = await service.retrieve_all(uow, offset, limit)
    answer_data = Base64Converter.key_to_base64(aggregates, is_list=True)
    return answer_data


@router.post('/create', response_model=AggregatesReadDTO)
async def create_aggregate(
    uow: UOWDep,
    service: AggregatesServiceDEP,
    aggregate_data: AggFieldsDEP,
    photo: Annotated[UploadFile, File()]
):
    """Создание агрегата"""
    create_data = await PhotoAddToSchema.file_add(photo, path, aggregate_data, AggregatesCreateUpdateDTO)
    new_aggregate = await service.create_one(uow, create_data)
    answer_data = Base64Converter.key_to_base64(new_aggregate)
    return answer_data


@router.get('/{object_id}', response_model=AggregatesReadDTO)
async def get_aggregate(uow: UOWDep, service: AggregatesServiceDEP, object_id: GetIdDEP):
    """Получение агрегата"""
    aggregate = await service.retrieve_one_by_id(uow, object_id)
    await error_raiser_if_none(aggregate, 'Aggregate')
    answer_data = Base64Converter.key_to_base64(aggregate)
    return answer_data


@router.put('/update/{object_id}', response_model=AggregatesReadDTO)
async def update_aggregate_put(
    uow: UOWDep,
    service: AggregatesServiceDEP,
    object_id: GetIdDEP,
    aggregate_data: AggFieldsDEP,
    photo: Annotated[UploadFile, File()],
):
    """Обновление агрегата методом put"""
    update_data = await PhotoAddToSchema.file_add(photo, path, aggregate_data, AggregatesCreateUpdateDTO)
    updated_aggregate = await service.update_one(uow, update_data, id=object_id)
    await error_raiser_if_none(updated_aggregate, 'Aggregate')
    answer_data = Base64Converter.key_to_base64(updated_aggregate)
    return answer_data


@router.patch('/update/{object_id}', response_model=AggregatesReadDTO)
async def update_aggregate_patch(
        uow: UOWDep,
        service: AggregatesServiceDEP,
        object_id: GetIdDEP,
        aggregate_data: AggFieldsPatchDEP,
        photo: Annotated[UploadFile, File()] = None,
):
    """Обновление агрегата методом patch"""
    aggregate_data = {key: value for key, value in aggregate_data.items() if value is not None}
    if photo:
        update_data = await PhotoAddToSchema.file_add(photo, path, aggregate_data, AggregatesUpdatePatchDTO)
    else:
        update_data = AggregatesUpdatePatchDTO(**aggregate_data)
    updated_aggregate = await service.update_one(uow, update_data, id=object_id)
    await error_raiser_if_none(updated_aggregate, 'Aggregate')
    answer_data = Base64Converter.key_to_base64(updated_aggregate)
    return answer_data


@router.delete('/delete/{object_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_aggregate(uow: UOWDep, service: AggregatesServiceDEP, object_id: GetIdDEP):
    """Удаление агрегата по id"""
    deleted_aggregate = await service.delete_one(uow, id=object_id)
    await error_raiser_if_none(deleted_aggregate, 'Aggregate')
