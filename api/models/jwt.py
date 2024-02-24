import uuid
from datetime import datetime

from sqlalchemy import String, BigInteger, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, idpk


class TokenBaseORM(Base):
    """Абстрактная модель для refresh токенов"""
    __abstract__ = True

    id: Mapped[idpk]
    refresh_token: Mapped[str] = mapped_column(
        String(1000),
        unique=True,
        nullable=False,
    )
    expire_date: Mapped[datetime]
    token_family: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )


class TokenORM(TokenBaseORM):
    __tablename__ = "jwt_refresh_tokens"

    employee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_employees.id'))

    employee: Mapped['EmployeesORM'] = relationship(
        back_populates='tokens'
    )


class TokenBlacklistORM(TokenBaseORM):
    __tablename__ = "jwt_blacklist"
