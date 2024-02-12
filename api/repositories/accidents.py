from models.accidents import LadlesAccidentORM, CranesAccidentORM, AggregatesAccidentORM
from utils.repositories_base import SqlAlchemyRepo


class LadlesAccidentRepo(SqlAlchemyRepo):
    """Репозиторий происшествия с ковшом"""
    model = LadlesAccidentORM


class CranesAccidentRepo(SqlAlchemyRepo):
    """Репозиторий происшествия с краном"""
    model = CranesAccidentORM


class AggregatesAccidentRepo(SqlAlchemyRepo):
    """Репозиторий происшествия с агрегатом"""
    model = AggregatesAccidentORM
