from sqlalchemy import Column, BigInteger

from ..database import Base


class IdMixin(Base):
    """Класс, добавляющий всем моделям поле id"""
    __abstract__ = True

    id = Column(BigInteger, primary_key=True)
