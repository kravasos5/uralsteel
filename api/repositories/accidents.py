from models.accidents import LadlesAccidentORM, CranesAccidentORM, AggregatesAccidentORM
from schemas.accidents import LadlesAccidentDTO, CranesAccidentDTO, AggregateAccidentDTO
from utils.repositories_base import SqlAlchemyRepo


class LadlesAccidentRepo(SqlAlchemyRepo):
    """Репозиторий происшествия с ковшом"""
    model = LadlesAccidentORM
    read_schema = LadlesAccidentDTO


class CranesAccidentRepo(SqlAlchemyRepo):
    """Репозиторий происшествия с краном"""
    model = CranesAccidentORM
    read_schema = CranesAccidentDTO


class AggregatesAccidentRepo(SqlAlchemyRepo):
    """Репозиторий происшествия с агрегатом"""
    model = AggregatesAccidentORM
    read_schema = AggregateAccidentDTO
