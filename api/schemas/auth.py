from pydantic import BaseModel


class TokenInfo(BaseModel):
    """Схема токена"""
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenBlacklistCreateUpdateDTO(BaseModel):
    """Схема токена из чёрного списка"""
    refresh_token: str


class RefreshTokenBlacklistReadDTO(RefreshTokenBlacklistCreateUpdateDTO):
    """Схема токена из чёрного списка"""
    id: int


class RefreshTokenCreateUpdateDTO(BaseModel):
    """Схема refresh токена"""
    refresh_token: str
    employee_id: int


class RefreshTokenReadDTO(RefreshTokenCreateUpdateDTO):
    """Схема refresh токена"""
    id: int
