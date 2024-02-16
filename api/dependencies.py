from enum import Enum
from http import HTTPStatus
from typing import Annotated, Any

from fastapi import Depends, Path, HTTPException, Query

from services.aggregates import AggregatesAllService
from services.cranes import CranesService
from services.employees import EmployeesService
from services.ladles import LadlesService
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


def is_author(uow, author_id: int):
    """Проверка есть ли автор с таким id"""
    author = EmployeesService().retrieve_one_by_id(uow, author_id)
    error_raiser_if_none(author, 'Author')


def is_object(uow, object_id: int, object_type: AccidentType):
    """Проверка есть ли агрегат с таким id"""
    service = None
    match object_type:
        case AccidentType.crane:
            service = CranesService()
        case AccidentType.ladle:
            service = LadlesService()
        case AccidentType.aggregate:
            service = AggregatesAllService()
    obj = service.retrieve_one(uow, id=object_id)
    error_raiser_if_none(obj)
