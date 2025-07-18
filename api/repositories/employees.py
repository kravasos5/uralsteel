from sqlalchemy import select

from models.employees import EmployeesORM
from schemas.commons import DataConverter
from schemas.employees import EmployeesReadDTO, EmployeeAuthReadDTO
from utils.repositories_base import SqlAlchemyRepo


class EmployeesRepo(SqlAlchemyRepo):
    """Репозиторий работника"""
    model = EmployeesORM
    read_schema = EmployeesReadDTO
    auth_schema = EmployeeAuthReadDTO

    async def retrieve_one_by_username(self, **filters):
        """Получение одной записи из бд"""
        stmt = select(self.model).filter_by(**filters)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if res:
            result = await DataConverter.model_to_dto(res, self.auth_schema)
            return result
        return res
