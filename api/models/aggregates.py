from datetime import datetime

from sqlalchemy import String, TIMESTAMP, Boolean, SmallInteger, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, declared_attr, mapped_column, Mapped

from database import Base, idpk


class AggregatesORM(Base):
    """Модель агрегатов (справочная информация)"""
    __tablename__ = "visual_aggregates"

    id: Mapped[idpk]
    title: Mapped[str] = mapped_column(String(100))
    num_agg: Mapped[str] = mapped_column(String(100))
    num_pos: Mapped[str] = mapped_column(String(100))
    coord_x: Mapped[int] = mapped_column(SmallInteger)
    coord_y: Mapped[int] = mapped_column(SmallInteger)
    stay_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    photo: Mapped[str] = mapped_column(String(100))
    is_broken: Mapped[bool] = mapped_column(Boolean)

    aggregates_gmp: Mapped[list['AggregatesGMPORM']] = relationship(back_populates='aggregate_info')
    aggregates_ukp: Mapped[list['AggregatesUKPORM']] = relationship(back_populates='aggregate_info')
    aggregates_uvs: Mapped[list['AggregatesUVSORM']] = relationship(back_populates='aggregate_info')
    aggregates_mnlz: Mapped[list['AggregatesMNLZORM']] = relationship(back_populates='aggregate_info')
    aggregates_l: Mapped[list['AggregatesLORM']] = relationship(back_populates='aggregate_info')
    aggregates_burner: Mapped[list['AggregatesBurnerORM']] = relationship(back_populates='aggregate_info')
    accidents: Mapped[list['AggregatesAccidentORM']] = relationship(back_populates='object_info')
    active_dynamic_table: Mapped[list['ActiveDynamicTableORM']] = relationship(back_populates='aggregate_info')
    archive_dynamic_table: Mapped[list['ArchiveDynamicTableORM']] = relationship(back_populates='aggregate_info')


class AggregatesBaseORMMixin(Base):
    """Базовый класс для всех агрегатов"""
    __abstract__ = True

    aggregates_ptr_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('visual_aggregates.id', ondelete='CASCADE'),
        primary_key=True
    )

    @declared_attr
    def aggregate_info(self) -> Mapped['AggregatesORM']:
        return relationship('AggregatesORM')


class AggregatesGMPORM(AggregatesBaseORMMixin):
    """Модель агрегатов ГМП"""
    __tablename__ = 'visual_aggregatesgmp'
    routes: Mapped['RoutesORM'] = relationship(back_populates='aggregates_gmp')


class AggregatesUKPORM(AggregatesBaseORMMixin):
    """Модель агрегатов УКП"""
    __tablename__ = 'visual_aggregatesukp'
    routes: Mapped['RoutesORM'] = relationship(back_populates='aggregates_ukp')


class AggregatesUVSORM(AggregatesBaseORMMixin):
    """Модель агрегатов УВС"""
    __tablename__ = 'visual_aggregatesuvs'
    routes: Mapped['RoutesORM'] = relationship(back_populates='aggregates_uvs')


class AggregatesMNLZORM(AggregatesBaseORMMixin):
    """Модель агрегатов МНЛЗ"""
    __tablename__ = 'visual_aggregatesmnlz'
    routes: Mapped['RoutesORM'] = relationship(back_populates='aggregates_mnlz')


class AggregatesLORM(AggregatesBaseORMMixin):
    """Модель агрегатов Лёжек"""
    __tablename__ = 'visual_aggregatesl'
    routes: Mapped['RoutesORM'] = relationship(back_populates='aggregates_l')


class AggregatesBurnerORM(AggregatesBaseORMMixin):
    """Модель агрегатов Горелок"""
    __tablename__ = 'visual_aggregatesburner'
    routes: Mapped['RoutesORM'] = relationship(back_populates='aggregates_burner')
