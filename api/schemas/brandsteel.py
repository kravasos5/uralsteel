from pydantic import BaseModel


class BrandSteelCreateUpdateDTO(BaseModel):
    """Схема марок стали"""
    title: str


class BrandSteelReadDTO(BrandSteelCreateUpdateDTO):
    """Схема марок стали для чтения"""
    id: int

    class Config:
        orm_mode = True
