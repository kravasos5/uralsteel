from models.aggregates import AggregatesGMPORM, AggregatesUKPORM, AggregatesUVSORM, AggregatesMNLZORM, AggregatesLORM, AggregatesBurnerORM
from utils.repositories_base import SqlAlchemyRepo


class AggregatesGMPRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов ГМП"""
    model = AggregatesGMPORM


class AggregatesUKPRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов УКП"""
    model = AggregatesUKPORM


class AggregatesUVSRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов УВС"""
    model = AggregatesUVSORM


class AggregatesMNLZRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов МНЛЗ"""
    model = AggregatesMNLZORM


class AggregatesLRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов Лёжек"""
    model = AggregatesLORM


class AggregatesBurnerRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов Горелок"""
    model = AggregatesBurnerORM
