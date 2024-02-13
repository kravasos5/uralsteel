from datetime import datetime

from pydantic import BaseModel

from schemas.aggregates import AggregatesReadDTO
from schemas.brandsteel import BrandSteelReadDTO
from schemas.ladles import LadlesReadDTO
from schemas.routes import RoutesReadDTO


class DynamicTableCreateUpdateDTO(BaseModel):
    """Схема создания динамических таблиц"""
    num_melt: str
    brand_steel_id: int
    plan_start: datetime
    plan_end: datetime
    actual_start: datetime
    actual_end: datetime
    aggregate_id: int
    ladle_id: int
    route_id: int


class DynamicTableReadDTO(DynamicTableCreateUpdateDTO):
    """Схема чтения информации с динамической таблицы краткая"""
    id: int


class DynamicTableFullReadDTO(BaseModel):
    """Схема чтения информации с динамической таблицы краткая"""
    id: int
    num_melt: str
    brand_steel_info: BrandSteelReadDTO
    plan_start: datetime
    plan_end: datetime
    actual_start: datetime
    actual_end: datetime
    aggregate_info: AggregatesReadDTO
    ladle_info: LadlesReadDTO
    route_info: RoutesReadDTO
