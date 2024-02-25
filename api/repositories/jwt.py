import uuid

from sqlalchemy import select, insert

from models.jwt import TokenBlacklistORM, TokenORM
from schemas.auth import RefreshTokenBlacklistReadDTO, RefreshTokenReadDTO, RefreshTokenBaseDTO
from schemas.commons import DataConverter
from utils.repositories_base import SqlAlchemyRepo


class RefreshTokenRepo(SqlAlchemyRepo):
    """Репозиторий для refresh токенов"""
    model = TokenORM
    blacklist_model = TokenBlacklistORM
    read_schema = RefreshTokenReadDTO

    def retrieve_token_family(self, token_family: uuid.UUID | str):
        """Получить семейство токенов"""
        subq = select(self.model).filter_by(token_family=token_family)
        res = self.session.execute(subq).scalars().all()
        t = DataConverter.models_to_dto(res, RefreshTokenBaseDTO)
        tokens = DataConverter.dtos_to_dict(t)
        stmt = insert(self.blacklist_model).values(tokens)
        ...


class RefreshTokenBlacklistRepo(SqlAlchemyRepo):
    """Репозиторий для refresh токенов из чёрного списка"""
    model = TokenBlacklistORM
    read_schema = RefreshTokenBlacklistReadDTO
