from models.dynamics import ArchiveDynamicTableORM, ActiveDynamicTableORM
from utils.repositories_base import SqlAlchemyRepo


class ArchiveDynamicTableRepo(SqlAlchemyRepo):
    """Репозиторий архивных записей динамической таблицы"""
    model = ArchiveDynamicTableORM


class ActiveDynamicTableRepo(SqlAlchemyRepo):
    """Репозиторий активных записей динамической таблицы"""
    model = ActiveDynamicTableORM
