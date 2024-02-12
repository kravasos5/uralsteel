from models.routes import RoutesORM
from utils.repositories_base import SqlAlchemyRepo


class RoutesRepo(SqlAlchemyRepo):
    """Репозиторий маршрутов"""
    model = RoutesORM
