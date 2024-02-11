from sqlalchemy import Column, String, TIMESTAMP, func, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


###################################################################
# Модели проишествий
# class AccidentsUserMixin:
#     """Миксин, добавляющий отношение с Employees для проишествий"""
#     author_id = Column(BigInteger, ForeignKey('visual_employees.id'), nullable=False)
#
#     @declared_attr
#     def author_info(self):
#         return relationship('Employees', back_populates='reports', uselist=False)


class AccidentsMixin(Base):
    """Модель происшествий"""
    __abstract__ = True

    id = Column(BigInteger, primary_key=True)
    report = Column(String, default=None, nullable=True)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    author_id = Column(BigInteger, ForeignKey('visual_employees.id'), nullable=False)


class LadlesAccident(AccidentsMixin):
    """Модель происшествий ковшей"""
    __tablename__ = 'visual_ladlesaccident'

    object_id = Column(BigInteger, ForeignKey('visual_ladles.id'), nullable=True)

    object_info = relationship(
        'Ladles',
        back_populates='accidents'
    )

    author_info = relationship(
        'Employees',
        back_populates='ladles_reports',
        uselist=False
    )


class CranesAccident(AccidentsMixin):
    """Модель проишествий кранов"""
    __tablename__ = 'visual_cranesaccident'

    object_id = Column(BigInteger, ForeignKey('visual_cranes.id'), nullable=True)

    object_info = relationship(
        'Cranes',
        back_populates='accidents'
    )

    author_info = relationship(
        'Employees',
        back_populates='cranes_reports',
        uselist=False
    )


class AggregatesAccident(AccidentsMixin):
    """Модель проишествий агрегатов"""
    __tablename__ = 'visual_aggregataccident'

    object_id = Column(BigInteger, ForeignKey('visual_aggregates.id'), nullable=True)

    object_info = relationship(
        'Aggregates',
        back_populates='accidents'
    )

    author_info = relationship(
        'Employees',
        back_populates='aggregates_reports',
        uselist=False
    )
