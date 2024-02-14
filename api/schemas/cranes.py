from pydantic import BaseModel


class CranesCreateUpdateDTO(BaseModel):
    """Схема кранов"""
    title: str
    size_x: int
    size_y: int
    photo: str
    is_broken: bool


class CranesReadDTO(CranesCreateUpdateDTO):
    """Схема кранов для чтения"""
    id: int

    class Config:
        orm_mode = True
