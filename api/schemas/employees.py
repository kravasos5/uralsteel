from datetime import datetime

from pydantic import BaseModel, EmailStr


###################################################################
# Схемы Employees
from models.employees import Posts


class EmployeesBaseSchema(BaseModel):
    """Схема работника"""
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    patronymic: str | None
    send_messages: bool = True
    photo: str | None


class EmployeesCreateSchema(EmployeesBaseSchema):
    """Схема создания работника"""
    password: str


class EmployeesUpdateSchema(EmployeesBaseSchema):
    """Схема изменения работника"""
    pass


class EmployeesReadSchema(EmployeesBaseSchema):
    """Схема чтения пользовательских данных"""
    id: int
    last_login: datetime | None
    is_active: bool = True
    date_joined: datetime
    post: Posts
    slug: str

    class Config:
        orm_mode = True


class EmployeesAdminReadSchema(EmployeesReadSchema):
    """Расширенная схема пользователя"""
    is_superuser: bool
    is_staff: bool
