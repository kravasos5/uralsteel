from sqlalchemy import Column, String, Boolean, SmallInteger
from sqlalchemy.orm import relationship

from .commons import IdMixin


###################################################################
# Модели кранов
class Cranes(IdMixin):
    """Модель кранов"""
    __tablename__ = 'visual_cranes'

    title = Column(String, nullable=False)
    size_x = Column(SmallInteger, nullable=False)
    size_y = Column(SmallInteger, nullable=False)
    photo = Column(String, nullable=False)
    is_broken = Column(Boolean, default=False, nullable=False)

    accidents = relationship('CranesAccident', back_populates='object_info')