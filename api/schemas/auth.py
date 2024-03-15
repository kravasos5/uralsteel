import uuid
from datetime import datetime

from pydantic import BaseModel


class TokenInfo(BaseModel):
    """Схема токена"""
    access_token: str
    refresh_token: str
    token_type: str


class TokenScopesData(BaseModel):
    """Схема информации в токене"""
    id: int
    scopes: list[str] = []


class RefreshTokenBaseDTO(BaseModel):
    """Схема токена из чёрного списка"""
    refresh_token: str
    expire_date: datetime
    token_family: uuid.UUID

    class Config:
        from_attributes = True


class RefreshTokenBlacklistReadDTO(RefreshTokenBaseDTO):
    """Схема токена из чёрного списка"""
    id: int


class RefreshTokenCreateUpdateDTO(RefreshTokenBaseDTO):
    """Схема refresh токена"""
    employee_id: int


class RefreshTokenUpdatePatchDTO(BaseModel):
    """Схема обновления refresh токена методом patch"""
    refresh_token: str | None = None
    expire_date: datetime | None = None
    token_family: uuid.UUID | None = None
    employee_id: int | None = None


class RefreshTokenReadDTO(RefreshTokenCreateUpdateDTO):
    """Схема refresh токена"""
    id: int
    employee_id: int | None = None
