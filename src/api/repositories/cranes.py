from models.cranes import CranesORM
from schemas.cranes import CranesReadDTO
from utils.repositories_base import SqlAlchemyRepo


class CranesRepo(SqlAlchemyRepo):
    """Репозиторий кранов"""
    model = CranesORM
    read_schema = CranesReadDTO
