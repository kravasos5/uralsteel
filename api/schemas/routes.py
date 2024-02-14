from pydantic import BaseModel

from schemas.aggregates import AggregatesReadDTO


class RoutesBaseDTO(BaseModel):
    """Схема маршрутов"""
    id: int


class RoutesFullReadDTO(RoutesBaseDTO):
    """Схема маршрутов"""
    aggregate_1: AggregatesReadDTO
    aggregate_2: AggregatesReadDTO
    aggregate_3: AggregatesReadDTO
    aggregate_4: AggregatesReadDTO


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
