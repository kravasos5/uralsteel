from pydantic import BaseModel


class LadlesBaseSchema(BaseModel):
    """Схема ковша"""
    title: str
    is_active: int
    is_broken: bool


class LadlesSchema(LadlesBaseSchema):
    """Схема ковша для чтения"""
    id: int

    class Config:
        orm_mode = True
