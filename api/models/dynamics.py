from datetime import datetime

from sqlalchemy import String, TIMESTAMP, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, declared_attr, Mapped, mapped_column

from database import Base, idpk


class DynamicTableORMMixin(Base):
    """Основная таблица с информацией о перемещении ковшей в реальном времени"""
    __abstract__ = True

    id: Mapped[idpk]
    ladle_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_ladles.id'))
    num_melt: Mapped[str] = mapped_column(String)
    brand_steel_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_brandsteel.id'))
    route_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_routes.id'))
    aggregate_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_aggregates.id'))
    plan_start: Mapped[datetime] = mapped_column(TIMESTAMP)
    plan_end: Mapped[datetime] = mapped_column(TIMESTAMP)
    actual_start: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    actual_end: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)

    @declared_attr
    def ladle_info(self) -> Mapped['LadlesORM']:
        return relationship('LadlesORM')

    @declared_attr
    def brand_steel_info(self) -> Mapped['BrandSteelORM']:
        return relationship('BrandSteelORM')

    @declared_attr
    def route_info(self) -> Mapped['RoutesORM']:
        return relationship('RoutesORM')

    @declared_attr
    def aggregate_info(self) -> Mapped['AggregatesORM']:
        return relationship('AggregatesORM')


class ArchiveDynamicTableORM(DynamicTableORMMixin):
    """Модель архивных записей динамической таблицы"""
    __tablename__ = 'visual_archivedynamictable'


class ActiveDynamicTableORM(DynamicTableORMMixin):
    """Модель активных записей динамической таблицы"""
    __tablename__ = 'visual_activedynamictable'
