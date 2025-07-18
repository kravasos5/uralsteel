from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

from database import Base


class AbstractDataConverter(ABC):
    """Абстрактный класс, содержащий методы конвертации данных"""

    @staticmethod
    @abstractmethod
    async def model_to_dto(model, schema):
        """Метод, конвертирующий модели или словари в dto"""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def models_to_dto(models, schema):
        """Метод, конвертирующий модели или словари в dto"""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def dto_to_dict(schema) -> dict:
        """Метод, конвертирующий dto в словарь"""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def dtos_to_dict(schemas) -> list[dict]:
        """Метод, конвертирующий dtos в список словарей"""
        raise NotImplementedError


class DataConverter(AbstractDataConverter):
    """Класс, содержащий методы конвертации данных"""

    @staticmethod
    async def model_to_dto(model: Base | dict, schema: Type[BaseModel]) -> BaseModel:
        """Метод, конвертирующий модели или словари в dto"""
        dto = schema.model_validate(model, from_attributes=True)
        return dto

    @staticmethod
    async def models_to_dto(models, schema: Type[BaseModel]) -> list[BaseModel]:
        """Метод, конвертирующий модели или словари в dto"""
        dtos = [schema.model_validate(row, from_attributes=True) for row in models]
        return dtos

    @staticmethod
    async def list_to_dto(list_data, schema: Type[BaseModel]) -> list[BaseModel]:
        """Конвертация списка кортежей в dto"""
        return [schema.model_validate(dict(zip(schema.model_fields, row))) for row in list_data]

    @staticmethod
    async def dto_to_dict(schema: BaseModel, exclude_unset: bool = False) -> dict:
        """Метод, конвертирующий dto в словарь"""
        return schema.model_dump(exclude_unset=exclude_unset)

    @staticmethod
    async def dtos_to_dict(schemas: list[BaseModel], exclude_unset: bool = False) -> list[dict]:
        """Метод, конвертирующий dtos в список словарей"""
        return [schema.model_dump(exclude_unset=exclude_unset) for schema in schemas]
