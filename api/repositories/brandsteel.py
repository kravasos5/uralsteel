from models.brandsteel import BrandSteelORM
from schemas.brandsteel import BrandSteelReadDTO
from utils.repositories_base import SqlAlchemyRepo


class BrandSteelRepo(SqlAlchemyRepo):
    """Репозиторий марок стали"""
    model = BrandSteelORM
    read_schema = BrandSteelReadDTO
