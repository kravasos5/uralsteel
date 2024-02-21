from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import SecretStr

from dependencies import UOWDep
from schemas.auth import TokenInfo
from schemas.employees import EmployeeAuthReadDTO
from services.employees import EmployeesService
from utils import auth_utils


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


def validate_auth_employee(
    uow: UOWDep,
    username: Annotated[str, Form()],
    password: Annotated[SecretStr, Form()],
):
    """Валидация пользователя"""
    unauthed_exp = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Invalid username or password'
    )
    if not (employee := EmployeesService().retrieve_one_by_username(uow=uow, username=username)):
        raise unauthed_exp

    if not auth_utils.validate_password(
        password=password.get_secret_value(),
        hashed_password=employee.password
    ):
        raise unauthed_exp

    if not employee.is_active:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='User inactive'
        )

    return employee


@router.post('/login', response_model=TokenInfo)
def auth_employee(
    employee: Annotated[EmployeeAuthReadDTO, Depends(validate_auth_employee)],
):
    """Получить новый access token"""
    jwt_payload = {
        'sub': employee.id,
        'username': employee.username,
    }
    access_token = auth_utils.encode_jwt(
        payload=jwt_payload
    )
    return TokenInfo(
        access_token=access_token,
        token_type='Bearer',
    )