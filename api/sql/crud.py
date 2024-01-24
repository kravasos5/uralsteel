from typing import Any

from sqlalchemy.orm import Session

from . import models, schemas


###################################################################
# Контроллеры пользователя (Employees)
def get_user_by_id(db: Session, user_id: int):
    """Получение пользователя по id"""
    return db.query(models.Employees).filter(models.Employees.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Получение пользователей"""
    return db.query(models.Employees).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_info: schemas.EmployeesUpdateSchema):
    """Изменение пользователя"""
    user_db = db.query(models.Employees).get(id=user_id)
    if user_db:
        for key, value in user_info.model_dump():
            setattr(user_db, key, value)
        user_db.commit()
        user_db.refresh()
        return user_db


def update_user_field(db: Session, user_id: int, field: str, value: Any):
    """Изменение одного атрибута пользователя"""
    user_db = db.query(models.Employees).get(id=user_id)
    if user_db:
        setattr(user_db, field, value)
        user_db.commit()
        user_db.refresh()
        return user_db


###################################################################
# Контроллеры отчёта пользователя
def get_report(db: Session, report_id: int, report_model):
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
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def update_report(
        db: Session,
        report_info: schemas.AccidentsBaseSchema,
        report_id: int,
        report_model
):
    """Изменение отчёта проишествия"""
    report = db.query(report_model).get(id=report_id)
    if report:
        for key, value in report_info.model_dump():
            setattr(report, key, value)
        report.commit()
        report.refresh()
        return report


###################################################################
# Контроллеры кранов
