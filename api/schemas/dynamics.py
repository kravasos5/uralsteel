from datetime import datetime

from pydantic import BaseModel

from schemas.aggregates import AggregatesReadDTO
from schemas.brandsteel import BrandSteelReadDTO
from schemas.ladles import LadlesReadDTO
from schemas.routes import RoutersReadShortDTO


class DynamicTableCreateUpdateDTO(BaseModel):
    """Схема создания динамических таблиц"""
    num_melt: str
    brand_steel_id: int
    plan_start: datetime
    plan_end: datetime
    actual_start: datetime | None
    actual_end: datetime | None
    aggregate_id: int
    ladle_id: int
    route_id: int


class DynamicTableUpdatePatchDTO(BaseModel):
    """Схема создания динамических таблиц"""
    num_melt: str | None = None
    brand_steel_id: int | None = None
    plan_start: datetime | None = None
    plan_end: datetime | None = None
    actual_start: datetime | None = None
    actual_end: datetime | None = None
    aggregate_id: int | None = None
    ladle_id: int | None = None
    route_id: int | None = None


class DynamicTableReadDTO(DynamicTableCreateUpdateDTO):
    """Схема чтения информации с динамической таблицы краткая"""
    id: int


class DynamicTableFullReadDTO(DynamicTableReadDTO):
    """Схема чтения информации с динамической таблицы краткая"""
    brand_steel_info: BrandSteelReadDTO
    aggregate_info: AggregatesReadDTO
    ladle_info: LadlesReadDTO
    route_info: RoutersReadShortDTO
