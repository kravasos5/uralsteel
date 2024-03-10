import uuid

from sqlalchemy import select, insert, delete

from models.jwt import TokenBlacklistORM, TokenORM
from schemas.auth import RefreshTokenBlacklistReadDTO, RefreshTokenReadDTO, RefreshTokenBaseDTO
from schemas.commons import DataConverter
from utils.repositories_base import SqlAlchemyRepo


class RefreshTokenRepo(SqlAlchemyRepo):
    """Репозиторий для refresh токенов"""
    model = TokenORM
    blacklist_model = TokenBlacklistORM
    read_schema = RefreshTokenReadDTO

    async def transfer_token_family_to_blacklist(self, token_family: uuid.UUID | str):
        """Добавить семейство токенов в чёрный список"""
        subq = select(self.model.id).filter_by(token_family=token_family)
        stmt = (
            delete(self.model)
            .where(self.model.id.in_(subq))
            .returning(
                self.model.refresh_token,
                self.model.expire_date,
                self.model.token_family,
            )
        )
        res = await self.session.execute(stmt)
        res = res.all()
        if res:
            transfer_tokens = await DataConverter.list_to_dto(res, RefreshTokenBaseDTO)
            transfer_tokens_dict = await DataConverter.dtos_to_dict(transfer_tokens)
            return await self.transfer_to_blacklist(transfer_tokens_dict)
        return None

    async def transfer_to_blacklist(self, tokens: list[dict]):
        """Добавить токен или токены в blacklist"""
        stmt_insert = (
            insert(self.blacklist_model)
            .values(tokens)
            .returning(self.blacklist_model.id)
        )
        result = await self.session.execute(stmt_insert)
        result = result.scalars().all()
        return result


class RefreshTokenBlacklistRepo(SqlAlchemyRepo):
    """Репозиторий для refresh токенов из чёрного списка"""
    model = TokenBlacklistORM
    read_schema = RefreshTokenBlacklistReadDTO
