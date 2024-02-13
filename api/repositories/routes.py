from models.routes import RoutesORM
from schemas.routes import RoutesReadDTO
from utils.repositories_base import SqlAlchemyRepo


class RoutesRepo(SqlAlchemyRepo):
    """Репозиторий маршрутов"""
    model = RoutesORM
    read_schema = RoutesReadDTO
