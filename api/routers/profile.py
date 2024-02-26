import os
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Path, UploadFile, File, Depends, HTTPException, Query

from dependencies import UOWDep, is_object, GetIdDEP, error_raiser_if_none, AccServiceDEP, EmpUpdatePatchFieldsDEP, \
    EmpUpdateFieldsDEP, oauth2_scheme, get_current_active_auth_user, employeeSlugPermissionDEP, emailDEP, \
    ResetPasswordDEP, ResetPayloadDEP, is_author_and_accident_object, access_denied, make_object_broken
from schemas.accidents import AccidentReadDTO, AccidentsCreateUpdateDTO, AccidentsUpdatePatchDTO, AccidentsCreateDTO
from schemas.aggregates import AggregatesUpdatePatchDTO
from schemas.cranes import CranesUpdatePatchDTO
from schemas.employees import EmployeesReadDTO, EmployeesUpdateDTO, EmployeesPatchUpdateDTO, \
    EmployeePasswordRestStartDTO
from schemas.ladles import LadlesUpdatePatchDTO
from services.accidents import AggregatesAccidentService, LadlesAccidentService, CranesAccidentService
from services.aggregates import AggregatesAllService
from services.cranes import CranesService
from services.employees import EmployeesService
from services.ladles import LadlesService
from utils.utilities import Base64Converter, PhotoAddToSchema
from utils import password_reset_utils


router = APIRouter(
    prefix='/profile',
    tags=['users'],
    dependencies=[Depends(oauth2_scheme)],
)


password_reset_router = APIRouter(
    prefix='/profile',
    tags=['users'],
)


path_start: str = 'photos'


@router.get('/me', response_model=EmployeesReadDTO)
def get_profile_auth_user(
    employee: Annotated[EmployeesReadDTO, Depends(get_current_active_auth_user)]
):
    """Получить профиль аутентифицированного работника"""
    answer_data = Base64Converter.key_to_base64(employee)
    return answer_data


@router.get('/{slug}', response_model=EmployeesReadDTO)
async def get_profile(
    slug: Annotated[str, Path(max_length=200)],
    uow: UOWDep
):
    """Получить данные профиля работника"""
    employee = EmployeesService().retrieve_one_by_slug(uow=uow, employee_slug=slug)
    error_raiser_if_none(employee, 'Profile')
    answer_data = Base64Converter.key_to_base64(employee)
    return answer_data


@router.put('/{slug}/change', response_model=EmployeesReadDTO)
async def change_profile_put(
    slug: employeeSlugPermissionDEP,
    uow: UOWDep,
    updated_employee: EmpUpdateFieldsDEP,
    photo: Annotated[UploadFile, File()],
):
    """Обновить данные профиля работника"""
    path: str = os.path.join(path_start, updated_employee["username"])
    update_data = await PhotoAddToSchema.file_add(
        photo, path, updated_employee, EmployeesUpdateDTO,
        create_dir=True, created_dir=path
    )
    employee = EmployeesService().update_one(uow=uow, data_schema=update_data, slug=slug)
    error_raiser_if_none(employee, 'Profile')
    answer_data = Base64Converter.key_to_base64(employee)
    return answer_data


@router.patch('/{slug}/change', response_model=EmployeesReadDTO)
async def change_profile_patch(
    slug: employeeSlugPermissionDEP,
    uow: UOWDep,
    updated_employee: EmpUpdatePatchFieldsDEP,
    photo: Annotated[UploadFile, File()] = None,
):
    """Обновить данные профиля работника"""
    service = EmployeesService()
    updated_employee = {key: value for key, value in updated_employee.items() if value is not None}
    if photo:
        if 'username' not in updated_employee:
            empl = service.retrieve_one(uow, slug=slug)
            path: str = os.path.join(path_start, empl.username)
        else:
            path: str = os.path.join(path_start, updated_employee["username"])
        update_data = await PhotoAddToSchema.file_add(
            photo, path, updated_employee, EmployeesPatchUpdateDTO,
            create_dir=True, created_dir=path
        )
    else:
        update_data = EmployeesPatchUpdateDTO(**updated_employee)
    employee = service.update_one(uow=uow, data_schema=update_data, slug=slug)
    error_raiser_if_none(employee, 'Profile')
    answer_data = Base64Converter.key_to_base64(employee)
    return answer_data


@password_reset_router.post('/password/reset', response_model=EmployeePasswordRestStartDTO)
async def password_reset(
    email: emailDEP,
):
    # Начало и отправка письма
    # функционал отправки письма
    payload = {
        'email': email,
    }
    token = password_reset_utils.generate_token(payload)
    return EmployeePasswordRestStartDTO(token=token)


@password_reset_router.patch('/password/reset/confirm/{token}')
async def password_reset(
    uow: UOWDep,
    payload: ResetPayloadDEP,
    hashed_password: ResetPasswordDEP,
):
    # сброс пароля
    EmployeesService().update_one(uow=uow, data_schema=hashed_password, email=payload.email)
    return {'message': 'Password changed'}


@router.get('/archive-report', include_in_schema=False)
async def get_archive_report():
    """Получение архивного отчёта"""
    # Celery
    ...


@router.post('/report/create', response_model=AccidentReadDTO)
async def create_accident(
    uow: UOWDep,
    service: AccServiceDEP,
    accident_data: AccidentsCreateDTO,
    employee: Annotated[EmployeesReadDTO, Depends(get_current_active_auth_user)],
):
    """Создание отчёта о происшествии"""
    # проверка есть ли такой автор и агрегат
    is_author_and_accident_object(uow, employee.id, accident_data.object_id, service)
    new_report = AccidentsCreateUpdateDTO(
        author_id=employee.id,
        report=accident_data.report,
        object_id=accident_data.object_id,
    )
    new_accident = service.create_one(uow, new_report)
    # отметить объект отчёта сломанным
    make_object_broken(uow, service, new_report.object_id)
    return new_accident


@router.patch('/report/update/{object_id}', response_model=AccidentReadDTO)
async def update_crane_patch(
    uow: UOWDep,
    service: AccServiceDEP,
    object_id: GetIdDEP,
    updated_report: Annotated[str, Query(max_length=800)],
    employee: Annotated[EmployeesReadDTO, Depends(get_current_active_auth_user)],
):
    """Обновление комментария отчёта происшествия методом patch"""
    # проверка существует ли такой отчёт
    if not (report := service.retrieve_one(uow, id=object_id)):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Report with that id doesn't exist"
        )
    # является ли текущий пользователь автором этого отчёта
    if report.author_id != employee.id:
        raise access_denied
    # получаю обновлённый dto происшествия
    new_report_data = AccidentsUpdatePatchDTO(report=updated_report)
    # обновляю происшествие
    updated_acc = service.update_one(uow, new_report_data, id=object_id)
    return updated_acc
