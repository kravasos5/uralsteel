from http import HTTPStatus

from fastapi import APIRouter

from dependencies import UOWDep, GetIdDEP, error_raiser_if_none, AggregatesServiceDEP
from schemas.aggregates import AggregatesReadDTO, AggregatesCreateUpdateDTO, AggregatesUpdatePatchDTO

router = APIRouter(
    prefix="/admin/aggregate",
    tags=["admin"],
)


@router.get('/aggregates', response_model=list[AggregatesReadDTO])
def get_aggregates(uow: UOWDep, service: AggregatesServiceDEP, offset: int = 0, limit: int = 100):
    """Получение агрегатов"""
    aggregates = service.retrieve_all(uow, offset, limit)
    return aggregates


@router.post('/create', response_model=AggregatesReadDTO)
def create_aggregate(uow: UOWDep, service: AggregatesServiceDEP,  aggregate_data: AggregatesCreateUpdateDTO):
    """Создание агрегата"""
    new_aggregate = service.create_one(uow, aggregate_data)
    return new_aggregate


@router.get('/{object_id}', response_model=AggregatesReadDTO)
def get_aggregate(uow: UOWDep, service: AggregatesServiceDEP, object_id: GetIdDEP):
    """Получение агрегата"""
    aggregate = service.retrieve_one_by_id(uow, object_id)
    error_raiser_if_none(aggregate, 'Aggregate')
    return aggregate


@router.put('/update/{object_id}', response_model=AggregatesReadDTO)
def update_aggregate_put(
        uow: UOWDep,
        service: AggregatesServiceDEP,
        object_id: GetIdDEP,
        aggregate_data: AggregatesCreateUpdateDTO
):
    """Обновление агрегата методом put"""
    updated_aggregate = service.update_one(uow, aggregate_data, id=object_id)
    error_raiser_if_none(updated_aggregate, 'Aggregate')
    return updated_aggregate


@router.patch('/update/{object_id}', response_model=AggregatesReadDTO)
def update_aggregate_patch(
        uow: UOWDep,
        service: AggregatesServiceDEP,
        object_id: GetIdDEP,
        aggregate_data: AggregatesUpdatePatchDTO
):
    """Обновление агрегата методом patch"""
    updated_aggregate = service.update_one(uow, aggregate_data, id=object_id)
    error_raiser_if_none(updated_aggregate, 'Aggregate')
    return updated_aggregate


@router.delete('/delete/{object_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_aggregate(uow: UOWDep, service: AggregatesServiceDEP, object_id: GetIdDEP):
    """Удаление агрегата по id"""
    deleted_aggregate = service.delete_one(uow, id=object_id)
    error_raiser_if_none(deleted_aggregate, 'Aggregate')
