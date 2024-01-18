from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, String, TIMESTAMP, SmallInteger, BigInteger, func
from sqlalchemy.orm import relationship

from .database import Base


class IdMixin(Base):
    """Класс, добавляющий всем моделям поле id"""
    __abstract__ = True

    id = Column(BigInteger, primary_key=True)


class Posts(Enum):
    """Класс, содержащий должности"""
    MASTER = 'MS'
    MECHANIC = 'MH'
    DISPATCHER = 'DT'


class Employees(IdMixin):
    """Модель работника"""
    __tablename__ = "visual_employees"

    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    last_login = Column(TIMESTAMP, nullable=True)
    is_superuser = Column(Boolean, nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(TIMESTAMP, nullable=False)
    send_messages = Column(Boolean, nullable=False, default=True)
    photo = Column(String, nullable=True)
    post = Column(Posts, nullable=False)
    slug = Column(String, unique=True, index=True)

    reports = relationship('AccidentsMixin', back_populates='author_info')


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
    dynamic_table = relationship('DynamicTableMixin', back_populates='aggregates_info')
    accidents = relationship('AggregateAccident', back_populates='object_info')


class AggregatesBaseMixin(Base):
    """Базовый класс для всех агрегатов"""
    __abstract__ = True

    id = Column(BigInteger, primary_key=True)
    aggregates_ptr_id = Column(BigInteger, ForeignKey('visual_aggregates.id'),
                               unique=True, nullable=False)
    aggregate_info = relationship('Aggregates', uselist=False)


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


class Cranes(IdMixin):
    """Модель кранов"""
    __tablename__ = 'visual_cranes'

    title = Column(String, nullable=False)
    size_x = Column(SmallInteger, nullable=False)
    size_y = Column(SmallInteger, nullable=False)
    photo = Column(String, nullable=False)
    is_broken = Column(Boolean, default=False, nullable=False)

    accidents = relationship('CranesAccident', back_populates='object_info')


class Ladles(IdMixin):
    """Модель ковшей"""
    __tablename__ = 'visual_ladles'

    title = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    is_broken = Column(Boolean, nullable=False, default=False)

    dynamic_table = relationship('DynamicTableMixin', back_populates='ladle_info')
    accidents = relationship('LadlesAccident', back_populates='object_info')


class BrandSteel(IdMixin):
    """Модель марок стали"""
    __tablename__ = 'visual_brandsteel'

    title = Column(String, nullable=False)

    dynamic_table = relationship('DynamicTableMixin', back_populates='brand_steel_info')


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

    ladle_info = relationship('Ladles')
    brand_steel_info = relationship('BrandSteel')
    route_info = relationship('Routes')
    aggregate_info = relationship('Aggregates')


class ArchiveDynamicTable(DynamicTableMixin):
    """Модель архивных записей динамической таблицы"""
    __tablename__ = 'visual_archivedynamictable'


class ActiveDynamicTable(DynamicTableMixin):
    """Модель активных записей динамической таблицы"""
    __tablename__ = 'visual_activedynamictable'


class AccidentsMixin(Base):
    """Модель происшествий"""
    __abstract__ = True

    id = Column(BigInteger, primary_key=True)
    author = Column(BigInteger, ForeignKey('visual_employees'), nullable=False)
    report = Column(String, default=None, nullable=True)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)

    author_info = relationship('Employees', back_populates='reports')


class LadlesAccident(AccidentsMixin):
    """Модель проишествий ковшей"""
    __tablename__ = 'visual_ladlesaccident'

    object = Column(BigInteger, ForeignKey('visual_ladles'), nullable=True)

    object_info = relationship('Ladles', back_populates='accidents')


class CranesAccident(AccidentsMixin):
    """Модель проишествий кранов"""
    __tablename__ = 'visual_cranesaccident'

    object = Column(BigInteger, ForeignKey('visual_cranes'), nullable=True)

    object_info = relationship('Cranes', back_populates='accidents')


class AggregateAccident(AccidentsMixin):
    """Модель проишествий агрегатов"""
    __tablename__ = 'visual_aggregataccident'

    object = Column(BigInteger, ForeignKey('visual_aggregates'), nullable=True)

    object_info = relationship('Aggregates', back_populates='accidents')
