from abc import ABC, abstractmethod
from typing import Type

import redis
from redis.commands.json.path import Path
from pydantic import BaseModel
from sqlalchemy import insert, delete, update, select
from sqlalchemy.orm import Session

from config import settings
from schemas.commons import DataConverter


class AbstractRepo(ABC):
    """Абстрактный репозиторий"""

    @abstractmethod
    async def create_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_ids(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def retrieve_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def retrieve_all(self, *args, **kwargs):
        raise NotImplementedError


class SqlAlchemyRepo(AbstractRepo):
    """Класс SqlAlchemy репозитория"""
    model = None
    read_schema = None

    def __init__(self, session: Session):
        self.session = session

    async def create_one(self, data_schema: BaseModel):
        """Создание новой записи в бд"""
        data = await DataConverter.dto_to_dict(data_schema)
        # запрос
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        res = res.scalar_one()
        # конвертация данных
        result = await DataConverter.model_to_dto(res, self.read_schema)
        return result

    async def delete_one(self, **filters):
        """Удаление записи из бд"""
        # запрос
        stmt = delete(self.model).filter_by(**filters).returning(self.model.id)
        result = await self.session.execute(stmt)
        result = result.scalar_one_or_none()
        if result:
            return result
        return None

    async def delete_by_ids(self, ids: list[int]):
        """Удаление записи из бд"""
        # запрос
        stmt = delete(self.model).where(self.model.id.in_(ids)).returning(self.model.id)
        result = await self.session.execute(stmt)
        result = result.scalars().all()
        if result:
            return result
        return None

    async def update_one(self, data_schema: BaseModel, **filters):
        """Обновление записи в бд"""
        data = await DataConverter.dto_to_dict(data_schema, exclude_unset=True)
        # запрос
        stmt = update(self.model).filter_by(**filters).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if res:
            result = await DataConverter.model_to_dto(res, self.read_schema)
            return result
        return res

    async def retrieve_one(self, read_schema: Type[BaseModel] | None = None, **filters):
        """Получение одной записи из бд"""
        stmt = select(self.model).filter_by(**filters)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if res:
            if read_schema is not None:
                read_schema = read_schema
            else:
                read_schema = self.read_schema
            result = await DataConverter.model_to_dto(res, read_schema)
            return result
        return res

    async def retrieve_all(self, offset: int = 0, limit: int = 100, **filters):
        """Получение списка записей из бд"""
        stmt = select(self.model).filter_by(**filters).offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        res = res.scalars().all()
        result = await DataConverter.models_to_dto(res, self.read_schema)
        return result


class AbstractRedisRepo(ABC):
    """Абстрактный репозиторий redis-кэша"""

    @abstractmethod
    def get_key_redis_json(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def set_key_redis_json(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_key_redis(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def set_key_redis(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete_key_redis(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete_keys_redis(self, *args, **kwargs):
        raise NotImplementedError


class RedisRepo(AbstractRedisRepo):
    """Репозиторий для работы с Redis-хранилищем"""

    @staticmethod
    def get_key_redis_json(key_name: str) -> dict | None:
        """
        Функция, извлекающая ключ из redis, если такого ключа нет,
        то вернёт None. Работает только с json
        """
        with redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT) as redis_client:
            result = redis_client.json().get(key_name)
        if result is not None:
            return result

    @staticmethod
    def set_key_redis_json(key_name: str, data: dict, ttl: int) -> None:
        """Функция, задающая ключ в храниилище. Работает только с json"""
        with redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT) as redis_client:
            # сохраняю ключ и данные
            redis_client.json().set(key_name, Path.root_path(), data)
            # даю время жизни кэшу ttl секунд
            redis_client.expire(key_name, ttl)

    @staticmethod
    def get_key_redis(key_name: str) -> str | None:
        """
        Функция, извлекающая ключ из redis, если такого ключа нет,
        то вернёт None
        """
        with redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT) as redis_client:
            result: bytes = redis_client.get(key_name)
        if result is not None:
            return result.decode()

    @staticmethod
    def set_key_redis(key_name: str, data: str, ttl: int) -> None:
        """Функция, задающая ключ в хранилище"""
        with redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT) as redis_client:
            # сохраняю ключ и данные
            redis_client.set(key_name, data)
            # даю время жизни кэшу ttl секунд
            redis_client.expire(key_name, ttl)

    @staticmethod
    def delete_key_redis(key_name: str) -> None:
        """Функция, удаляющая ключ из хранилища"""
        with redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT) as redis_client:
            # удаляю ключ
            redis_client.delete(key_name)

    @staticmethod
    def delete_keys_redis(pattern: str) -> None:
        """Функция, удаляющая ключи из хранилища по паттерну"""
        with redis.Redis() as redis_client:
            # получаю все ключи по паттерну
            all_keys: list = redis_client.keys(pattern)
            for key in all_keys:
                # удаляю ключ
                redis_client.delete(key)
