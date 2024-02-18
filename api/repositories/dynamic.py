from datetime import datetime

import pytz
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from config import settings
from models.dynamics import ArchiveDynamicTableORM, ActiveDynamicTableORM
from schemas.commons import DataConverter
from schemas.dynamics import DynamicTableReadDTO, DynamicTableCreateUpdateDTO
from utils.repositories_base import SqlAlchemyRepo


class ArchiveDynamicTableRepo(SqlAlchemyRepo):
    """Репозиторий архивных записей динамической таблицы"""
    model = ArchiveDynamicTableORM
    read_schema = DynamicTableReadDTO


class ActiveDynamicTableRepo(SqlAlchemyRepo):
    """Репозиторий активных записей динамической таблицы"""
    model = ActiveDynamicTableORM
    read_schema = DynamicTableReadDTO
    create_schema = DynamicTableCreateUpdateDTO

    def convert_to_create_schema(self, read_data_schema: BaseModel):
        """Перевести информацию из схемы чтения в схему создания"""
        read_data_dict = DataConverter.dto_to_dict(read_data_schema)
        create_schema = DataConverter.model_to_dto(read_data_dict, self.create_schema)
        return create_schema

    def retrieve_transporting(self, date: datetime, ladles_info: dict, deletion_ids: list[int]):
        """Получить транспортируемые ковши"""
        stmt = (
            select(self.model)
            .options(joinedload(self.model.ladle_info),
                     joinedload(self.model.brand_steel_info),
                     joinedload(self.model.aggregate_info))
            .filter(self.model.actual_start.isnot(None),
                    self.model.actual_end.isnot(None),
                    self.model.actual_start <= date)
        )
        ladles_queryset = self.session.execute(stmt).scalars().all()
        ladles_info, deletion_ids = self.ladles_into_dict(
            ladles_queryset=ladles_queryset,
            ladles_info=ladles_info,
            is_transporting=True,
            deletion_ids=deletion_ids
        )
        return ladles_info, deletion_ids

    def retrieve_waiting(self, date: datetime, ladles_info: dict, deletion_ids: list[int]):
        """Получить ожидающие ковши"""
        stmt = (
            select(self.model)
            .options(joinedload(self.model.ladle_info),
                     joinedload(self.model.brand_steel_info),
                     joinedload(self.model.aggregate_info))
            .filter(self.model.actual_start.isnot(None),
                    self.model.actual_end.is_(None),
                    self.model.actual_start <= date)
        )
        ladles_queryset = self.session.execute(stmt).scalars().all()
        ladles_info, deletion_ids = self.ladles_into_dict(
            ladles_queryset=ladles_queryset,
            ladles_info=ladles_info,
            deletion_ids=deletion_ids,
            is_plan=True
        )
        return ladles_info, deletion_ids

    def retrieve_starting(self, date: datetime, ladles_info: dict, deletion_ids: list[int]):
        """Получить начинающие ковши"""
        stmt = (
            select(self.model)
            .options(joinedload(self.model.ladle_info),
                     joinedload(self.model.brand_steel_info),
                     joinedload(self.model.aggregate_info))
            .filter(self.model.actual_start.is_(None),
                    self.model.actual_end.is_(None),
                    self.model.plan_start < date,
                    self.model.plan_end > date)
        )
        ladles_queryset = self.session.execute(stmt).scalars().all()
        ladles_info, deletion_ids = self.ladles_into_dict(
            ladles_queryset=ladles_queryset,
            ladles_info=ladles_info,
            deletion_ids=deletion_ids
        )
        return ladles_info, deletion_ids

    def ladles_into_dict(
            self,
            ladles_queryset,
            ladles_info: dict,
            deletion_ids: list[int],
            is_transporting: bool = False,
            is_plan: bool = False,
    ) -> (dict, list):
        """
        Метод, преобразующий queryset ковшей в dict.
        Этот метод создаёт единый фундамент для всех видов
        ковшей, передаваемых фронту. Преобразование проходит с использованием sqlalchemy
        """
        for elem in ladles_queryset:
            if str(elem.ladle_info.id) in ladles_info:
                continue
            ladles_info[f'{elem.ladle_info.id}'] = {
                'ladle_title': f'{elem.ladle_info.title}',
                'x': elem.aggregate_info.coord_x,
                'y': elem.aggregate_info.coord_y,
                'num_melt': f'{elem.num_melt}',
                'brand_steel': f'{elem.brand_steel_info.title}',
                'aggregate': f'{elem.aggregate_info.title}',
                'plan_start': f'{elem.plan_start.astimezone(pytz.timezone(settings.TIME_ZONE))}',
                'plan_end': f'{elem.plan_end.astimezone(pytz.timezone(settings.TIME_ZONE))}',
                'next_aggregate': '-',
                'next_plan_start': '-',
                'next_plan_end': '-',
                'operation_id': elem.id
            }
            if is_transporting:
                # если ковш едет на следующую позицию, то есть
                # он "транспортируемый", то is_transporting=True
                ladles_info[f'{elem.ladle_info.id}']['is_transporting'] = True
            else:
                ladles_info[f'{elem.ladle_info.id}']['is_transporting'] = False

            if is_plan:
                # для "начинающих" ковшей
                ladles_info[f'{elem.ladle_info.id}']['photo'] = '/media/photos/aggregates/starting_ladle.png'
                ladles_info[f'{elem.ladle_info.id}']['is_starting'] = True
            else:
                # для "транспортируемых" и "ожидающих"
                ladles_info[f'{elem.ladle_info.id}']['photo'] = f'{elem.aggregate_info.photo}'
                ladles_info[f'{elem.ladle_info.id}']['is_starting'] = False

            # нахожу следующую позицию текущего ковша в БД
            next_elems_stmt = (
                select(self.model)
                .options(joinedload(self.model.aggregate_info))
                .filter(self.model.ladle_id == elem.ladle_id,
                        self.model.route_id == elem.route_id,
                        self.model.brand_steel_id == elem.brand_steel_id,
                        self.model.num_melt == elem.num_melt,
                        self.model.plan_start > elem.plan_end)
                .order_by(self.model.plan_start)
            )
            next_elems = self.session.execute(next_elems_stmt).scalars().all()
            # если следующая позиция присутствует, то обновляю
            # соответствующие поля словаря
            if next_elems:
                # получаю следующую позицию ковша
                # это первый элемент next_elems, так как next_elems
                # отсортирован по plan_start
                next_elem = next_elems[0]
                ladles_info[f'{elem.ladle_id}']['next_aggregate'] = f'{next_elem.aggregate_info.title}'
                ladles_info[f'{elem.ladle_id}'][
                    'next_plan_start'] = f'{next_elem.plan_start.astimezone(pytz.timezone(settings.TIME_ZONE))}'
                ladles_info[f'{elem.ladle_id}'][
                    'next_plan_end'] = f'{next_elem.plan_end.astimezone(pytz.timezone(settings.TIME_ZONE))}'
                ladles_info[f'{elem.ladle_id}']['next_x'] = next_elem.aggregate_info.coord_x
                ladles_info[f'{elem.ladle_id}']['next_y'] = next_elem.aggregate_info.coord_y
                ladles_info[f'{elem.ladle_id}']['next_id'] = next_elem.id
            elif not next_elems and ladles_info[str(elem.ladle_id)]['is_transporting']:
                # если ковш отмечен, как транспортируемый и у него нет следующей позиции
                # то такой ковш завершил свою последнюю операцию, а значит
                # его нужно переписать в архивную таблицу и удалить из активной
                # удаляю из словаря, чтобы ковш не отображался на сайте
                del ladles_info[str(elem.ladle_id)]
                # Добавляю id записей, которые нужно переписать из активной в архивную таблицу
                deletion_ids.append(elem.id)

        return ladles_info, deletion_ids
