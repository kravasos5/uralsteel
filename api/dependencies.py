from enum import Enum
from http import HTTPStatus
from typing import Annotated, Any

from fastapi import Depends, Path, HTTPException, Query

from services.accidents import CranesAccidentService, LadlesAccidentService, AggregatesAccidentService
from services.dynamic import ActiveDynamicTableService, ArchiveDynamicTableService
from services.aggregates import AggregatesGMPService, AggregatesUKPService, AggregatesUVSService,\
    AggregatesMNLZService, AggregatesLService, AggregatesBurnerService
from services.employees import EmployeesService
from utils.service_base import ServiceBase
from utils.unitofwork import AbstractUnitOfWork, UnitOfWork


UOWDep = Annotated[AbstractUnitOfWork, Depends(UnitOfWork)]


def get_object_id(object_id: Annotated[int, Path(gt=0)]):
    """object_id зависимость"""
    return object_id


GetIdDEP = Annotated[int, Depends(get_object_id)]


class AccidentType(str, Enum):
    """Типы инцидентов"""
    crane: str = 'Cranes'
    ladle: str = 'Ladles'
    aggregate: str = 'Aggregates'


def get_accident_type(accident_type: Annotated[AccidentType, Query()]):
    """Зависимость типа инцидента"""
    return accident_type


GetAccTypeDEP = Annotated[AccidentType, Depends(get_accident_type)]


def error_raiser_if_none(obj: Any, message_name: str = 'Object'):
    """Вызывает ошибку, если нет такого объекта"""
    if not obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"{message_name} not found")


def is_object(uow, object_id: int, service: ServiceBase, message: str = 'Object'):
    """Проверка есть ли объект с таким id"""
    obj = service.retrieve_one(uow, id=object_id)
    error_raiser_if_none(obj, message)


def is_author_and_accident_object(
        uow: AbstractUnitOfWork,
        author_id: int,
        object_id: int,
        service: ServiceBase
):
    """Проверка наличия автора и агрегата с таким id"""
    is_object(uow, author_id, EmployeesService(), 'Author')
    is_object(uow, object_id, service)


def get_accident_service(acc_type: GetAccTypeDEP):
    """Зависимость сервиса происшествий"""
    service = None
    match acc_type:
        case AccidentType.crane:
            service = CranesAccidentService()
        case AccidentType.ladle:
            service = LadlesAccidentService()
        case AccidentType.aggregate:
            service = AggregatesAccidentService()
    return service


AccServiceDEP = Annotated[ServiceBase, Depends(get_accident_service)]


class AggregateType(str, Enum):
    """Перечисление агрегатов"""
    gmp: str = 'GMP'
    ukp: str = 'UKP'
    uvs: str = 'UVS'
    mnlz: str = 'MNLZ'
    l: str = 'L'
    burner: str = 'Burner'


def get_aggregate_type(aggregate_type: Annotated[AggregateType, Query()]):
    """Зависимость типа агрегата"""
    return aggregate_type


GetAggTypeDEP = Annotated[AggregateType, Depends(get_aggregate_type)]


def get_aggregate_service(agg_type: GetAggTypeDEP):
    """Зависимость сервиса агрегатов"""
    service = None
    match agg_type:
        case AggregateType.gmp:
            service = AggregatesGMPService()
        case AggregateType.ukp:
            service = AggregatesUKPService()
        case AggregateType.uvs:
            service = AggregatesUVSService()
        case AggregateType.mnlz:
            service = AggregatesMNLZService()
        case AggregateType.l:
            service = AggregatesLService()
        case AggregateType.burner:
            service = AggregatesBurnerService()
    return service


AggregatesServiceDEP = Annotated[ServiceBase, Depends(get_aggregate_service)]


class DynamicTableType(str, Enum):
    """Перечисление типов динамических таблиц"""
    active: str = 'active'
    archive: str = 'archive'


def get_dynamic_type(dynamic_type: Annotated[DynamicTableType, Query()]):
    """Зависимость типов динамических таблиц"""
    return dynamic_type


GetDynTypeDEP = Annotated[DynamicTableType, Depends(get_dynamic_type)]


def get_dynamic_service(dyn_type: GetDynTypeDEP):
    """Зависимость сервиса динамических таблиц"""
    service = None
    match dyn_type:
        case DynamicTableType.active:
            service = ActiveDynamicTableService()
        case DynamicTableType.archive:
            service = ArchiveDynamicTableService()
    return service


DynamicServiceDEP = Annotated[ServiceBase, Depends(get_dynamic_service)]
