from datetime import datetime

from pydantic import BaseModel


class AggregatesCreateUpdateDTO(BaseModel):
    """Схема создания агрегатов"""
    title: str
    num_agg: str
    num_pos: str
    coord_x: int
    coord_y: int
    stay_time: datetime
    photo: str
    is_broken: bool


class AggregatesReadDTO(AggregatesCreateUpdateDTO):
    """Схема агрегатов для чтения"""
    id: int

    class Config:
        from_attributes = True
