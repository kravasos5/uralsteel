from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import idpk, Base


###################################################################
# Модели марок стали
class BrandSteelORM(Base):
    """Модель марок стали"""
    __tablename__ = 'visual_brandsteel'

    id: Mapped[idpk]
    title: Mapped[str] = mapped_column(String(100))

    active_dynamic_table: Mapped[list['ActiveDynamicTableORM']] = relationship(back_populates='brand_steel_info')
    archive_dynamic_table: Mapped[list['ArchiveDynamicTableORM']] = relationship(back_populates='brand_steel_info')
