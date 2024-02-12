from pydantic import BaseModel

from schemas.aggregates import AggregatesDTO


class RoutesBaseDTO(BaseModel):
    """Схема маршрутов"""
    id: int


class RoutesDTO(RoutesBaseDTO):
    """Схема маршрутов"""
    aggregate_1: AggregatesDTO
    aggregate_2: AggregatesDTO
    aggregate_3: AggregatesDTO
    aggregate_4: AggregatesDTO


class RoutesShortDTO(RoutesBaseDTO):
    """Схема маршрутов для чтения"""
    class Config:
        from_attributes = True
