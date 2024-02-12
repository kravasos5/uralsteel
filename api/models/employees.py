from datetime import datetime
from enum import Enum

from sqlalchemy import String, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base, created_at, idpk


class Posts(str, Enum):
    """Enum, содержащий должности"""
    MASTER = 'MS'
    MECHANIC = 'MH'
    DISPATCHER = 'DT'


class EmployeesORM(Base):
    """Модель работника"""
    __tablename__ = "visual_employees"

    id: Mapped[idpk]
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(128))
    username: Mapped[str] = mapped_column(String(150))
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    patronymic: Mapped[str] = mapped_column(String(100), nullable=True)
    last_login: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    date_joined: Mapped[created_at]
    send_messages: Mapped[bool] = mapped_column(Boolean, default=True)
    photo: Mapped[str] = mapped_column(String(100), nullable=True)
    post: Mapped[Posts] = mapped_column(String(2), default=Posts.MECHANIC.value)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True)

    ladles_reports: Mapped[list['LadlesAccidentORM']] = relationship(
        back_populates='author_info'
    )
    cranes_reports: Mapped[list['CranesAccidentORM']] = relationship(
        back_populates='author_info'
    )
    aggregates_reports: Mapped[list['AggregatesAccidentORM']] = relationship(
        back_populates='author_info'
    )
