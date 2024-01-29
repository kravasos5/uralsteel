import datetime
from enum import Enum
from http import HTTPStatus
from typing import Type

import pytz
from django.contrib.auth.hashers import make_password
from passlib.context import CryptContext
from sqlalchemy.orm import Session, selectinload
from django.utils.text import slugify

from uralsteel.settings import TIME_ZONE
from visual.tasks import archive_report_handler
from . import models, schemas
from ...uralsteel.visual.views import CranesView, LadlesView, LadleOperationTypes


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


def delete_from_db(db: Session, obj) -> None:
    """Удаление объекта из БД"""
    db.delete(obj)
    db.commit()
    db.refresh(obj)


def update_obj(db: Session, obj, obj_info, http_method: HTTPMethods):
    """Обновление объекта методом PUT или PATCH"""
    if http_method is HTTPMethods.put:
        return update_obj_put_patch(db, obj, obj_info)
    elif http_method is HTTPMethods.patch:
        return update_obj_put_patch(db, obj, obj_info, exclude_unset=True)


def update_obj_put_patch(db: Session, obj, obj_info, exclude_unset: bool = False):
    """Обновление объекта PUT или PATCH методом"""
    for key, value in obj_info.model_dump(exclude_unset=exclude_unset):
        setattr(obj, key, value)
    return commit_refresh(db, obj)


def hash_password(password: str) -> str:
    # Создаю объект CryptContext для хэширования пароля
    password_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
    # Используем passlib для хеширования пароля
    hashed_password = password_context.hash(password)
    return hashed_password


