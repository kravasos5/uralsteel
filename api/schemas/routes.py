from pydantic import BaseModel

from schemas.aggregates import AggregatesSchema


###################################################################
# Схемы маршрутов
class RoutesBaseSchema(BaseModel):
    """Схема маршрутов"""
    aggregate_1: AggregatesSchema
    aggregate_2: AggregatesSchema
    aggregate_3: AggregatesSchema
    aggregate_4: AggregatesSchema


class RoutesSchema(BaseModel):
    """Схема маршрутов для чтения"""
    id: int

    class Config:
        orm_mode = True
