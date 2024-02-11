from abc import ABC, abstractmethod

from sqlalchemy import insert, delete, update, select
from sqlalchemy.orm import Session


class AbstractRepo(ABC):
    """Абстрактный репозиторий"""

    @abstractmethod
    def create_one(self):
        raise NotImplementedError

    @abstractmethod
    def delete_one(self):
        raise NotImplementedError

    @abstractmethod
    def update_one(self):
        raise NotImplementedError

    @abstractmethod
    def retrieve_one(self):
        raise NotImplementedError

    @abstractmethod
    def retrieve_all(self):
        raise NotImplementedError


class SqlAlchemyRepo(AbstractRepo):
    """Класс SqlAlchemy репозитория"""
    model = None

    def __init__(self, session: Session):
        self.session = session

    def create_one(self, data: dict):
        """Comment"""
        stmt = insert(self.model).values(**data).returning(self.model.id)
        result = self.session.execute(stmt).scalar_one()
        return result

    def delete_one(self, obj_id: int):
        """Comment"""
        stmt = delete(self.model).where(self.model.id == obj_id).returning(self.model.id)
        result = self.session.execute(stmt).scalar_one()
        return result

    def update_one(self, obj_id: int, data: dict):
        """Comment"""
        stmt = update(self.model).where(self.model.id == obj_id).values(**data).returning(self.model)
        result = self.session.execute(stmt).scalar_one()
        return result

    def retrieve_one(self, obj_id: int):
        """Comment"""
        stmt = select(self.model).where(self.model.id == obj_id).returning(self.model)
        result = self.session.execute(stmt).scalar_one()
        return result

    def retrieve_all(self, limit: int, offset: int):
        """Comment"""
        stmt = select(self.model).offset(offset).limit(limit).returning(self.model)
        result = self.session.execute(stmt).scalars().all()
        return result


class AbstractRedisRepo(ABC):
    """Абстрактный репозиторий redis-кэша"""
    ...
