from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

from database import Base


class AbstractDataConverter(ABC):
    """Абстрактный класс, содержащий методы конвертации данных"""

    @abstractmethod
    @staticmethod
    def model_to_dto(model, schema):
        """Метод, конвертирующий модели или словари в dto"""
        raise NotImplementedError

    @abstractmethod
    @staticmethod
    def models_to_dto(models, schema):
        """Метод, конвертирующий модели или словари в dto"""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def dto_to_dict(schema) -> dict:
        """Метод, конвертирующий dto в словарь"""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def dtos_to_dict(schemas) -> list[dict]:
        """Метод, конвертирующий dtos в список словарей"""
        raise NotImplementedError


class DataConverter(AbstractDataConverter):
    """Класс, содержащий методы конвертации данных"""

    @staticmethod
    def model_to_dto(model: Base | dict, schema: Type[BaseModel]) -> BaseModel:
        """Метод, конвертирующий модели или словари в dto"""
        dto = schema.model_validate(model, from_attributes=True)
        return dto

    @staticmethod
    def models_to_dto(models: list[Base] | list[dict], schema: Type[BaseModel]) -> list[BaseModel]:
        """Метод, конвертирующий модели или словари в dto"""
        dtos = [schema.model_validate(row, from_attributes=True) for row in models]
        return dtos

    @staticmethod
    def dto_to_dict(schema: BaseModel) -> dict:
        """Метод, конвертирующий dto в словарь"""
        return schema.model_dump()

    @staticmethod
    def dtos_to_dict(schemas: list[BaseModel]) -> list[dict]:
        """Метод, конвертирующий dtos в список словарей"""
        return [schema.model_dump() for schema in schemas]
