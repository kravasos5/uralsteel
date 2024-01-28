from datetime import datetime

from pydantic import BaseModel, EmailStr

from api.sql.models import Posts


###################################################################
# Схемы Employees
class EmployeesBaseSchema(BaseModel):
    """Схема работника"""
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    patronymic: str | None
    send_messages: bool = True
    photo: str | None


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


###################################################################
# Схемы агрегатов
class AggregatesBaseSchema(BaseModel):
    """Схема агрегатов (справочная информация)"""
    title: str
    num_agg: str
    num_pos: str
    coord_x: int
    coord_y: int
    stay_time: datetime
    photo: str
    is_broken: bool


class AggregatesSchema(AggregatesBaseSchema):
    """Схема агрегатов (справочная информация) для чтения"""
    id: int

    class Config:
        orm_mode = True


###################################################################
# Схемы маршрутов
class RoutesBaseSchema(BaseModel):
    """Схема маршрутов"""
    aggregate_1: AggregatesSchema
    aggregate_2: AggregatesSchema
    aggregate_3: AggregatesSchema
    aggregate_4: AggregatesSchema


class RoutesSchema(BaseModel):
    """Схема маршрутов для чтения"""
    id: int

    class Config:
        orm_mode = True


###################################################################
# Схемы кранов
class CranesBaseSchema(BaseModel):
    """Схема кранов"""
    title: str
    size_x: int
    size_y: int
    photo: str
    is_broken: bool


class CranesSchema(CranesBaseSchema):
    """Схема кранов для чтения"""
    id: int

    class Config:
        orm_mode = True


###################################################################
# Схемы ковшей
class LadlesBaseSchema(BaseModel):
    """Схема ковша"""
    title: str
    is_active: int
    is_broken: bool


class LadlesSchema(LadlesBaseSchema):
    """Схема ковша для чтения"""
    id: int

    class Config:
        orm_mode = True


###################################################################
# Схемы марок стали
class BrandSteelBaseSchema(BaseModel):
    """Схема марок стали"""
    title: str

    class Config:
        orm_mode = True


class BrandSteelSchema(BrandSteelBaseSchema):
    """Схема марок стали для чтения"""
    id: int

    class Config:
        orm_mode = True


###################################################################
# Схемы динамических таблиц
class DynamicTableBaseSchema(BaseModel):
    """Схема основной таблицы с информацией о перемещении ковшей в реальном времени"""
    ladle: int
    num_melt: str
    brand_steel: int
    route: int
    aggregate: int
    plan_start: datetime
    plan_end: datetime
    actual_start: datetime
    actual_end: datetime
    ladle_info: LadlesSchema
    brand_steel_info: BrandSteelSchema
    route_info: RoutesSchema
    aggregate_info: AggregatesSchema


class DynamicTableSchema(DynamicTableBaseSchema):
    """
    Схема основной таблицы с информацией о перемещении ковшей в реальном времени.
    Для чтения.
    """
    id: int


###################################################################
# Схемы проишествий
class AccidentsBaseSchema(BaseModel):
    """Схема происшествий"""
    author: int
    report: str
    created_at: datetime
    author_info: EmployeesReadSchema
    object: int


class LadlesAccidentSchema(AccidentsBaseSchema):
    """Схема происшествий с ковшами"""
    object_info: list[LadlesSchema]


class CranesAccidentSchema(AccidentsBaseSchema):
    """Модель проишествий кранов"""
    object_info: list[CranesSchema]


class AggregateAccidentSchema(AccidentsBaseSchema):
    """Модель проишествий кранов"""
    object_info: list[AggregatesSchema]
