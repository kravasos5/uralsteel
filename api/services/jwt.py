import uuid

from schemas.auth import RefreshTokenBaseDTO
from utils.service_base import ServiceBase
from utils.unitofwork import AbstractUnitOfWork


class RefreshTokenService(ServiceBase):
    """Сервис для работы с refresh токенами"""
    repository = 'refresh_token_repo'
    blacklist_repository = 'refresh_token_bl_repo'

    def transfer_to_blacklist(
        self,
        uow: AbstractUnitOfWork,
        refresh_token: str,
        employee_id: int,
        token_family: uuid.UUID | str,
    ):
        """Перенести токен в чёрный список"""
        # получаю токен, который нужно занести в blacklist
        curr_token = self.retrieve_one(
            uow,
            employee_id=employee_id,
            token_family=token_family,
            refresh_token=refresh_token
        )
        # получаю dto для токена в чёрном списке
        create_bl_dto = RefreshTokenBaseDTO(
            refresh_token=curr_token.refresh_token,
            expire_date=curr_token.expire_date,
            token_family=curr_token.token_family
        )
        # заношу этот токен в чёрный список
        uow.repositories[self.blacklist_repository].create_one(uow, create_bl_dto)
        # удаляю токен из бд
        self.delete_one(
            uow,
            employee_id=employee_id,
            token_family=token_family,
            refresh_token=refresh_token
        )

    def delete_family(self, token_family: uuid.UUID | str):
        """Удалить семейство токенов"""
        ...

    def check_token(
        self,
        uow: AbstractUnitOfWork,
        token: str,
        token_family: uuid.UUID | str,
    ):
        """Проверка есть ли такой токен в blacklist"""
        if uow.repositories[self.blacklist_repository].retrieve_one(
            refresh_token=token,
            token_family=token_family
        ):
            ...


class RefreshTokenBlacklistService(ServiceBase):
    """Сервис для работы с blacklist refresh токенами"""
    repository = 'refresh_token_bl_repo'
