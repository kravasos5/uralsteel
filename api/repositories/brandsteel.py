from models.brandsteel import BrandSteelORM
from utils.repositories_base import SqlAlchemyRepo


class BrandSteelRepo(SqlAlchemyRepo):
    """Репозиторий марок стали"""
    model = BrandSteelORM
