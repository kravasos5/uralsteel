from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base, idpk


class RoutesORM(Base):
    """Модель маршрутов"""
    __tablename__ = 'visual_routes'

    id: Mapped[idpk]
    aggregate_1_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_aggregatesgmp.aggregates_ptr_id'))
    aggregate_2_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_aggregatesukp.aggregates_ptr_id'))
    aggregate_3_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_aggregatesuvs.aggregates_ptr_id'))
    aggregate_4_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_aggregatesmnlz.aggregates_ptr_id'))

    aggregates_gmp: Mapped[list['AggregatesGMPORM']] = relationship(back_populates='routes')
    aggregates_ukp: Mapped[list['AggregatesUKPORM']] = relationship(back_populates='routes')
    aggregates_uvs: Mapped[list['AggregatesUVSORM']] = relationship(back_populates='routes')
    aggregates_mnlz: Mapped[list['AggregatesMNLZORM']] = relationship(back_populates='routes')
    # aggregates_l: Mapped[list['AggregatesLORM']] = relationship(back_populates='routes')
    # aggregates_burner: Mapped[list['AggregatesBurnerORM']] = relationship(back_populates='routes')
    active_dynamic_table: Mapped[list['ActiveDynamicTableORM']] = relationship(back_populates='route_info')
    archive_dynamic_table: Mapped[list['ArchiveDynamicTableORM']] = relationship(back_populates='route_info')
