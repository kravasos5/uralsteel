from models.brandsteel import BrandSteel
from utils.repositories_base import SqlAlchemyRepo


class BrandSteelRepo(SqlAlchemyRepo):
    """Репозиторий марок стали"""
    model = BrandSteel
