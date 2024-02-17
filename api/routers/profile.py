from typing import Annotated

from fastapi import APIRouter, Path

from dependencies import UOWDep, GetAccTypeDEP, is_object, AccidentType, GetIdDEP, error_raiser_if_none, AccServiceDEP
from schemas.accidents import AccidentReadDTO, AccidentsCreateUpdateDTO, AccidentsUpdatePatchDTO
from schemas.employees import EmployeesReadDTO, EmployeesUpdateDTO, EmployeesPatchUpdateDTO
from services.accidents import CranesAccidentService, LadlesAccidentService, AggregatesAccidentService
from services.employees import EmployeesService


router = APIRouter(
    prefix="/profile",
    tags=["users"],
)


@router.get('/{slug}', response_model=EmployeesReadDTO)
def get_profile(slug: Annotated[str, Path(max_length=200)], uow: UOWDep):
    """Получить данные профиля работника"""
    employee = EmployeesService().retrieve_one_by_slug(uow=uow, user_slug=slug)
    error_raiser_if_none(employee, 'User')
    return employee


@router.put('/{slug}/change', response_model=EmployeesReadDTO)
def change_profile_put(
        slug: Annotated[str, Path(max_length=200)],
        uow: UOWDep,
        updated_employee: EmployeesUpdateDTO,
):
    """Обновить данные профиля работника"""
    employee = EmployeesService().update_one(uow=uow, data_schema=updated_employee, slug=slug)
    error_raiser_if_none(employee, 'User')
    return employee


@router.patch('/{slug}/change', response_model=EmployeesReadDTO)
def change_profile_patch(
        slug: Annotated[str, Path(max_length=200)],
        uow: UOWDep,
        updated_employee: EmployeesPatchUpdateDTO,
):
    """Обновить данные профиля работника"""
    employee = EmployeesService().update_one(uow=uow, data_schema=updated_employee, slug=slug)
    error_raiser_if_none(employee, 'User')
    return employee


@router.get('/password/reset', include_in_schema=False)
def password_reset():
    # Начало и отправка письма
    ...


@router.get('/password/reset/complete', include_in_schema=False)
def password_reset():
    # оповещение об успешно сброшенном пароле
    ...


@router.get('/password/reset/starting', include_in_schema=False)
def password_reset():
    # оповещение об отправленном письме
    ...


@router.get('/password/reset/confirm/{uidb}/{token}', include_in_schema=False)
def password_reset(uidb: int, token: str):
    # сброс пароля
    ...


@router.get('/archive-report', include_in_schema=False)
def get_archive_report():
    """Получение архивного отчёта"""
    # Celery
    ...


@router.post('/report/create', response_model=AccidentReadDTO, include_in_schema=False)
def create_accident(uow: UOWDep, service: AccServiceDEP, accident_data: AccidentsCreateUpdateDTO):
    """Создание отчёта о происшествии"""
    # проверка есть ли такой автор и агрегат
    # is_author(uow, accident_data.author_id)
    accident_data.author_id = id
    # логика назначения автором текущего авторизованного пользователя
    is_object(uow, accident_data.object_id, service)
    new_accident = service.create_one(uow, accident_data)
    return new_accident


@router.patch('/report/update/{object_id}', response_model=AccidentReadDTO, include_in_schema=False)
def update_crane_patch(
        uow: UOWDep,
        service: AccServiceDEP,
        object_id: GetIdDEP,
        accident_data: AccidentsUpdatePatchDTO
):
    """Обновление происшествия методом put"""
    # проверка есть ли такой автор и агрегат
    # is_author(uow, accident_data.author_id)
    accident_data.author_id = id
    # логика назначения автором текущего авторизованного пользователя
    # а также проверка на авторство за этим репортом
    is_object(uow, accident_data.object_id, service)
    updated_acc = service.update_one(uow, accident_data, id=object_id)
    error_raiser_if_none(updated_acc)
    return updated_acc

# Ещё система разграничения доступа с JWT
