from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy import insert, delete, update, select
from sqlalchemy.orm import Session

from schemas.commons import DataConverter


class AbstractRepo(ABC):
    """Абстрактный репозиторий"""

    @abstractmethod
    def create_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def retrieve_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def retrieve_all(self, *args, **kwargs):
        raise NotImplementedError


class SqlAlchemyRepo(AbstractRepo):
    """Класс SqlAlchemy репозитория"""
    model = None
    read_schema = None

    def __init__(self, session: Session):
        self.session = session

    def create_one(self, data_schema: BaseModel):
        """Создание новой записи в бд"""
        data = DataConverter.dto_to_dict(data_schema)
        # запрос
        stmt = insert(self.model).values(**data).returning(self.model)
        res = self.session.execute(stmt).scalar_one()
        # конвертация данных
        result = DataConverter.model_to_dto(res, self.read_schema)
        return result

    def delete_one(self, **filters):
        """Удаление записи из бд"""
        # запрос
        stmt = delete(self.model).filter_by(**filters).returning(self.model.id)
        result = self.session.execute(stmt).scalar_one()[0]
        return result

    def update_one(self, data_schema: BaseModel, **filters):
        """Обновление записи в бд"""
        data = DataConverter.dto_to_dict(data_schema)
        # запрос
        stmt = update(self.model).filter_by(**filters).values(**data).returning(self.model)
        res = self.session.execute(stmt).scalar_one()
        result = DataConverter.model_to_dto(res, self.read_schema)
        return result

    def retrieve_one(self, **filters):
        """Получение одной записи из бд"""
        stmt = select(self.model).filter_by(**filters)
        res = self.session.execute(stmt).scalar_one()
        result = DataConverter.model_to_dto(res, self.read_schema)
        return result

    def retrieve_all(self, offset: int, limit: int, **filters):
        """Получение списка записей из бд"""
        stmt = select(self.model).filter_by(**filters).offset(offset).limit(limit)
        res = self.session.execute(stmt).scalars().all()
        result = DataConverter.models_to_dto(res, self.read_schema)
        return result


class AbstractRedisRepo(ABC):
    """Абстрактный репозиторий redis-кэша"""
    ...
