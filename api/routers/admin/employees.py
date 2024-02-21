from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Path, UploadFile, File

from dependencies import UOWDep, error_raiser_if_none, EmpCreateFieldsDEP, EmpUpdateFieldsDEP, EmpUpdatePatchFieldsDEP
from schemas.employees import EmployeesReadDTO, EmployeesCreateDTO, EmployeesUpdateDTO, EmployeesPatchUpdateDTO
from services.employees import EmployeesService
from utils.utilities import Base64Converter, PhotoAddToSchema

router = APIRouter(
    prefix='/employee',
)


path_start: str = 'photos/'


@router.get('/employees', response_model=list[EmployeesReadDTO])
async def get_employees(uow: UOWDep, offset: int = 0, limit: int = 100):
    """Получить работников"""
    employees = EmployeesService().retrieve_all(uow, offset, limit)
    answer_data = Base64Converter.key_to_base64(employees, is_list=True)
    return answer_data


@router.post('/create', response_model=EmployeesReadDTO)
async def create_employee(
    uow: UOWDep,
    new_user: EmpCreateFieldsDEP,
    photo: Annotated[UploadFile, File()]
):
    """Создание нового работника"""
    path: str = f'{path_start}{new_user["username"]}/'
    create_data = await PhotoAddToSchema.file_add(
        photo, path, new_user, EmployeesCreateDTO,
        create_dir=True, created_dir=path
    )
    employee = EmployeesService().create_one(uow, create_data)
    answer_data = Base64Converter.key_to_base64(employee)
    return answer_data


@router.delete('/delete/{employee_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_employee(uow: UOWDep, employee_id: int):
    """Удаление работника"""
    deleted_employee = EmployeesService().delete_one(uow, id=employee_id)
    error_raiser_if_none(deleted_employee, 'Employee')


@router.put('/{employee_id}/change', response_model=EmployeesReadDTO)
async def change_employee_put(
        employee_id: Annotated[int, Path(gt=0)],
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
    employee = EmployeesService().update_one(uow=uow, data_schema=update_data, id=employee_id)
    error_raiser_if_none(employee, 'Employee')
    answer_data = Base64Converter.key_to_base64(employee)
    return answer_data


@router.patch('/{employee_id}/change', response_model=EmployeesReadDTO)
async def change_employee_patch(
        employee_id: Annotated[int, Path(gt=0)],
        uow: UOWDep,
        updated_employee: EmpUpdatePatchFieldsDEP,
        photo: Annotated[UploadFile, File()] = None,
):
    """Обновить данные профиля работника"""
    service = EmployeesService()
    updated_employee = {key: value for key, value in updated_employee.items() if value is not None}
    if photo:
        if 'username' not in updated_employee:
            empl = service.retrieve_one_by_id(uow, employee_id)
            path: str = f'{path_start}{empl.username}/'
        else:
            path: str = f'{path_start}{updated_employee["username"]}/'
        update_data = await PhotoAddToSchema.file_add(
            photo, path, updated_employee, EmployeesPatchUpdateDTO,
            create_dir=True, created_dir=path
        )
    else:
        update_data = EmployeesPatchUpdateDTO(**updated_employee)
    employee = service.update_one(uow=uow, data_schema=update_data, id=employee_id)
    error_raiser_if_none(employee, 'Employee')
    answer_data = Base64Converter.key_to_base64(employee)
    return answer_data


@router.get('/{employee_id}', response_model=EmployeesReadDTO)
async def get_employee(employee_id: Annotated[int, Path(gt=0)], uow: UOWDep):
    """Получить данные работника"""
    employee = EmployeesService().retrieve_one_by_id(uow=uow, employee_id=employee_id)
    error_raiser_if_none(employee, 'Employee')
    answer_data = Base64Converter.key_to_base64(employee)
    return answer_data
