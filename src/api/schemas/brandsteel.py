from pydantic import BaseModel


class BrandSteelCreateUpdateDTO(BaseModel):
    """Схема марок стали"""
    title: str


class BrandSteelUpdatePatchDTO(BaseModel):
    """Схема марок стали"""
    title: str | None = None


class BrandSteelReadDTO(BrandSteelCreateUpdateDTO):
    """Схема марок стали для чтения"""
    id: int

    class ConfigDict:
        from_attributes = True
