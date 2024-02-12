from pydantic import BaseModel


class CranesBaseSchema(BaseModel):
    """Схема кранов"""
    title: str
    size_x: int
    size_y: int
    photo: str
    is_broken: bool


class CranesSchema(CranesBaseSchema):
    """Схема кранов для чтения"""
    id: int

    class Config:
        orm_mode = True
