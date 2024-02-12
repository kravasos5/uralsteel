from models.ladles import LadlesORM
from utils.repositories_base import SqlAlchemyRepo


class LadlesRepo(SqlAlchemyRepo):
    """Репозиторий ковшей"""
    model = LadlesORM
