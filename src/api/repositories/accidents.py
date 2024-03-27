from typing import Type

from pydantic import BaseModel
from sqlalchemy import insert, update, select
from sqlalchemy.orm import joinedload

from models.accidents import LadlesAccidentORM, CranesAccidentORM, AggregatesAccidentORM
from models.aggregates import AggregatesORM
from models.cranes import CranesORM
from models.ladles import LadlesORM
from schemas.accidents import AccidentReadShortDTO, AccidentReadDTO, LadlesAccidentReadDTO, CranesAccidentReadDTO, \
    AggregateAccidentReadDTO
from schemas.commons import DataConverter
from utils.repositories_base import SqlAlchemyRepo


class AccidentsRepoBase(SqlAlchemyRepo):
    """Базовый репозиторий для инцидентов"""
    model = None
    # read_schema = AccidentReadDTO
    read_schema = None
    read_short_schema = AccidentReadShortDTO
    aggregate_model = None

    async def create_one(self, data_schema: BaseModel):
        """Создание новой записи в бд"""
        data = await DataConverter.dto_to_dict(data_schema)
        # нужно обновить статус крана, ковша или агрегата и отметить его как сломанный
        # извлекаю его id
        aggregate_id = data.get('object_id')
        stmt_object = update(self.aggregate_model).filter_by(id=aggregate_id).values(is_broken=True)
        await self.session.execute(stmt_object)
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        res = res.scalar_one()
        # конвертация данных
        result = await DataConverter.model_to_dto(res, self.read_short_schema)
        return result

    async def retrieve_one(self, read_schema: Type[BaseModel] | None = None, **filters):
        """Получение одной записи из бд"""
        stmt = (
            select(self.model)
            .options(
                joinedload(self.model.author_info),
                joinedload(self.model.object_info)
            )
            .filter_by(**filters)
        )
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
        stmt = (
            select(self.model)
            .options(
                joinedload(self.model.author_info),
                joinedload(self.model.object_info)
            )
            .filter_by(**filters)
            .offset(offset)
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        res = res.scalars().all()
        result = await DataConverter.models_to_dto(res, self.read_schema)
        return result


class LadlesAccidentRepo(AccidentsRepoBase):
    """Репозиторий происшествия с ковшом"""
    model = LadlesAccidentORM
    read_schema = LadlesAccidentReadDTO
    aggregate_model = LadlesORM


class CranesAccidentRepo(AccidentsRepoBase):
    """Репозиторий происшествия с краном"""
    model = CranesAccidentORM
    read_schema = CranesAccidentReadDTO
    aggregate_model = CranesORM


class AggregatesAccidentRepo(AccidentsRepoBase):
    """Репозиторий происшествия с агрегатом"""
    model = AggregatesAccidentORM
    read_schema = AggregateAccidentReadDTO
    aggregate_model = AggregatesORM
