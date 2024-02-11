from datetime import datetime

from pydantic import BaseModel

from schemas.aggregates import AggregatesSchema
from schemas.brandsteel import BrandSteelSchema
from schemas.ladles import LadlesSchema
from schemas.routes import RoutesSchema


###################################################################
# Схемы динамических таблиц
class DynamicTableBaseSchema(BaseModel):
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
    ladle_info: LadlesSchema
    brand_steel_info: BrandSteelSchema
    route_info: RoutesSchema
    aggregate_info: AggregatesSchema


class DynamicTableSchema(DynamicTableBaseSchema):
    """
    Схема основной таблицы с информацией о перемещении ковшей в реальном времени.
    Для чтения.
    """
    id: int
