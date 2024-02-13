from pydantic import BaseModel

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
