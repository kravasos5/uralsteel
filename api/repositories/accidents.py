from pydantic import BaseModel
from sqlalchemy import insert, update

from models.accidents import LadlesAccidentORM, CranesAccidentORM, AggregatesAccidentORM
from models.aggregates import AggregatesORM
from models.cranes import CranesORM
from models.ladles import LadlesORM
from schemas.accidents import LadlesAccidentReadDTO, CranesAccidentReadDTO, AggregateAccidentReadDTO
from schemas.commons import DataConverter
from utils.repositories_base import SqlAlchemyRepo


class AccidentsRepoBase(SqlAlchemyRepo):
    """Базовый репозиторий для инцидентов"""
    model = None
    read_schema = None
    aggregate_model = None

    def create_one(self, data_schema: BaseModel):
        """Создание новой записи в бд"""
        data = DataConverter.dto_to_dict(data_schema)
        # нужно обновить статус крана, ковша или агрегата и отметить его как сломанный
        # извлекаю его id
        aggregate_id = data.get('object_id')
        stmt_object = update(self.aggregate_model).filter_by(id=aggregate_id).values(is_broken=True)
        self.session.execute(stmt_object)
        stmt = insert(self.model).values(**data).returning(self.model)
        res = self.session.execute(stmt).scalar_one()
        # конвертация данных
        result = DataConverter.model_to_dto(res, self.read_schema)
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
