from datetime import datetime

from pydantic import BaseModel

from schemas.aggregates import AggregatesReadDTO
from schemas.cranes import CranesReadDTO
from schemas.employees import EmployeesReadDTO
from schemas.ladles import LadlesReadDTO


class AccidentsUpdateDTO(BaseModel):
    """Схема обновления происшествий"""
    author: int
    report: str | None
    object_id: int


class AccidentsCreateDTO(BaseModel):
    """Схема создания проишествий"""
    report: str | None
    object_id: int


class AccidentReadDTO(AccidentsUpdateDTO):
    """Схема происшествий для чтения"""
    id: int
    created_at: datetime
    author_info: EmployeesReadDTO


class LadlesAccidentReadDTO(AccidentReadDTO):
    """Схема происшествий с ковшами"""
    object_info: LadlesReadDTO


class CranesAccidentReadDTO(AccidentReadDTO):
    """Модель проишествий кранов"""
    object_info: CranesReadDTO


class AggregateAccidentReadDTO(AccidentReadDTO):
    """Модель проишествий кранов"""
    object_info: AggregatesReadDTO
