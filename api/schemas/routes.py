from pydantic import BaseModel

from schemas.aggregates import AggregatesDTO


class RoutesBaseDTO(BaseModel):
    """Схема маршрутов"""
    id: int


class RoutesFullReadDTO(RoutesBaseDTO):
    """Схема маршрутов"""
    aggregate_1: AggregatesDTO
    aggregate_2: AggregatesDTO
    aggregate_3: AggregatesDTO
    aggregate_4: AggregatesDTO


class RoutesReadDTO(RoutesBaseDTO):
    """Схема маршрутов для чтения"""
    class Config:
        from_attributes = True


class RoutersCreateUpdateDTO(BaseModel):
    """Схема создания маршрутов"""
    aggregate_1: int
    aggregate_2: int
    aggregate_3: int
    aggregate_4: int
