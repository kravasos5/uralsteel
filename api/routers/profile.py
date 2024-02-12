from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from dependencies import UOWDep
from schemas.employees import EmployeesReadDTO
from services.employees import EmployeesService
from utils.unitofwork import AbstractUnitOfWork

router = APIRouter(
    prefix="/profile",
    tags=["users"],
)


@router.get('/{slug}', response_model=EmployeesReadDTO)
def get_profile(slug: Annotated[str, Path(max_length=200)], uow: UOWDep):
    """Получить данные профиля пользователя"""
    user = EmployeesService().get_employee_by_slug(uow=uow, user_slug=slug)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user
