from sqlalchemy import Column, String, TIMESTAMP, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, declared_attr

from database import Base


###################################################################
# Модели динамических таблиц
class DynamicTableMixin(Base):
    """Основная таблица с информацией о перемещении ковшей в реальном времени"""
    __abstract__ = True

    id = Column(BigInteger, primary_key=True)
    ladle = Column(BigInteger, ForeignKey('visual_ladles.id'),
                   nullable=False)
    num_melt = Column(String, nullable=False)
    brand_steel = Column(BigInteger, ForeignKey('visual_brandsteel.id'),
                         nullable=False)
    route = Column(BigInteger, ForeignKey('visual_routes.id'),
                   nullable=False)
    aggregate = Column(BigInteger, ForeignKey('visual_aggregates.id'),
                       nullable=False)
    plan_start = Column(TIMESTAMP, nullable=False)
    plan_end = Column(TIMESTAMP, nullable=False)
    actual_start = Column(TIMESTAMP, nullable=True)
    actual_end = Column(TIMESTAMP, nullable=True)

    @declared_attr
    def ladle_info(self):
        return relationship('Ladles', uselist=False)

    @declared_attr
    def brand_steel_info(self):
        return relationship('BrandSteel', uselist=False)

    @declared_attr
    def route_info(self):
        return relationship('Routes', uselist=False)

    # @declared_attr
    # def aggregate_info(self):
    #     return relationship('Aggregates', uselist=False)


class ArchiveDynamicTable(DynamicTableMixin):
    """Модель архивных записей динамической таблицы"""
    __tablename__ = 'visual_archivedynamictable'


class ActiveDynamicTable(DynamicTableMixin):
    """Модель активных записей динамической таблицы"""
    __tablename__ = 'visual_activedynamictable'
