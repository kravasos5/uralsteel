from sqlalchemy import String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base, idpk


class LadlesORM(Base):
    """Модель ковшей"""
    __tablename__ = 'visual_ladles'

    id: Mapped[idpk]
    title: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_broken: Mapped[bool] = mapped_column(Boolean, default=False)

    active_dynamic_table: Mapped[list['ActiveDynamicTableORM']] = relationship(back_populates='ladle_info')
    archive_dynamic_table: Mapped[list['ArchiveDynamicTableORM']] = relationship(back_populates='ladle_info')
    accidents: Mapped[list['LadlesAccidentORM']] = relationship(back_populates='object_info')
