from models.employees import EmployeesORM
from schemas.employees import EmployeesReadDTO
from utils.repositories_base import SqlAlchemyRepo


class EmployeesRepo(SqlAlchemyRepo):
    """Репозиторий работника"""
    model = EmployeesORM
    read_schema = EmployeesReadDTO
