from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from .commons import IdMixin


###################################################################
# Модели маршрутов
class Routes(IdMixin):
    """Модель маршрутов"""
    __tablename__ = 'visual_routes'

    aggregate_1 = Column(BigInteger, ForeignKey('visual_aggregatesgmp.id'),
                         nullable=False)
    aggregate_2 = Column(BigInteger, ForeignKey('visual_aggregatesukp.id'),
                         nullable=False)
    aggregate_3 = Column(BigInteger, ForeignKey('visual_aggregatesuvs.id'),
                         nullable=False)
    aggregate_4 = Column(BigInteger, ForeignKey('visual_aggregatesmnlz.id'),
                         nullable=False)

    aggregate_gmp = relationship('AggregatesGMP', back_populates='routes')
    aggregate_ukp = relationship('AggregatesUKP', back_populates='routes')
    aggregate_uvs = relationship('AggregatesUVS', back_populates='routes')
    aggregate_mnlz = relationship('AggregatesMNLZ', back_populates='routes')
    dynamic_table = relationship('DynamicTableMixin', back_populates='route_info')
