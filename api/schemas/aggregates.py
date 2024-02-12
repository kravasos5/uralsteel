from datetime import datetime

from pydantic import BaseModel


class AggregatesBaseDTO(BaseModel):
    """Схема агрегатов (справочная информация)"""
    title: str
    num_agg: str
    num_pos: str
    coord_x: int
    coord_y: int
    stay_time: datetime
    photo: str
    is_broken: bool


class AggregatesDTO(AggregatesBaseDTO):
    """Схема агрегатов (справочная информация) для чтения"""
    id: int

    class Config:
        from_attributes = True
