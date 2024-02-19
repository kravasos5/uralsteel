from datetime import time

from pydantic import BaseModel


class AggregatesCreateUpdateDTO(BaseModel):
    """Схема создания агрегатов"""
    title: str
    num_agg: str
    num_pos: str
    coord_x: int
    coord_y: int
    stay_time: time
    is_broken: bool
    photo: str


class AggregatesUpdatePatchDTO(BaseModel):
    """Схема создания агрегатов"""
    title: str | None = None
    num_agg: str | None = None
    num_pos: str | None = None
    coord_x: int | None = None
    coord_y: int | None = None
    stay_time: time | None = None
    is_broken: bool | None = None
    photo: str | None = None


class AggregatesReadDTO(AggregatesCreateUpdateDTO):
    """Схема агрегатов для чтения"""
    id: int

    class Config:
        from_attributes = True
