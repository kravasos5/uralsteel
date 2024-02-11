from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from .commons import IdMixin


###################################################################
# Модели ковшей
class Ladles(IdMixin):
    """Модель ковшей"""
    __tablename__ = 'visual_ladles'

    title = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    is_broken = Column(Boolean, nullable=False, default=False)

    dynamic_table = relationship('DynamicTableMixin', back_populates='ladle_info')
    accidents = relationship('LadlesAccident', back_populates='object_info')