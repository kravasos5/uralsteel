from pydantic import BaseModel


class LadlesCreateUpdateDTO(BaseModel):
    """Схема ковша"""
    title: str
    is_active: int
    is_broken: bool


class LadlesReadDTO(LadlesCreateUpdateDTO):
    """Схема ковша для чтения"""
    id: int

    class Config:
        from_attributes = True
