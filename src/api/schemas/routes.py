from pydantic import BaseModel

from schemas.aggregates import AggregatesReadDTO


class RoutesFullReadDTO(BaseModel):
    """Схема маршрутов"""
    id: int
    aggregate_1_id: AggregatesReadDTO
    aggregate_2_id: AggregatesReadDTO
    aggregate_3_id: AggregatesReadDTO
    aggregate_4_id: AggregatesReadDTO


class RoutersCreateUpdateDTO(BaseModel):
    """Схема создания маршрутов"""
    aggregate_1_id: int
    aggregate_2_id: int
    aggregate_3_id: int
    aggregate_4_id: int


class RoutersReadShortDTO(RoutersCreateUpdateDTO):
    """Схема создания маршрутов"""
    id: int

    class ConfigDict:
        from_attributes = True


class RoutersUpdatePatchDTO(BaseModel):
    """Схема создания маршрутов методом patch"""
    aggregate_1_id: int | None = None
    aggregate_2_id: int | None = None
    aggregate_3_id: int | None = None
    aggregate_4_id: int | None = None
