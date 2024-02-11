from datetime import datetime

from pydantic import BaseModel

from schemas.aggregates import AggregatesSchema
from schemas.cranes import CranesSchema
from schemas.employees import EmployeesReadSchema
from schemas.ladles import LadlesSchema


###################################################################
# Схемы проишествий
class AccidentsBaseSchema(BaseModel):
    """Схема происшествий"""
    author: int
    report: str
    created_at: datetime
    author_info: EmployeesReadSchema
    object: int


class LadlesAccidentSchema(AccidentsBaseSchema):
    """Схема происшествий с ковшами"""
    object_info: list[LadlesSchema]


class CranesAccidentSchema(AccidentsBaseSchema):
    """Модель проишествий кранов"""
    object_info: list[CranesSchema]


class AggregateAccidentSchema(AccidentsBaseSchema):
    """Модель проишествий кранов"""
    object_info: list[AggregatesSchema]
