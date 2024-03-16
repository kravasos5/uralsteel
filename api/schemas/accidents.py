from datetime import datetime

from pydantic import BaseModel

from schemas.aggregates import AggregatesReadDTO
from schemas.cranes import CranesReadDTO
from schemas.employees import EmployeesReadDTO
from schemas.ladles import LadlesReadDTO


class AccidentsCreateDTO(BaseModel):
    """Схема обновления происшествий"""
    report: str | None = None
    object_id: int


class AccidentsCreateUpdateDTO(AccidentsCreateDTO):
    """Схема обновления происшествий"""
    author_id: int
    report: str | None
    object_id: int


class AccidentsUpdatePatchDTO(BaseModel):
    """Схема обновления происшествий"""
    author_id: int | None = None
    report: str | None = None
    object_id: int | None = None


class AccidentReadDTO(AccidentsCreateUpdateDTO):
    """Схема происшествий для чтения"""
    id: int
    created_at: datetime
    author_info: EmployeesReadDTO


class AccidentReadShortDTO(AccidentsCreateUpdateDTO):
    """Схема происшествий для чтения"""
    id: int
    created_at: datetime


class LadlesAccidentReadDTO(AccidentReadDTO):
    """Схема происшествий с ковшами"""
    object_info: LadlesReadDTO


class CranesAccidentReadDTO(AccidentReadDTO):
    """Модель проишествий кранов"""
    object_info: CranesReadDTO


class AggregateAccidentReadDTO(AccidentReadDTO):
    """Модель проишествий кранов"""
    object_info: AggregatesReadDTO
