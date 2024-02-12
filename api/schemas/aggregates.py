from datetime import datetime

from pydantic import BaseModel


class AggregatesBaseSchema(BaseModel):
    """Схема агрегатов (справочная информация)"""
    title: str
    num_agg: str
    num_pos: str
    coord_x: int
    coord_y: int
    stay_time: datetime
    photo: str
    is_broken: bool


class AggregatesSchema(AggregatesBaseSchema):
    """Схема агрегатов (справочная информация) для чтения"""
    id: int

    class Config:
        orm_mode = True
