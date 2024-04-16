from pydantic import BaseModel


class CranesCreateUpdateDTO(BaseModel):
    """Схема кранов"""
    title: str
    size_x: int
    size_y: int
    is_broken: bool
    photo: str


class CranesUpdatePatchDTO(BaseModel):
    """Схема кранов для patch метода"""
    title: str | None = None
    size_x: int | None = None
    size_y: int | None = None
    is_broken: bool | None = None
    photo: str | None = None


class CranesReadDTO(CranesCreateUpdateDTO):
    """Схема кранов для чтения"""
    id: int

    class ConfigDict:
        from_attributes = True
