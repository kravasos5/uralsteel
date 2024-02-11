from models.dynamics import ArchiveDynamicTable, ActiveDynamicTable
from utils.repositories_base import SqlAlchemyRepo


class ArchiveDynamicTableRepo(SqlAlchemyRepo):
    """Репозиторий архивных записей динамической таблицы"""
    model = ArchiveDynamicTable


class ActiveDynamicTableRepo(SqlAlchemyRepo):
    """Репозиторий активных записей динамической таблицы"""
    model = ActiveDynamicTable
