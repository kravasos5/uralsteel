from models.employees import EmployeesORM
from utils.repositories_base import SqlAlchemyRepo


class EmployeesRepo(SqlAlchemyRepo):
    """Репозиторий работника"""
    model = EmployeesORM
