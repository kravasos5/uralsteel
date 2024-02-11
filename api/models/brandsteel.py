from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .commons import IdMixin


###################################################################
# Модели марок стали
class BrandSteel(IdMixin):
    """Модель марок стали"""
    __tablename__ = 'visual_brandsteel'

    title = Column(String, nullable=False)

    dynamic_table = relationship('DynamicTableMixin', back_populates='brand_steel_info')