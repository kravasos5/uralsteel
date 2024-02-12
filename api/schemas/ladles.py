from pydantic import BaseModel


class LadlesBaseDTO(BaseModel):
    """Схема ковша"""
    title: str
    is_active: int
    is_broken: bool


class LadlesDTO(LadlesBaseDTO):
    """Схема ковша для чтения"""
    id: int

    class Config:
        orm_mode = True
