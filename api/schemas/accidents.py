from datetime import datetime

from pydantic import BaseModel

from schemas.aggregates import AggregatesDTO
from schemas.cranes import CranesDTO
from schemas.employees import EmployeesReadDTO
from schemas.ladles import LadlesDTO


class AccidentsBaseDTO(BaseModel):
    """Схема происшествий"""
    author: int
    report: str
    created_at: datetime
    author_info: EmployeesReadDTO
    object: int


class LadlesAccidentDTO(AccidentsBaseDTO):
    """Схема происшествий с ковшами"""
    object_info: list[LadlesDTO]


class CranesAccidentDTO(AccidentsBaseDTO):
    """Модель проишествий кранов"""
    object_info: list[CranesDTO]


class AggregateAccidentDTO(AccidentsBaseDTO):
    """Модель проишествий кранов"""
    object_info: list[AggregatesDTO]
