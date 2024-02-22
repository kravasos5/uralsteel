from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, idpk


class TokenORM(Base):
    __tablename__ = "jwt_refresh_tokens"

    id: Mapped[idpk]
    refresh_token: Mapped[str] = mapped_column(String(1000), unique=True)
    employee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('visual_employees.id'))

    employee: Mapped['EmployeesORM'] = relationship(
        back_populates='tokens'
    )


class TokenBlacklistORM(Base):
    __tablename__ = "jwt_blacklist"

    id: Mapped[idpk]
    refresh_token: Mapped[str] = mapped_column(String(1000), unique=True)
