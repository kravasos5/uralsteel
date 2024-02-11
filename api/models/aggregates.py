from sqlalchemy import Column, String, TIMESTAMP, Boolean, func, SmallInteger, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, declared_attr

from database import Base
from .commons import IdMixin


###################################################################
# Модели агрегатов
class Aggregates(IdMixin):
    """Модель агрегатов (справочная информация)"""
    __tablename__ = "visual_aggregates"

    title = Column(String, nullable=False)
    num_agg = Column(String, nullable=False)
    num_pos = Column(String, nullable=False)
    coord_x = Column(SmallInteger, nullable=False)
    coord_y = Column(SmallInteger, nullable=False)
    stay_time = Column(TIMESTAMP, nullable=False)
    photo = Column(String, nullable=False)
    is_broken = Column(Boolean, nullable=False)

    aggregates_gmp = relationship('AggregatesGMP', back_populates='aggregate_info', uselist=False)
    aggregates_ukp = relationship('AggregatesUKP', back_populates='aggregate_info', uselist=False)
    aggregates_uvs = relationship('AggregatesUVS', back_populates='aggregate_info', uselist=False)
    aggregates_mnlz = relationship('AggregatesMNLZ', back_populates='aggregate_info', uselist=False)
    aggregates_l = relationship('AggregatesL', back_populates='aggregate_info', uselist=False)
    aggregates_burner = relationship('AggregatesBurner', back_populates='aggregate_info', uselist=False)
    # dynamic_table = relationship('DynamicTableMixin', back_populates='aggregates_info')
    accidents = relationship('AggregateAccident', back_populates='object_info')


class AggregatesBaseMixin(Base):
    """Базовый класс для всех агрегатов"""
    __abstract__ = True

    id = Column(BigInteger, primary_key=True)
    aggregates_ptr_id = Column(BigInteger, ForeignKey('visual_aggregates.id'),
                               unique=True, nullable=False)

    @declared_attr
    def aggregate_info(self):
        return relationship('Aggregates', uselist=False)


class AggregatesGMP(AggregatesBaseMixin):
    """Модель агрегатов ГМП"""
    __tablename__ = 'visual_aggregatesgmp'
    routes = relationship('Routes', back_populates='aggregate_gmp')


class AggregatesUKP(AggregatesBaseMixin):
    """Модель агрегатов УКП"""
    __tablename__ = 'visual_aggregatesukp'
    routes = relationship('Routes', back_populates='aggregate_ukp')


class AggregatesUVS(AggregatesBaseMixin):
    """Модель агрегатов УВС"""
    __tablename__ = 'visual_aggregatesuvs'
    routes = relationship('Routes', back_populates='aggregate_uvs')


class AggregatesMNLZ(AggregatesBaseMixin):
    """Модель агрегатов МНЛЗ"""
    __tablename__ = 'visual_aggregatesmnlz'
    routes = relationship('Routes', back_populates='aggregate_mnlz')


class AggregatesL(AggregatesBaseMixin):
    """Модель агрегатов Лёжек"""
    __tablename__ = 'visual_aggregatesl'


class AggregatesBurner(AggregatesBaseMixin):
    """Модель агрегатов Горелок"""
    __tablename__ = 'visual_aggregatesburner'