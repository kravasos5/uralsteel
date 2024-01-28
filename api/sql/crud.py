from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Session

from . import models, schemas
from ...uralsteel.visual.views import CranesView, LadlesView


# def commit_refresh(obj):
#     """Коммит изменений и обновление"""
#     obj.commit()
#     obj.refresh()
#     return obj


class HTTPMethods(str, Enum):
    """Класс http-методов"""
    put = 'PUT'
    patch = 'PATCH'
    get = 'GET'
    delete = 'DELETE'


def commit_refresh(db: Session, obj):
    """Коммит изменений и обновление"""
    db.commit()
    db.refresh(obj)
    return obj


def create_in_db(db: Session, obj):
    """Создание объекта в БД"""
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_obj(db: Session, obj, obj_info, http_method: HTTPMethods):
    """Обновление объекта методом PUT или PATCH"""
    if http_method == HTTPMethods.put:
        return update_obj_put_patch(db, obj, obj_info)
    elif http_method == HTTPMethods.patch:
        return update_obj_put_patch(db, obj, obj_info, exclude_unset=True)


def update_obj_put_patch(db: Session, obj, obj_info, exclude_unset: bool = False):
    """Обновление объекта PUT или PATCH методом"""
    for key, value in obj_info.model_dump(exclude_unset=exclude_unset):
        setattr(obj, key, value)
    return commit_refresh(db, obj)


###################################################################
# Контроллеры пользователя (Employees)
def get_user_by_id(db: Session, user_id: int):
    """Получение пользователя по id"""
    return db.query(models.Employees).get(id=user_id)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Получение пользователей"""
    return db.query(models.Employees).offset(skip).limit(limit).all()


def update_user_put(db: Session, user_id: int, user_info: schemas.EmployeesUpdateSchema):
    """Изменение пользователя"""
    user_db = get_user_by_id(db, user_id)
    if user_db:
        return update_obj(db, user_db, user_info, HTTPMethods.put)


def update_user_patch(db: Session, user_id: int, user_info: schemas.EmployeesUpdateSchema):
    """Изменение одного атрибута пользователя"""
    user_db = get_user_by_id(db, user_id)
    if user_db:
        return update_obj(db, user_db, user_info, HTTPMethods.patch)


###################################################################
# Контроллеры отчёта пользователя
def get_report_by_id(db: Session, report_id: int, report_model):
    """Получение отчёта проишествия"""
    return db.query(report_model).get(id=report_id)


def get_reports(db: Session, report_model, skip: int = 0, limit: int = 100):
    """Получение отчётов проишествий"""
    return db.query(report_model).offset(skip).limit(limit).all()


def create_report(
        db: Session,
        report_info: schemas.AccidentsBaseSchema,
        report_model,
        user_id: int
):
    """Создание отчёта проишествия"""
    report = report_model(**report_info.model_dump(), author=user_id)
    return create_in_db(db, report)


def update_report_patch(
        db: Session,
        report_info: schemas.AccidentsBaseSchema,
        report_id: int,
        report_model
):
    """Изменение отчёта проишествия"""
    report = get_report_by_id(db, report_id, report_model)
    if report:
        return update_obj(db, report, report_info, HTTPMethods.patch)


###################################################################
# Контроллеры кранов
def get_crane_by_id(db: Session, crane_id: int):
    """Получение крана по id"""
    return db.query(models.Cranes).get(id=crane_id)


def get_cranes(db: Session, skip: int, limit: int = 100):
    """Получение кранов"""
    return db.query(models.Cranes).offset(skip).limit(limit).all()


def update_crane_put(db: Session, crane_id: int, crane_info: schemas.CranesSchema):
    """Изменение крана PUT"""
    crane = get_crane_by_id(db, crane_id)
    if crane:
        return update_obj(db, crane, crane_info, HTTPMethods.put)


def update_crane_patch(db: Session, crane_id: int, crane_info: schemas.CranesSchema):
    """Изменение крана PATCH"""
    crane = get_crane_by_id(db, crane_id)
    if crane:
        return update_obj(db, crane, crane_info, HTTPMethods.patch)


def get_cranes_pos_info():
    """Получение информации о ковшах"""
    data: dict = {
        'cranes_pos': CranesView.get_cranes_pos(),
        'cranes_info': CranesView.get_cranes_info()
    }
    return data


###################################################################
# Контроллеры ковшей
def get_ladle_by_id(db: Session, ladle_id: int):
    """Получение ковша"""
    return db.query(models.Ladles).get(id=ladle_id)


def get_ladles(db: Session, skip: int = 0, limit: int = 100):
    """Получение ковшей"""
    return db.query(models.Ladles).offset(skip).limit(limit).all()


def update_ladle(
        db: Session,
        ladle_id: int,
        ladle_info: schemas.LadlesBaseSchema,
        http_method: HTTPMethods
):
    """Изменение ковша по его id. PUT"""
    ladle_db = get_ladle_by_id(db, ladle_id)
    if ladle_db:
        return update_obj(db, ladle_db, ladle_info, http_method)


def update_ladle_patch(db: Session, ladle_id: int, ladle_info: schemas.LadlesBaseSchema):
    """Изменение ковша по его id. PATCH"""
    ladle_db = get_ladle_by_id(db, ladle_id)
    if ladle_db:
        return update_obj(db, ladle_db, ladle_info, HTTPMethods.patch)


def get_ladle_timeform():
    """
    Получение информации о времени в форме времени на странице ковшей.
    Проходит проверка наличия значения времени в кэше, оно будет передано
    странице и там обработано
    """
    ladle_timeform = LadlesView.get_key_redis('ltimeform')
    if ladle_timeform:
        return {'timeformvalue': ladle_timeform}
    return {}


def get_ladles_info(date: datetime):
    """Получение информации о положении ковшей на странице"""
    ...
