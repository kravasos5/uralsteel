from models.cranes import Cranes
from utils.repositories_base import SqlAlchemyRepo


class CranesRepo(SqlAlchemyRepo):
    """Репозиторий кранов"""
    model = Cranes
