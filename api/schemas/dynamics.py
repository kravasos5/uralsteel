from datetime import datetime

from pydantic import BaseModel

from schemas.aggregates import AggregatesDTO
from schemas.brandsteel import BrandSteelDTO
from schemas.ladles import LadlesDTO
from schemas.routes import RoutesDTO


class DynamicTableBaseDTO(BaseModel):
    """Схема основной таблицы с информацией о перемещении ковшей в реальном времени"""
    ladle: int
    num_melt: str
    brand_steel: int
    route: int
    aggregate: int
    plan_start: datetime
    plan_end: datetime
    actual_start: datetime
    actual_end: datetime
    ladle_info: LadlesDTO
    brand_steel_info: BrandSteelDTO
    route_info: RoutesDTO
    aggregate_info: AggregatesDTO


class DynamicTableDTO(DynamicTableBaseDTO):
    """
    Схема основной таблицы с информацией о перемещении ковшей в реальном времени.
    Для чтения.
    """
    id: int
