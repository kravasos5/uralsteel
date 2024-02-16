from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Path

from dependencies import UOWDep, error_raiser_if_none
from schemas.employees import EmployeesReadDTO, EmployeesCreateDTO, EmployeesUpdateDTO, EmployeesPatchUpdateDTO
from services.employees import EmployeesService

router = APIRouter(
    prefix="/admin/employee",
    tags=["admin"],
)


@router.get('/employees', response_model=list[EmployeesReadDTO])
def get_employees(uow: UOWDep, offset: int = 0, limit: int = 100):
    """Получить работников"""
    employees = EmployeesService().retrieve_all(uow, offset, limit)
    return employees


@router.post('/create', response_model=EmployeesReadDTO)
def create_employee(uow: UOWDep, new_user: EmployeesCreateDTO):
    """Создание нового работника"""
    employee = EmployeesService().create_one(uow, new_user)
    return employee


@router.delete('/delete/{employee_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_employee(uow: UOWDep, employee_id: int):
    """Удаление работника"""
    deleted_employee = EmployeesService().delete_one(uow, id=employee_id)
    error_raiser_if_none(deleted_employee, 'Employee')


@router.put('/{employee_id}/change', response_model=EmployeesReadDTO)
def change_employee_put(
        employee_id: Annotated[int, Path(gt=0)],
        uow: UOWDep,
        updated_employee: EmployeesUpdateDTO,
):
    """Обновить данные профиля работника"""
    employee = EmployeesService().update_one(uow=uow, data_schema=updated_employee, id=employee_id)
    error_raiser_if_none(employee, 'Employee')
    return employee


@router.patch('/{employee_id}/change', response_model=EmployeesReadDTO)
def change_employee_patch(
        employee_id: Annotated[int, Path(gt=0)],
        uow: UOWDep,
        updated_employee: EmployeesPatchUpdateDTO,
):
    """Обновить данные профиля работника"""
    employee = EmployeesService().update_one(uow=uow, data_schema=updated_employee, id=employee_id)
    error_raiser_if_none(employee, 'Employee')
    return employee


@router.get('/{employee_id}', response_model=EmployeesReadDTO)
def get_employee(employee_id: Annotated[int, Path(gt=0)], uow: UOWDep):
    """Получить данные работника"""
    employee = EmployeesService().retrieve_one_by_id(uow=uow, employee_id=employee_id)
    error_raiser_if_none(employee, 'Employee')
    return employee
