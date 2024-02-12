from datetime import datetime

from pydantic import BaseModel, EmailStr

from models.employees import Posts


class EmployeesBaseDTO(BaseModel):
    """Схема работника"""
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    patronymic: str | None
    send_messages: bool = True
    photo: str | None


class EmployeesCreateDTO(EmployeesBaseDTO):
    """Схема создания работника"""
    password: str


class EmployeesUpdateDTO(EmployeesBaseDTO):
    """Схема изменения работника"""
    pass


class EmployeesReadDTO(EmployeesBaseDTO):
    """Схема чтения пользовательских данных"""
    id: int
    last_login: datetime | None
    is_active: bool = True
    date_joined: datetime
    post: Posts
    slug: str

    class Config:
        from_attributes = True


class EmployeesAdminReadDTO(EmployeesReadDTO):
    """Расширенная схема пользователя"""
    is_superuser: bool
    is_staff: bool
