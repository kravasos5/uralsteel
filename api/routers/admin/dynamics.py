from http import HTTPStatus

from fastapi import APIRouter

from dependencies import UOWDep, GetIdDEP, error_raiser_if_none, DynamicServiceDEP, is_object
from schemas.dynamics import DynamicTableReadDTO, DynamicTableUpdatePatchDTO, DynamicTableCreateUpdateDTO
from services.aggregates import AggregatesAllService
from services.brandsteel import BrandSteelService
from services.ladles import LadlesService
from services.routes import RoutesService
from utils.unitofwork import AbstractUnitOfWork

router = APIRouter(
    prefix='/dynamic-tables',
)


error_raiser_message: str = 'Dynamic Table object'


async def is_bs_agg_ladle_route(
    uow: AbstractUnitOfWork,
    brand_steel_id: int | None,
    aggregate_id: int | None,
    ladle_id: int | None,
    route_id: int | None
):
    """
    Проверка есть ли записи связанных таблиц
    brand_steel, aggregate_id, ladle_id, route_id
    """
    if brand_steel_id is not None:
        await is_object(uow, brand_steel_id, BrandSteelService(), 'Brand steel')
    if aggregate_id is not None:
        await is_object(uow, aggregate_id, AggregatesAllService(), 'Aggregate')
    if ladle_id is not None:
        await is_object(uow, ladle_id, LadlesService(), 'Ladle')
    if route_id is not None:
        await is_object(uow, route_id, RoutesService(), 'Route')


@router.get('/all', response_model=list[DynamicTableReadDTO])
async def get_dyn(uow: UOWDep, service: DynamicServiceDEP, offset: int = 0, limit: int = 100):
    """Получение плана из динамической таблицы"""
    dyn = await service.retrieve_all(uow, offset, limit)
    return dyn


@router.post('/create', response_model=DynamicTableReadDTO)
async def create_dyn(uow: UOWDep, service: DynamicServiceDEP, dyn_data: DynamicTableCreateUpdateDTO):
    """Создание записи плана в динамической таблице"""
    # проверка
    await is_bs_agg_ladle_route(uow, dyn_data.brand_steel_id, dyn_data.aggregate_id, dyn_data.ladle_id, dyn_data.route_id)
    new_dyn = await service.create_one(uow, dyn_data)
    return new_dyn


@router.get('/{object_id}', response_model=DynamicTableReadDTO)
async def get_dyn(uow: UOWDep, service: DynamicServiceDEP, object_id: GetIdDEP):
    """Получение плана из динамической таблицы"""
    dyn = await service.retrieve_one(uow, id=object_id)
    await error_raiser_if_none(dyn, error_raiser_message)
    return dyn


@router.put('/update/{object_id}', response_model=DynamicTableReadDTO)
async def update_dyn_put(
        uow: UOWDep,
        service: DynamicServiceDEP,
        object_id: GetIdDEP,
        dyn_data: DynamicTableCreateUpdateDTO
):
    """Обновление плана методом put"""
    # проверка
    await is_bs_agg_ladle_route(uow, dyn_data.brand_steel_id, dyn_data.aggregate_id, dyn_data.ladle_id, dyn_data.route_id)
    updated_dyn = await service.update_one(uow, dyn_data, id=object_id)
    await error_raiser_if_none(updated_dyn, error_raiser_message)
    return updated_dyn


@router.patch('/update/{object_id}', response_model=DynamicTableReadDTO)
async def update_dyn_patch(
        uow: UOWDep,
        service: DynamicServiceDEP,
        object_id: GetIdDEP,
        dyn_data: DynamicTableUpdatePatchDTO
):
    """Обновление плана методом patch"""
    # проверка
    await is_bs_agg_ladle_route(uow, dyn_data.brand_steel_id, dyn_data.aggregate_id, dyn_data.ladle_id, dyn_data.route_id)
    updated_dyn = await service.update_one(uow, dyn_data, id=object_id)
    await error_raiser_if_none(updated_dyn, error_raiser_message)
    return updated_dyn


@router.delete('/delete/{object_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_dyn(uow: UOWDep, service: DynamicServiceDEP, object_id: GetIdDEP):
    """Удаление плана из динамической таблицы по id записи"""
    deleted_dyn = await service.delete_one(uow, id=object_id)
    await error_raiser_if_none(deleted_dyn, error_raiser_message)
