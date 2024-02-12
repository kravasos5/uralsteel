from passlib.context import CryptContext

from django.utils.text import slugify

from schemas.employees import EmployeesReadDTO, EmployeesCreateDTO
from schemas.commons import DataConverter
from utils.unitofwork import AbstractUnitOfWork


class EmployeesService:
    """Сервис взаимодействия с Employees"""
    def hash_password(self, password: str) -> str:
        # Создаю объект CryptContext для хэширования пароля
        password_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
        # Используем passlib для хеширования пароля
        hashed_password = password_context.hash(password)
        return hashed_password

    def get_employee_by_id(self, uow: AbstractUnitOfWork, user_id: int):
        """Получение пользователя по id"""
        with uow:
            employee = uow.employees_repo.retrieve_one(id=user_id)
            employee_dto = DataConverter.model_to_dto(employee, EmployeesReadDTO)
            return employee_dto

    def get_employee_by_slug(self, uow: AbstractUnitOfWork, user_slug: str):
        """Получение пользователя по slug"""
        with uow:
            employee = uow.employees_repo.retrieve_one(slug=user_slug)
            employee_dto = DataConverter.model_to_dto(employee, EmployeesReadDTO)
            return employee_dto

    def get_employees(
        self,
        uow: AbstractUnitOfWork,
        skip: int = 0,
        limit: int = 100,
        **filters
    ):
        """Получение пользователей"""
        with uow:
            employees = uow.employees_repo.retrieve_all(limit=limit, offset=skip, **filters)
            employees_dto = DataConverter.models_to_dto(employees, EmployeesReadDTO)
            return employees_dto

    def update_employee(self, uow: AbstractUnitOfWork, data: dict,  **filters):
        """Обновление пользователя"""
        with uow:
            employee = uow.employees_repo.update_one(data=data, **filters)
            return employee

    def delete_user(self, uow: AbstractUnitOfWork, **filters):
        """Удаление пользователя"""
        with uow:
            employee = uow.employees_repo.delete_one(**filters)
            return employee

    def create_user(self, uow: AbstractUnitOfWork, data: EmployeesCreateDTO):
        """Создание нового пользователя"""
        # получаю информацию о новом пользователе
        new_data = DataConverter.dto_to_dict(data)
        # хэширую пароль и привожу slug к корректному формату
        password: str = new_data.get('password')
        hashed_password: str = self.hash_password(password)
        slug = slugify(f'{new_data.get("username")}')
        # обновляю пароль и slug
        new_data['password'] = hashed_password
        new_data['slug'] = slug
        with uow:
            # создание пользователя
            new_employee = uow.employees_repo.create_one(data=new_data)
            # возврат результата в формате dict
            new_employee_dict = DataConverter.model_to_dto(new_employee, EmployeesReadDTO)
            return new_employee_dict
