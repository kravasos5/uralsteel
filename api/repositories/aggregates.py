from models.aggregates import AggregatesGMP, AggregatesUKP, AggregatesUVS, AggregatesMNLZ, AggregatesL, AggregatesBurner
from utils.repositories_base import SqlAlchemyRepo


class AggregatesGMPRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов ГМП"""
    model = AggregatesGMP


class AggregatesUKPRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов УКП"""
    model = AggregatesUKP


class AggregatesUVSRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов УВС"""
    model = AggregatesUVS


class AggregatesMNLZRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов МНЛЗ"""
    model = AggregatesMNLZ


class AggregatesLRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов Лёжек"""
    model = AggregatesL


class AggregatesBurnerRepo(SqlAlchemyRepo):
    """Репозиторий агрегатов Горелок"""
    model = AggregatesBurner
