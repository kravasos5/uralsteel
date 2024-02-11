from models.employees import Employees
from utils.repositories_base import SqlAlchemyRepo


class EmployeesRepo(SqlAlchemyRepo):
    """Репозиторий работника"""
    model = Employees
