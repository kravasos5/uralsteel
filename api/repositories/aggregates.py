from pydantic import BaseModel
from sqlalchemy import select, update, delete, insert

from models.aggregates import AggregatesGMPORM, AggregatesUKPORM, AggregatesUVSORM, AggregatesMNLZORM, AggregatesLORM, \
    AggregatesBurnerORM, AggregatesORM
from schemas.aggregates import AggregatesReadDTO
from schemas.commons import DataConverter
from utils.repositories_base import SqlAlchemyRepo


class AggregatesAllRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов"""
    model = AggregatesORM
    read_schema = AggregatesReadDTO


class AggregatesUtilityRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов НЕ из таблицы visual_aggregates"""
    main_model = AggregatesORM
    model = None
    read_schema = AggregatesReadDTO

    def create_one(self, data_schema: BaseModel):
        """Создание новой записи в бд"""
        data = DataConverter.dto_to_dict(data_schema)
        # первый запрос занесёт данные в таблицу visual_aggregates
        stmt = insert(self.main_model).values(**data).returning(self.main_model)
        # получаю результат для формирования ответа и внесения данных в таблицу
        # visual_aggregates_<directly_aggregate>
        res = self.session.execute(stmt).scalar_one()
        # вношу данные в связанную таблицу visual_aggregates_<directly_aggregate>
        second_stmt = insert(self.model).values(aggregates_ptr_id=res[0].id)
        # выполняю запрос
        self.session.execute(second_stmt)
        # конвертация данных
        result = DataConverter.model_to_dto(res, self.read_schema)
        return result

    def delete_one(self, **filters):
        """Удаление записи из бд"""
        # запрос
        stmt = delete(self.main_model).filter_by(**filters).returning(self.main_model.id)
        result = self.session.execute(stmt).scalar_one()[0]
        # также нужно удалить эту информации из связанной таблицы
        # visual_aggregates_<directly_aggregate>
        second_stmt = delete(self.model).filter_by(aggregates_ptr_id=result)
        self.session.execute(second_stmt)
        return result

    def update_one(self, data_schema: BaseModel, **filters):
        """Обновление записи в бд"""
        data = DataConverter.dto_to_dict(data_schema)
        # запрос
        stmt = update(self.main_model).filter_by(**filters).values(**data).returning(self.main_model)
        res = self.session.execute(stmt).scalar_one()
        result = DataConverter.model_to_dto(res, self.read_schema)
        return result

    def retrieve_one(self, **filters):
        """Получение одной записи из бд"""
        stmt = select(self.main_model).filter_by(**filters)
        res = self.session.execute(stmt).scalar_one()
        result = DataConverter.model_to_dto(res, self.read_schema)
        return result

    def retrieve_all(self, offset: int, limit: int, **filters):
        """Получение списка записей из бд"""
        stmt = (
            select(self.model)
            .join(self.main_model, self.main_model.id == self.model.aggregates_ptr_id)
            .filter_by(**filters)
            .offset(offset)
            .limit(limit)
        )
        res = self.session.execute(stmt).scalars().all()
        result = DataConverter.models_to_dto(res, self.read_schema)
        return result


class AggregatesGMPRepo(AggregatesUtilityRepo):
    """Репозиторий агрегатов ГМП"""
    model = AggregatesGMPORM


class AggregatesUKPRepo(AggregatesUtilityRepo):
    """Репозиторий агрегатов УКП"""
    model = AggregatesUKPORM


class AggregatesUVSRepo(AggregatesUtilityRepo):
    """Репозиторий агрегатов УВС"""
    model = AggregatesUVSORM


class AggregatesMNLZRepo(AggregatesUtilityRepo):
    """Репозиторий агрегатов МНЛЗ"""
    model = AggregatesMNLZORM


class AggregatesLRepo(AggregatesUtilityRepo):
    """Репозиторий агрегатов Лёжек"""
    model = AggregatesLORM


class AggregatesBurnerRepo(AggregatesUtilityRepo):
    """Репозиторий агрегатов Горелок"""
    model = AggregatesBurnerORM

