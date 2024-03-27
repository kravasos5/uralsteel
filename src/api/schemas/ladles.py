from pydantic import BaseModel


class LadlesCreateUpdateDTO(BaseModel):
    """Схема ковша"""
    title: str
    is_active: bool
    is_broken: bool


class LadlesUpdatePatchDTO(BaseModel):
    """Схема ковша"""
    title: str | None = None
    is_active: bool | None = False
    is_broken: bool | None = False


class LadlesReadDTO(LadlesCreateUpdateDTO):
    """Схема ковша для чтения"""
    id: int

    class Config:
        from_attributes = True
