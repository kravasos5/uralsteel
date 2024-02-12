from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base, idpk


class RoutesORM(Base):
    """Модель маршрутов"""
    __tablename__ = 'visual_routes'

    id: Mapped[idpk]
    aggregate_1: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_aggregatesgmp.id'))
    aggregate_2: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_aggregatesukp.id'))
    aggregate_3: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_aggregatesuvs.id'))
    aggregate_4: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_aggregatesmnlz.id'))

    aggregate_gmp: Mapped['AggregatesGMPORM'] = relationship(back_populates='routes')
    aggregate_ukp: Mapped['AggregatesUKPORM'] = relationship(back_populates='routes')
    aggregate_uvs: Mapped['AggregatesUVSORM'] = relationship(back_populates='routes')
    aggregate_mnlz: Mapped['AggregatesMNLZORM'] = relationship(back_populates='routes')
    active_dynamic_table: Mapped[list['ActiveDynamicTableORM']] = relationship(back_populates='route_info')
    archive_dynamic_table: Mapped[list['ArchiveDynamicTableORM']] = relationship(back_populates='route_info')