###################################################################
# Контроллеры пользователя (Employees)
def get_user_by_id(db: Session, user_id: int):
    """Получение пользователя по id"""
    return db.query(models.Employees).filter_by(id=user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Получение пользователей"""
    return db.query(models.Employees).offset(skip).limit(limit).all()


def update_user(
    db: Session,
    user_id: int,
    user_info: schemas.EmployeesUpdateSchema,
    http_method: HTTPMethods
):
    """Изменение пользователя"""
    user_db = get_user_by_id(db, user_id)
    if user_db:
        return update_obj(db, user_db, user_info, http_method)


def delete_user(db: Session, user_id: int):
    """Удаление пользователя"""
    user_db = get_user_by_id(db, user_id)
    delete_from_db(db, user_db)
    return HTTPStatus.NO_CONTENT


def create_user(db: Session, user_info: schemas.EmployeesCreateSchema):
    """Создание нового пользователя"""
    user_dict: dict = user_info.model_dump()
    password: str = user_dict.get('password')
    hashed_password: str = hash_password(password)
    slug = slugify(f'{user_dict.get("username")}')
    user_db = models.Employees(**user_dict, password=make_password(hashed_password), slug=slug)
    return create_in_db(db, user_db)


###################################################################
# Контроллеры отчёта пользователя
def get_report_by_id(db: Session, report_id: int, report_model):
    """Получение отчёта проишествия"""
    return db.query(report_model).filter_by(id=report_id).first()


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
        report_model,
        http_method: HTTPMethods
):
    """Изменение отчёта проишествия"""
    report = get_report_by_id(db, report_id, report_model)
    if report:
        return update_obj(db, report, report_info, http_method)


def delete_repost(db: Session, report_id: int, report_model):
    """Удаление отчёта о проишествии"""
    report_db = get_report_by_id(db, report_id, report_model)
    delete_from_db(db, report_db)
    return HTTPStatus.NO_CONTENT


def create_report_for_user(first_name: str, email: str):
    """Формирование отчёта для пользователя"""
    archive_report_handler.delay(first_name, email)
    return {'message': 'Письмо с отчётом успешно отправлено.'}


###################################################################
# Контроллеры кранов
def get_crane_by_id(db: Session, crane_id: int):
    """Получение крана по id"""
    return db.query(models.Cranes).filter_by(id=crane_id).first()


def get_cranes(db: Session, skip: int, limit: int = 100):
    """Получение кранов"""
    return db.query(models.Cranes).offset(skip).limit(limit).all()


def update_crane_put(
    db: Session,
    crane_id: int,
    crane_info: schemas.CranesSchema,
    http_method: HTTPMethods
):
    """Изменение крана"""
    crane = get_crane_by_id(db, crane_id)
    if crane:
        return update_obj(db, crane, crane_info, http_method)


def delete_crane(db: Session, crane_id: int):
    """Удаление крана по id"""
    crane_db = get_crane_by_id(db, crane_id)
    delete_from_db(db, crane_db)


def create_crane(db: Session, crane_info: schemas.CranesBaseSchema):
    """Создание крана"""
    crane_db = models.Cranes(**crane_info.model_dump())
    return create_in_db(db, crane_db)


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
    return db.query(models.Ladles).filter_by(id=ladle_id).first()


def get_ladles(db: Session, skip: int = 0, limit: int = 100):
    """Получение ковшей"""
    return db.query(models.Ladles).offset(skip).limit(limit).all()


def update_ladle(
        db: Session,
        ladle_id: int,
        ladle_info: schemas.LadlesBaseSchema,
        http_method: HTTPMethods
):
    """Изменение ковша по его id"""
    ladle_db = get_ladle_by_id(db, ladle_id)
    if ladle_db:
        return update_obj(db, ladle_db, ladle_info, http_method)


def delete_ladle(db: Session, ladle_id: int):
    """Удаление ковша по id"""
    ladle_db = get_ladle_by_id(db, ladle_id)
    delete_from_db(db, ladle_db)


def create_ladle(db: Session, ladle_info: schemas.LadlesBaseSchema):
    """Создание ковша"""
    ladle_db = models.Ladles(**ladle_info.model_dump())
    return create_in_db(db, ladle_db)


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


def time_convert(time: str) -> datetime:
    """Метод, переводящий время в удобный формат без использования django timezone"""
    t: list[str, str] = time.split(':')
    hours: int = int(t[0])
    minutes: int = int(t[1])
    # записываю время в redis-cache
    LadlesView.set_key_redis('ltimeform', f'{hours}:{minutes}', 120)
    # получаю "наивную дату"
    naive_datetime = datetime.datetime(2023, 12, 11, hours, minutes)
    # преобразую её в "осведомлённую", то есть знающую часовой пояс
    aware_datetime = pytz.timezone(TIME_ZONE).localize(naive_datetime)
    ############
    # в будущем здесь может быть любая дата, но будет текущий день
    # получаю текущий часовой пояс
    # current_timezone = pytz.timezone(TIME_ZONE)
    # получаю сегодняшнюю дату
    # today = current_timezone.localize(datetime.now())
    ############
    return aware_datetime


def get_ladles_info(db: Session, date: datetime):
    """Получение информации о положении ковшей на странице"""
    # Использование статических методов из LadlesView
    # date = LadlesView.time_convert(date)
    # data: dict = LadlesView.get_ladles_info(date)
    # return data

    # Использование sqlalchemy
    ladles_info: dict = {}
    # получаю имя ключа, которое используется при кэшировании
    key_name: str = f"ltime:{date.strftime('%H-%M')}"
    # проверка наличия ключа в redis-cache
    result: dict | None = LadlesView.get_key_redis_json(key_name)
    if result is not None:
        return result
    # если ключа нет, то брать информацию из базы данных,
    # она автоматически добавится в кэш в конце этого метода, перед return
    ladles_queryset = db.query(models.ActiveDynamicTable) \
        .options(selectinload(models.ActiveDynamicTable.ladle_info),
                 selectinload(models.ActiveDynamicTable.brand_steel_info),
                 selectinload(models.ActiveDynamicTable.aggregate_info)) \
        .filter(models.ActiveDynamicTable.actual_start.isnot(None),
                models.ActiveDynamicTable.actual_end.isnot(None),
                models.ActiveDynamicTable.actual_start <= date).all()
    # добавляю всю нужную информацию в словарь
    ladles_info = ladles_into_dict(db, ladles_queryset, ladles_info, is_transporting=True)
    # Извлекаю "ожидающие" ковши
    ladles_queryset = db.query(models.ActiveDynamicTable) \
        .options(selectinload(models.ActiveDynamicTable.ladle_info),
                 selectinload(models.ActiveDynamicTable.brand_steel_info),
                 selectinload(models.ActiveDynamicTable.aggregate_info)) \
        .filter(models.ActiveDynamicTable.actual_start.isnot(None),
                models.ActiveDynamicTable.actual_end.is_(None),
                models.ActiveDynamicTable.actual_start <= date).all()
    # добавляю всю нужную информацию в словарь
    ladles_info = ladles_into_dict(db, ladles_queryset, ladles_info)
    # Извлекаю "начинающие" ковши
    ladles_queryset = db.query(models.ActiveDynamicTable) \
        .options(selectinload(models.ActiveDynamicTable.ladle_info),
                 selectinload(models.ActiveDynamicTable.brand_steel_info),
                 selectinload(models.ActiveDynamicTable.aggregate_info)) \
        .filter(models.ActiveDynamicTable.actual_start.is_(None),
                models.ActiveDynamicTable.actual_end.is_(None),
                models.ActiveDynamicTable.plan_start < date,
                models.ActiveDynamicTable.plan_end > date).all()
    # добавляю всю нужную информацию в словарь
    ladles_info = ladles_into_dict(db, ladles_queryset, ladles_info, is_plan=True)
    # добавление ключа в redis
    LadlesView.set_key_redis_json(key_name, ladles_info, 300)
    return ladles_info


def ladles_into_dict(
        db: Session,
        ladles_queryset,
        ladles_info: dict,
        is_transporting: bool = False,
        is_plan: bool = False
) -> dict:
    """
    Метод, преобразующий queryset ковшей в dict.
    Этот метод создаёт единый фундамент для всех видов
    ковшей, передаваемых фронту. Преобразование проходит с использованием sqlalchemy
    """
    for elem in ladles_queryset:
        if str(elem.ladle_info.id) in ladles_info:
            continue
        ladles_info[f'{elem.ladle_info.id}'] = {
            'ladle_title': f'{elem.ladle_info.title}',
            'x': elem.aggregate_info.coord_x,
            'y': elem.aggregate_info.coord_y,
            'num_melt': f'{elem.num_melt}',
            'brand_steel': f'{elem.brand_steel_info.title}',
            'aggregate': f'{elem.aggregate_info.title}',
            'plan_start': f'{elem.plan_start.astimezone(pytz.timezone(TIME_ZONE))}',
            'plan_end': f'{elem.plan_end.astimezone(pytz.timezone(TIME_ZONE))}',
            'next_aggregate': '-',
            'next_plan_start': '-',
            'next_plan_end': '-',
            'operation_id': elem.id
        }
        if is_transporting:
            # если ковш едет на следующую позицию, то есть
            # он "транспортируемый", то is_transporting=True
            ladles_info[f'{elem.ladle_info.id}']['is_transporting'] = True
        else:
            ladles_info[f'{elem.ladle_info.id}']['is_transporting'] = False

        if is_plan:
            # для "начинающих" ковшей
            ladles_info[f'{elem.ladle_info.id}']['photo'] = '/media/photos/aggregates/starting_ladle.png'
            ladles_info[f'{elem.ladle_info.id}']['is_starting'] = True
        else:
            # для "транспортируемых" и "ожидающих"
            ladles_info[f'{elem.ladle_info.id}']['photo'] = f'{elem.aggregate_info.photo.url}'
            ladles_info[f'{elem.ladle_info.id}']['is_starting'] = False

        # нахожу следующую позицию текущего ковша в БД
        next_elems = db.query(models.ActiveDynamicTable) \
            .options(selectinload(models.ActiveDynamicTable.aggregate_info)) \
            .filter(models.ActiveDynamicTable.ladle == elem.ladle,
                    models.ActiveDynamicTable.route == elem.route,
                    models.ActiveDynamicTable.brand_steel == elem.brand_steel,
                    models.ActiveDynamicTable.num_melt == elem.num_melt,
                    models.ActiveDynamicTable.plan_start > elem.plan_end) \
            .order_by(models.ActiveDynamicTable.plan_start)
        # если следующая позиция присутствует, то обновляю
        # соответствующие поля словаря
        if next_elems.exists():
            # получаю следующую позицию ковша
            # это первый элемент next_elems, так как next_elems
            # отсортирован по plan_start
            next_elem = next_elems.first()
            ladles_info[f'{elem.ladle_info.id}']['next_aggregate'] = f'{next_elem.aggregate_info.title}'
            ladles_info[f'{elem.ladle_info.id}'][
                'next_plan_start'] = f'{next_elem.plan_start.astimezone(pytz.timezone(TIME_ZONE))}'
            ladles_info[f'{elem.ladle_info.id}'][
                'next_plan_end'] = f'{next_elem.plan_end.astimezone(pytz.timezone(TIME_ZONE))}'
            ladles_info[f'{elem.ladle_info.id}']['next_x'] = next_elem.aggregate_info.coord_x
            ladles_info[f'{elem.ladle_info.id}']['next_y'] = next_elem.aggregate_info.coord_y
            ladles_info[f'{elem.ladle_info.id}']['next_id'] = next_elem.id
        elif not next_elems.exists() and ladles_info[str(elem.ladle_info.id)]['is_transporting']:
            # если ковш отмечен, как транспортируемый и у него нет следующей позиции
            # то такой ковш завершил свою последнюю операцию, а значит
            # его нужно переписать в архивную таблицу и удалить из активной
            # удаляю из словаря, чтобы ковш не отображался на сайте
            del ladles_info[str(elem.ladle_info.id)]
            # переписываю запись из активной таблицы в архивную
            from_active_to_archive(db, elem)

    return ladles_info


def from_active_to_archive(db: Session, operation: Type[models.ActiveDynamicTable]) -> None:
    """Метод, переписывающий ковш из активной таблицы в архив с помощью sqlalchemy"""
    # перезаписываю запись в архивную таблицу
    new_obj = models.ArchiveDynamicTable(
        ladle=operation.ladle,
        num_melt=operation.num_melt,
        brand_steel=operation.brand_steel,
        route=operation.route,
        aggregate=operation.aggregate,
        plan_start=operation.plan_start,
        plan_end=operation.plan_end,
        actual_start=operation.actual_start,
        actual_end=operation.actual_end)
    create_in_db(db, new_obj)
    # удаляю запись из активной таблицы
    delete_from_db(db, operation)


def ladle_operation_id(db: Session, operation_id: int, operation_type: LadleOperationTypes, time: str):
    """Запрос с операцией над ковшом"""
    data: dict = {}
    # получаю объект операции или 404
    operation = db.query(models.ActiveDynamicTable).filter_by(id=operation_id).first()
    # получаю время
    time = time_convert(time)
    # удаляю старые ключи из хранилища redis
    LadlesView.delete_keys_redis('*ltime:*')
    status: int = HTTPStatus.OK
    match operation_type.value:
        case LadleOperationTypes.TRANSPORTING.value:
            # если ковш "транспортируемый"
            # перезаписываю запись в архивную таблицу
            from_active_to_archive(db, operation)
            data['st'] = 'перемещён в архив'
        case LadleOperationTypes.STARTING.value:
            # если ковш "начинающий"
            # перезаписываю дату в операции Активной Таблицы,
            # то есть теперь ковш стаёт "ожидающим"
            operation.actual_start = time
            commit_refresh(db, operation)
            data['st'] = 'теперь ковш ожидающим'
        case LadleOperationTypes.ENDING.value:
            # если ковш "ожидающий"
            # перезаписываю дату в операции Активной Таблицы,
            # то есть теперь ковш стаёт "транспортируемым"
            operation.actual_end = time
            commit_refresh(db, operation)
            data['st'] = 'теперь ковш транспортируемый'
        case _:
            # в таком случае status=400, то есть пользователь
            # клиент неверно указал operation_type
            status = HTTPStatus.BAD_REQUEST
            data['st'] = 'неверно указан operation_type'
    data['status'] = status
    return data
