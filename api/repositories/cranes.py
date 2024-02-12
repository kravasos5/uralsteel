from models.cranes import CranesORM
from utils.repositories_base import SqlAlchemyRepo


class CranesRepo(SqlAlchemyRepo):
    """Репозиторий кранов"""
    model = CranesORM
