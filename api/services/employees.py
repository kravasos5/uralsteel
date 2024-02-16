from passlib.context import CryptContext

from django.utils.text import slugify

from schemas.employees import EmployeesCreateDTO
from utils.service_base import ServiceBase
from utils.unitofwork import AbstractUnitOfWork


class EmployeesService(ServiceBase):
    """Сервис взаимодействия с Employees"""
    repository = 'employees_repo'

    def hash_password(self, password: str) -> str:
        # Создаю объект CryptContext для хэширования пароля
        password_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
        # Используем passlib для хеширования пароля
        hashed_password = password_context.hash(password)
        return hashed_password

    def retrieve_one_by_id(self, uow: AbstractUnitOfWork, employee_id: int):
        """Получение пользователя по id"""
        with uow:
            employee = uow.repositories[self.repository].retrieve_one(id=employee_id)
            return employee

    def retrieve_one_by_slug(self, uow: AbstractUnitOfWork, employee_slug: str):
        """Получение пользователя по slug"""
        with uow:
            employee = uow.repositories[self.repository].retrieve_one(slug=employee_slug)
            return employee

    def create_one(self, uow: AbstractUnitOfWork, data: EmployeesCreateDTO):
        """Создание нового пользователя"""
        # хэширую пароль и привожу slug к корректному формату
        password: str = data.password
        hashed_password: str = self.hash_password(password)
        if data.slug:
            slug = slugify(f'{data.slug}')
        else:
            slug = slugify(f'{data.username}')
        # обновляю пароль и slug
        data.password = hashed_password
        data.slug = slug
        with uow:
            # создание пользователя
            new_employee = uow.repositories[self.repository].create_one(data_schema=data)
            uow.commit()
            return new_employee
