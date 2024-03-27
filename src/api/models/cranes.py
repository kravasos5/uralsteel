from sqlalchemy import String, Boolean, SmallInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base, idpk


class CranesORM(Base):
    """Модель кранов"""
    __tablename__ = 'visual_cranes'

    id: Mapped[idpk]
    title: Mapped[str] = mapped_column(String(100))
    size_x: Mapped[int] = mapped_column(SmallInteger)
    size_y: Mapped[int] = mapped_column(SmallInteger)
    photo: Mapped[str] = mapped_column(String(100))
    is_broken: Mapped[bool] = mapped_column(Boolean, default=False)

    accidents: Mapped[list['CranesAccidentORM']] = relationship(
        back_populates='object_info'
    )
