from pydantic import BaseModel


class BrandSteelBaseDTO(BaseModel):
    """Схема марок стали"""
    title: str

    class Config:
        orm_mode = True


class BrandSteelDTO(BrandSteelBaseDTO):
    """Схема марок стали для чтения"""
    id: int

    class Config:
        orm_mode = True
