from datetime import datetime

from pydantic import BaseModel, EmailStr

from models.employees import Posts


class EmployeesBaseDTO(BaseModel):
    """Схема работника"""
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    patronymic: str | None = None
    send_messages: bool = True
    photo: str | None = None
    post: Posts


class EmployeesCreateDTO(EmployeesBaseDTO):
    """Схема создания работника"""
    password: str
    slug: str | None = None


class EmployeesUpdateDTO(EmployeesBaseDTO):
    """Схема изменения работника"""
    pass


class EmployeesPatchUpdateDTO(BaseModel):
    """Схема изменения работника методом PATCH"""
    email: EmailStr | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    send_messages: bool | None = None
    photo: str | None = None
    post: Posts | None = None


class EmployeesReadDTO(EmployeesBaseDTO):
    """Схема чтения пользовательских данных"""
    id: int
    last_login: datetime | None
    is_active: bool = True
    date_joined: datetime
    slug: str

    class Config:
        from_attributes = True


class EmployeesAdminReadDTO(EmployeesReadDTO):
    """Расширенная схема пользователя"""
    is_superuser: bool
    is_staff: bool


class EmployeeLoginDTO(BaseModel):
    """Схема аутентификации"""
    username: str
    password: str


class EmployeeAuthReadDTO(EmployeesReadDTO):
    """Схема для аутентификации"""
    password: str
    is_superuser: bool


class EmployeePasswordRestStartDTO(BaseModel):
    """Схема для сброса пароля"""
    token: str


class EmployeePasswordResetDTO(BaseModel):
    """Схема сброса пароля"""
    password: str


class EmployeeResetPayloadDTO(BaseModel):
    """Схема данных, кодируемых в токен для сброса пароля"""
    email: str
    exp: datetime
