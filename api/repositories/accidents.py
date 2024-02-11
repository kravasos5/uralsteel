from models.accidents import LadlesAccident, CranesAccident, AggregatesAccident
from utils.repositories_base import SqlAlchemyRepo


class LadlesAccidentRepo(SqlAlchemyRepo):
    """Репозиторий происшествия с ковшом"""
    model = LadlesAccident


class CranesAccidentRepo(SqlAlchemyRepo):
    """Репозиторий происшествия с краном"""
    model = CranesAccident


class AggregatesAccidentRepo(SqlAlchemyRepo):
    """Репозиторий происшествия с агрегатом"""
    model = AggregatesAccident
