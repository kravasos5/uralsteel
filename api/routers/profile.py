from typing import Annotated

from fastapi import APIRouter, Path, UploadFile, File

from dependencies import UOWDep, is_object, GetIdDEP, error_raiser_if_none, AccServiceDEP, EmpUpdatePatchFieldsDEP, \
    EmpUpdateFieldsDEP
from schemas.accidents import AccidentReadDTO, AccidentsCreateUpdateDTO, AccidentsUpdatePatchDTO
from schemas.employees import EmployeesReadDTO, EmployeesUpdateDTO, EmployeesPatchUpdateDTO
from services.employees import EmployeesService
from utils.utilities import Base64Converter, PhotoAddToSchema

router = APIRouter(
    prefix="/profile",
    tags=["users"],
)


path_start: str = 'photos/'


@router.get('/{slug}', response_model=EmployeesReadDTO)
async def get_profile(slug: Annotated[str, Path(max_length=200)], uow: UOWDep):
    """Получить данные профиля работника"""
    employee = EmployeesService().retrieve_one_by_slug(uow=uow, employee_slug=slug)
    error_raiser_if_none(employee, 'Profile')
    answer_data = Base64Converter.key_to_base64(employee)
    return answer_data


@router.put('/{slug}/change', response_model=EmployeesReadDTO)
async def change_profile_put(
        slug: Annotated[str, Path(max_length=200)],
        uow: UOWDep,
        updated_employee: EmpUpdateFieldsDEP,
        photo: Annotated[UploadFile, File()],
):
    """Обновить данные профиля работника"""
    path: str = f'{path_start}{updated_employee["username"]}/'
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
        slug: Annotated[str, Path(max_length=200)],
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
            path: str = f'{path_start}{empl.username}/'
        else:
            path: str = f'{path_start}{updated_employee["username"]}/'
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


@router.get('/password/reset', include_in_schema=False)
async def password_reset():
    # Начало и отправка письма
    ...


@router.get('/password/reset/complete', include_in_schema=False)
async def password_reset():
    # оповещение об успешно сброшенном пароле
    ...


@router.get('/password/reset/starting', include_in_schema=False)
async def password_reset():
    # оповещение об отправленном письме
    ...


@router.get('/password/reset/confirm/{uidb}/{token}', include_in_schema=False)
async def password_reset(uidb: int, token: str):
    # сброс пароля
    ...


@router.get('/archive-report', include_in_schema=False)
async def get_archive_report():
    """Получение архивного отчёта"""
    # Celery
    ...


@router.post('/report/create', response_model=AccidentReadDTO, include_in_schema=False)
async def create_accident(uow: UOWDep, service: AccServiceDEP, accident_data: AccidentsCreateUpdateDTO):
    """Создание отчёта о происшествии"""
    # проверка есть ли такой автор и агрегат
    # is_author(uow, accident_data.author_id)
    accident_data.author_id = id
    # логика назначения автором текущего авторизованного пользователя
    is_object(uow, accident_data.object_id, service)
    new_accident = service.create_one(uow, accident_data)
    return new_accident


@router.patch('/report/update/{object_id}', response_model=AccidentReadDTO, include_in_schema=False)
async def update_crane_patch(
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
