from abc import ABC, abstractmethod

from pydantic import BaseModel

from utils.unitofwork import AbstractUnitOfWork


class AbstractService(ABC):
    """Абстрактный сервис"""
    repository = None

    @abstractmethod
    def create_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def retrieve_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def retrieve_all(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update_one(self, *args, **kwargs):
        raise NotImplementedError


class ServiceBase(AbstractService):
    """Базовый сервис"""
    repository = None

    def create_one(self, uow: AbstractUnitOfWork, data_schema: BaseModel):
        """Создания одного объекта в БД"""
        with uow:
            result = uow.repositories[self.repository].create_one(data_schema=data_schema)
            uow.commit()
            return result

    def retrieve_one(self, uow: AbstractUnitOfWork, **filters):
        """Получение одного объекта из БД"""
        with uow:
            result = uow.repositories[self.repository].retrieve_one(**filters)
            return result

    def retrieve_all(
        self,
        uow: AbstractUnitOfWork,
        offset: int = 0,
        limit: int = 100,
        **filters
    ):
        """Получение списка объектов из БД"""
        with uow:
            result = uow.repositories[self.repository].retrieve_all(offset=offset, limit=limit, **filters)
            return result

    def delete_one(self, uow: AbstractUnitOfWork, data_schema: BaseModel, **filters):
        """Удаление одного объекта в БД"""
        with uow:
            result = uow.repositories[self.repository].delete_one(**filters)
            uow.commit()
            return result

    def update_one(self, uow: AbstractUnitOfWork, data_schema: BaseModel, **filters):
        """Обновление одного объекта в БД"""
        with uow:
            result = uow.repositories[self.repository].update_one(data_schema=data_schema, **filters)
            uow.commit()
            return result
