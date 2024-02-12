from passlib.context import CryptContext

from django.utils.text import slugify

from schemas.employees import EmployeesCreateDTO
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
            return employee

    def get_employee_by_slug(self, uow: AbstractUnitOfWork, user_slug: str):
        """Получение пользователя по slug"""
        with uow:
            employee = uow.employees_repo.retrieve_one(slug=user_slug)
            return employee

    def get_employees(
        self,
        uow: AbstractUnitOfWork,
        offset: int = 0,
        limit: int = 100,
        **filters
    ):
        """Получение пользователей"""
        with uow:
            employees = uow.employees_repo.retrieve_all(offset=offset, limit=limit, **filters)
            return employees

    def update_employee(self, uow: AbstractUnitOfWork, data,  **filters):
        """Обновление пользователя"""
        with uow:
            employee = uow.employees_repo.update_one(data=data, **filters)
            uow.commit()
            return employee

    def delete_user(self, uow: AbstractUnitOfWork, **filters):
        """Удаление пользователя"""
        with uow:
            employee = uow.employees_repo.delete_one(**filters)
            uow.commit()
            return employee

    def create_user(self, uow: AbstractUnitOfWork, data: EmployeesCreateDTO):
        """Создание нового пользователя"""
        # хэширую пароль и привожу slug к корректному формату
        password: str = data.password
        hashed_password: str = self.hash_password(password)
        slug = slugify(f'{data.username}')
        # обновляю пароль и slug
        data.password = hashed_password
        data.slug = slug
        with uow:
            # создание пользователя
            new_employee = uow.employees_repo.create_one(data=data)
            uow.commit()
            return new_employee
