from models.aggregates import AggregatesGMPORM, AggregatesUKPORM, AggregatesUVSORM, AggregatesMNLZORM, AggregatesLORM, \
    AggregatesBurnerORM, AggregatesORM
from schemas.aggregates import AggregatesDTO
from utils.repositories_base import SqlAlchemyRepo


class AggregatesAllRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов ГМП"""
    model = AggregatesORM
    read_schema = AggregatesDTO


class AggregatesGMPRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов ГМП"""
    model = AggregatesGMPORM
    read_schema = AggregatesDTO


class AggregatesUKPRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов УКП"""
    model = AggregatesUKPORM
    read_schema = AggregatesDTO


class AggregatesUVSRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов УВС"""
    model = AggregatesUVSORM
    read_schema = AggregatesDTO


class AggregatesMNLZRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов МНЛЗ"""
    model = AggregatesMNLZORM
    read_schema = AggregatesDTO


class AggregatesLRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов Лёжек"""
    model = AggregatesLORM
    read_schema = AggregatesDTO


class AggregatesBurnerRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов Горелок"""
    model = AggregatesBurnerORM
    read_schema = AggregatesDTO
