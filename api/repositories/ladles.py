from models.ladles import Ladles
from utils.repositories_base import SqlAlchemyRepo


class LadlesRepo(SqlAlchemyRepo):
    """Репозиторий ковшей"""
    model = Ladles
