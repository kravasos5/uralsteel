from pydantic import BaseModel


###################################################################
# Схемы марок стали
class BrandSteelBaseSchema(BaseModel):
    """Схема марок стали"""
    title: str

    class Config:
        orm_mode = True


class BrandSteelSchema(BrandSteelBaseSchema):
    """Схема марок стали для чтения"""
    id: int

    class Config:
        orm_mode = True
