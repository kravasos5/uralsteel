from pydantic import BaseModel


class CranesCreateUpdateDTO(BaseModel):
    """Схема кранов"""
    title: str
    size_x: int
    size_y: int
    photo: str
    is_broken: bool


class CranesUpdatePatchDTO(BaseModel):
    """Схема кранов для patch метода"""
    title: str | None = None
    size_x: int | None = None
    size_y: int | None = None
    photo: str | None = None
    is_broken: bool | None = None


class CranesReadDTO(CranesCreateUpdateDTO):
    """Схема кранов для чтения"""
    id: int

    class Config:
        from_attributes = True
