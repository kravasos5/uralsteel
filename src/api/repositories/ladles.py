from models.ladles import LadlesORM
from schemas.ladles import LadlesReadDTO
from utils.repositories_base import SqlAlchemyRepo


class LadlesRepo(SqlAlchemyRepo):
    """Репозиторий ковшей"""
    model = LadlesORM
    read_schema = LadlesReadDTO
