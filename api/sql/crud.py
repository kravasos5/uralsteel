from typing import Any

from sqlalchemy.orm import Session

from . import models, schemas
from ...uralsteel.visual.views import CranesView


def commit_refresh(obj):
    """Коммит изменений и обновление"""
    obj.commit()
    obj.refresh()
    return obj


def create_in_db(db: Session, obj):
    """Создание объекта в БД"""
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


###################################################################
# Контроллеры пользователя (Employees)
def get_user_by_id(db: Session, user_id: int):
    """Получение пользователя по id"""
    return db.query(models.Employees).get(id=user_id)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Получение пользователей"""
    return db.query(models.Employees).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_info: schemas.EmployeesUpdateSchema):
    """Изменение пользователя"""
    user_db = get_user_by_id(db, user_id)
    if user_db:
        for key, value in user_info.model_dump():
            setattr(user_db, key, value)
        return commit_refresh(user_db)


def update_user_field(db: Session, user_id: int, field: str, value: Any):
    """Изменение одного атрибута пользователя"""
    user_db = get_user_by_id(db, user_id)
    if user_db:
        setattr(user_db, field, value)
        return commit_refresh(user_db)


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


def update_report(
        db: Session,
        report_info: schemas.AccidentsBaseSchema,
        report_id: int,
        report_model
):
    """Изменение отчёта проишествия"""
    report = get_report_by_id(db, report_id, report_model)
    if report:
        for key, value in report_info.model_dump():
            setattr(report, key, value)
        return commit_refresh(report)


###################################################################
# Контроллеры кранов
def get_crane_by_id(db: Session, crane_id: int):
    """Получение крана по id"""
    return db.query(models.Cranes).get(id=crane_id)


def get_cranes(db: Session, skip: int, limit: int = 100):
    """Получение кранов"""
    return db.query(models.Cranes).offset(skip).limit(limit).all()


def update_crane(db: Session, crane_id: int, crane_info: schemas.CranesSchema):
    """Изменение крана PUT"""
    crane = get_crane_by_id(db, crane_id)
    if crane:
        for field, value in crane_info.model_dump():
            setattr(crane, field, value)
        return commit_refresh(crane)


def update_crane_field(db: Session, crane_id: int, field: str, value: Any):
    """Изменение крана PATCH"""
    crane = get_crane_by_id(db, crane_id)
    if crane:
        setattr(crane, field, value)
        return commit_refresh(crane)


def get_cranes_pos_info(db: Session):
    """Получение информации о ковшах"""
    data: dict = {
        'cranes_pos': CranesView.get_cranes_pos(),
        'cranes_info': CranesView.get_cranes_info()
    }
    return data


###################################################################
# Контроллеры ковшей

