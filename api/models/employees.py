from enum import Enum

from sqlalchemy import Column, String, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship

from .commons import IdMixin


###################################################################
# Модели Employees(пользователя или же работника)
class Posts(str, Enum):
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
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(TIMESTAMP, nullable=False, server_default=func.now())
    send_messages = Column(Boolean, nullable=False, default=True)
    photo = Column(String, nullable=True)
    post = Column(Enum(Posts, name='posts_enum'), nullable=False, default=Posts.MECHANIC.value)
    slug = Column(String, unique=True, index=True)

    ladles_reports = relationship(
        'LadlesAccident',
        back_populates='author_info',
        uselist=True
    )
    cranes_reports = relationship(
        'CranesAccident',
        back_populates='author_info',
        uselist=True
    )
    aggregates_reports = relationship(
        'AggregatesAccident',
        back_populates='author_info',
        uselist=True
    )