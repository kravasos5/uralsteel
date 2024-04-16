import uuid

from utils.service_base import ServiceBase
from utils.unitofwork import AbstractUnitOfWork


class RefreshTokenService(ServiceBase):
    """Сервис для работы с refresh токенами"""
    repository = 'refresh_token_repo'
    blacklist_repository = 'refresh_token_bl_repo'

    async def transfer_to_blacklist(
        self,
        uow: AbstractUnitOfWork,
        refresh_token: str,
        employee_id: int,
        token_family: uuid.UUID | str,
    ):
        """Перенести токен в чёрный список"""
        async with uow:
            # получаю токен, который нужно занести в blacklist
            curr_token = await self.retrieve_one(
                uow,
                employee_id=employee_id,
                token_family=token_family,
                refresh_token=refresh_token
            )
            # получаю dict для токена в чёрном списке
            create_bl = dict(
                refresh_token=curr_token.refresh_token,
                expire_date=curr_token.expire_date,
                token_family=curr_token.token_family
            )
            # заношу этот токен в чёрный список
            await uow.repositories[self.repository].transfer_to_blacklist([create_bl])
            await uow.commit()
            # удаляю токен из бд
            await self.delete_one(
                uow,
                employee_id=curr_token.employee_id,
                token_family=curr_token.token_family,
                refresh_token=curr_token.refresh_token,
            )

    async def delete_family(self, uow: AbstractUnitOfWork, token_family: uuid.UUID | str):
        """Удалить семейство токенов"""
        async with uow:
            result = await uow.repositories[self.repository] \
                .transfer_token_family_to_blacklist(token_family=token_family)
            await uow.commit()
            return result

    async def check_token(
        self,
        uow: AbstractUnitOfWork,
        token: str,
        token_family: uuid.UUID | str,
    ):
        """Проверка есть ли такой токен в blacklist"""
        async with uow:
            if await uow.repositories[self.blacklist_repository].retrieve_one(
                refresh_token=token,
                token_family=token_family
            ):
                return True
            return False


class RefreshTokenBlacklistService(ServiceBase):
    """Сервис для работы с blacklist refresh токенами"""
    repository = 'refresh_token_bl_repo'
