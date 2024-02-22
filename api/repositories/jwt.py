from models.jwt import TokenBlacklistORM, TokenORM
from schemas.auth import RefreshTokenBlacklistReadDTO, RefreshTokenReadDTO
from utils.repositories_base import SqlAlchemyRepo


class RefreshTokenRepo(SqlAlchemyRepo):
    """Репозиторий для refresh токенов"""
    model = TokenORM
    read_schema = RefreshTokenReadDTO


class RefreshTokenBlacklistRepo(SqlAlchemyRepo):
    """Репозиторий для refresh токенов из чёрного списка"""
    model = TokenBlacklistORM
    read_schema = RefreshTokenBlacklistReadDTO
