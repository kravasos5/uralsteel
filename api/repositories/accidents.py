from models.accidents import LadlesAccidentORM, CranesAccidentORM, AggregatesAccidentORM
from schemas.accidents import LadlesAccidentReadDTO, CranesAccidentReadDTO, AggregateAccidentReadDTO
from utils.repositories_base import SqlAlchemyRepo


class LadlesAccidentRepo(SqlAlchemyRepo):
    """Репозиторий происшествия с ковшом"""
    model = LadlesAccidentORM
    read_schema = LadlesAccidentReadDTO


class CranesAccidentRepo(SqlAlchemyRepo):
    """Репозиторий происшествия с краном"""
    model = CranesAccidentORM
    read_schema = CranesAccidentReadDTO


class AggregatesAccidentRepo(SqlAlchemyRepo):
    """Репозиторий происшествия с агрегатом"""
    model = AggregatesAccidentORM
    read_schema = AggregateAccidentReadDTO
