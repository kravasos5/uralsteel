from models.routes import Routes
from utils.repositories_base import SqlAlchemyRepo


class RoutesRepo(SqlAlchemyRepo):
    """Репозиторий маршрутов"""
    model = Routes
