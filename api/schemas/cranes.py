from pydantic import BaseModel


class CranesBaseDTO(BaseModel):
    """Схема кранов"""
    title: str
    size_x: int
    size_y: int
    photo: str
    is_broken: bool


class CranesDTO(CranesBaseDTO):
    """Схема кранов для чтения"""
    id: int

    class Config:
        orm_mode = True
