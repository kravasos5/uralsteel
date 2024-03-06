from abc import ABC, abstractmethod

from pydantic import BaseModel

from utils.unitofwork import AbstractUnitOfWork


class AbstractService(ABC):
    """Абстрактный сервис"""
    repository = None

    @abstractmethod
    async def create_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def retrieve_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def retrieve_all(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, *args, **kwargs):
        raise NotImplementedError


class ServiceBase(AbstractService):
    """Базовый сервис"""
    repository = None

    async def create_one(self, uow: AbstractUnitOfWork, data_schema: BaseModel):
        """Создания одного объекта в БД"""
        async with uow:
            result = await uow.repositories[self.repository].create_one(data_schema=data_schema)
            await uow.commit()
            return result

    async def retrieve_one(self, uow: AbstractUnitOfWork, **filters):
        """Получение одного объекта из БД"""
        async with uow:
            result = await uow.repositories[self.repository].retrieve_one(**filters)
            return result

    async def retrieve_all(
        self,
        uow: AbstractUnitOfWork,
        offset: int = 0,
        limit: int = 100,
        **filters
    ):
        """Получение списка объектов из БД"""
        async with uow:
            result = await uow.repositories[self.repository].retrieve_all(offset=offset, limit=limit, **filters)
            return result

    async def delete_one(self, uow: AbstractUnitOfWork, **filters):
        """Удаление одного объекта в БД"""
        async with uow:
            result = await uow.repositories[self.repository].delete_one(**filters)
            await uow.commit()
            return result

    async def delete_by_ids(self, uow: AbstractUnitOfWork, ids: list[int]):
        """Удаление одного объекта в БД"""
        async with uow:
            result = await uow.repositories[self.repository].delete_by_ids(ids)
            await uow.commit()
            return result

    async def update_one(self, uow: AbstractUnitOfWork, data_schema: BaseModel, **filters):
        """Обновление одного объекта в БД"""
        async with uow:
            result = await uow.repositories[self.repository].update_one(data_schema=data_schema, **filters)
            await uow.commit()
            return result
