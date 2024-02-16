from sqlalchemy import Column, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base, idpk, created_at


class AccidentsORMMixin(Base):
    """Модель происшествий"""
    __abstract__ = True

    id: Mapped[idpk]
    report: Mapped[str | None] = mapped_column(String(800), default=None, nullable=True)
    created_at: Mapped[created_at]
    author_id: Mapped[int] = Column(BigInteger, ForeignKey('visual_employees.id'))


class LadlesAccidentORM(AccidentsORMMixin):
    """Модель происшествий ковшей"""
    __tablename__ = 'visual_ladlesaccident'

    object_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('visual_ladles.id'), nullable=True)

    object_info: Mapped['LadlesORM'] = relationship(
        back_populates='accidents'
    )

    author_info: Mapped['EmployeesORM'] = relationship(
        back_populates='ladles_reports'
    )


class CranesAccidentORM(AccidentsORMMixin):
    """Модель происшествий кранов"""
    __tablename__ = 'visual_cranesaccident'

    object_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('visual_cranes.id'), nullable=True)

    object_info: Mapped['CranesORM'] = relationship(
        back_populates='accidents'
    )

    author_info: Mapped['EmployeesORM'] = relationship(
        back_populates='cranes_reports'
    )


class AggregatesAccidentORM(AccidentsORMMixin):
    """Модель происшествий агрегатов"""
    __tablename__ = 'visual_aggregateaccident'

    object_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('visual_aggregates.id'), nullable=True)

    object_info: Mapped['AggregatesORM'] = relationship(
        back_populates='accidents'
    )

    author_info: Mapped['EmployeesORM'] = relationship(
        back_populates='aggregates_reports'
    )
