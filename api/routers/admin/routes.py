from http import HTTPStatus

from fastapi import APIRouter

from dependencies import UOWDep, GetIdDEP, error_raiser_if_none, is_object
from schemas.routes import RoutersReadShortDTO, RoutersCreateUpdateDTO, RoutersUpdatePatchDTO
from services.aggregates import AggregatesGMPService, AggregatesUKPService, AggregatesUVSService, AggregatesMNLZService
from services.routes import RoutesService
from utils.unitofwork import AbstractUnitOfWork

router = APIRouter(
    prefix='/route',
)


error_raiser_message: str = 'Route'


async def is_aggregates(
    uow: AbstractUnitOfWork,
    ag1_id: int,
    ag2_id: int,
    ag3_id: int,
    ag4_id: int
):
    """Проверка существуют ли такие агрегаты"""
    if ag1_id is not None:
        await is_object(uow, ag1_id, AggregatesGMPService(), 'GMP (aggregate_1_id)')
    if ag2_id is not None:
        await is_object(uow, ag2_id, AggregatesUKPService(), 'UKP (aggregate_2_id)')
    if ag3_id is not None:
        await is_object(uow, ag3_id, AggregatesUVSService(), 'UVS (aggregate_3_id)')
    if ag4_id is not None:
        await is_object(uow, ag4_id, AggregatesMNLZService(), 'MNLZ (aggregate_4_id)')


@router.get('/routes', response_model=list[RoutersReadShortDTO])
async def get_routes(uow: UOWDep, offset: int = 0, limit: int = 100):
    """Получение маршрутов"""
    route = await RoutesService().retrieve_all(uow, offset, limit)
    return route


@router.post('/create', response_model=RoutersReadShortDTO)
async def create_route(uow: UOWDep, route_data: RoutersCreateUpdateDTO):
    """Создание маршрута"""
    await is_aggregates(
        uow,
        route_data.aggregate_1_id,
        route_data.aggregate_2_id,
        route_data.aggregate_3_id,
        route_data.aggregate_4_id
    )
    new_route = await RoutesService().create_one(uow, route_data)
    return new_route


@router.get('/{object_id}', response_model=RoutersReadShortDTO)
async def get_route(uow: UOWDep, object_id: GetIdDEP):
    """Получение маршрута"""
    route = await RoutesService().retrieve_one(uow, id=object_id)
    await error_raiser_if_none(route, error_raiser_message)
    return route


@router.put('/update/{object_id}', response_model=RoutersReadShortDTO)
async def update_route_put(
        uow: UOWDep,
        object_id: GetIdDEP,
        route_data: RoutersCreateUpdateDTO
):
    """Обновление маршрута методом put"""
    await is_aggregates(
        uow,
        route_data.aggregate_1_id,
        route_data.aggregate_2_id,
        route_data.aggregate_3_id,
        route_data.aggregate_4_id
    )
    updated_route = await RoutesService().update_one(uow, route_data, id=object_id)
    await error_raiser_if_none(updated_route, error_raiser_message)
    return updated_route


@router.patch('/update/{object_id}', response_model=RoutersReadShortDTO)
async def update_route_patch(
        uow: UOWDep,
        object_id: GetIdDEP,
        route_data: RoutersUpdatePatchDTO
):
    """Обновление маршрута методом patch"""
    await is_aggregates(
        uow,
        route_data.aggregate_1_id,
        route_data.aggregate_2_id,
        route_data.aggregate_3_id,
        route_data.aggregate_4_id
    )
    updated_route = await RoutesService().update_one(uow, route_data, id=object_id)
    await error_raiser_if_none(updated_route, error_raiser_message)
    return updated_route


@router.delete('/delete/{object_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_route(uow: UOWDep, object_id: GetIdDEP):
    """Удаление маршрута по id"""
    deleted_route = await RoutesService().delete_one(uow, id=object_id)
    await error_raiser_if_none(deleted_route, error_raiser_message)
