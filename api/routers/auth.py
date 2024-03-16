import datetime
import uuid
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import SecretStr

from dependencies import UOWDep, oauth2_scheme, invalid_token_exception
from schemas.auth import TokenInfo, RefreshTokenCreateUpdateDTO, RefreshTokenBaseDTO
from schemas.employees import EmployeeAuthReadDTO
from services.employees import EmployeesService
from services.jwt import RefreshTokenService, RefreshTokenBlacklistService
from utils import auth_utils
from utils.unitofwork import AbstractUnitOfWork

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


async def validate_auth_employee(
    uow: UOWDep,
    username: Annotated[str, Form()],
    password: Annotated[SecretStr, Form()],
):
    """Валидация пользователя"""
    unauthed_exp = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Invalid username or password'
    )
    if not (employee := await EmployeesService().retrieve_one_by_username(uow=uow, username=username)):
        raise unauthed_exp

    if not auth_utils.validate_password(
        password=password.get_secret_value(),
        hashed_password=employee.password
    ):
        raise unauthed_exp

    if not employee.is_active:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Employee inactive'
        )

    return employee


async def create_tokens(
    jwt_payload: dict,
    uow: AbstractUnitOfWork,
) -> TokenInfo:
    """Функция создания refresh и access токенов"""
    # создание access_token
    access_token = auth_utils.encode_jwt(
        payload=jwt_payload
    )[0]
    # создание refresh_token
    refresh_token, expire = auth_utils.encode_jwt(
        payload=jwt_payload,
        is_refresh=True,
    )
    # получаю схему refresh_token
    refresh_token_create_schema = RefreshTokenCreateUpdateDTO(
        refresh_token=refresh_token,
        expire_date=expire,
        token_family=jwt_payload.get('token_family'),
        employee_id=jwt_payload.get('sub'),
    )
    # сохраняю refresh_token в бд
    await RefreshTokenService().create_one(uow, refresh_token_create_schema)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='Bearer',
    )


@router.post('/login', response_model=TokenInfo)
async def auth_employee(
    employee: Annotated[EmployeeAuthReadDTO, Depends(validate_auth_employee)],
    uow: UOWDep,
):
    """Получить новый access и refresh tokens"""
    scopes = ['employee']
    if employee.is_superuser:
        scopes.append('admin')

    token_family = uuid.uuid4()

    jwt_payload = {
        'sub': employee.id,
        'scopes': scopes,
        'token_family': str(token_family),
    }
    answer = await create_tokens(jwt_payload, uow)
    return answer


@router.post('/refresh', response_model=TokenInfo)
async def refresh_tokens(
    refresh_token: str,
    uow: UOWDep,
):
    """Получить новые access и refresh токены"""
    # расшифровать refresh
    payload = auth_utils.decode_jwt(refresh_token)
    token_family: str | None = payload.get('token_family')
    scopes = payload.get('scopes')
    employee_id = payload.get('sub')
    if not (employee_id and token_family):
        raise invalid_token_exception
    # инициализация сервисов
    rt_service = RefreshTokenService()
    # проверяю есть ли этот токен в blacklist, если есть, то заношу
    # всё семейство в blacklist
    if await rt_service.check_token(uow, refresh_token, token_family):
        await rt_service.delete_family(uow, token_family)
        raise invalid_token_exception
    # если токен используется впервые, то выполняю стандартные действия
    else:
        # переношу текущий токен в чёрный список и удаляю из таблицы токенов
        await rt_service.transfer_to_blacklist(
            uow,
            refresh_token,
            employee_id,
            token_family,
        )
        # создаю новый access и refresh токены
        jwt_payload = {
            'sub': employee_id,
            'scopes': scopes,
            'token_family': token_family,
        }

        answer = await create_tokens(jwt_payload, uow)
        return answer


@router.post('/logout', status_code=HTTPStatus.NO_CONTENT)
async def logout(
    uow: UOWDep,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    """Выйти из учётной записи"""
    # добавить refresh_token в black_list
    # расшифровать access_token
    payload = auth_utils.decode_jwt(token)
    token_family = payload.get('token_family')
    # занести в чёрный список семейство refresh_token
    await RefreshTokenService().delete_family(uow, token_family)
    # занести в чёрный список текущий access токен
    creation_bl_schema = RefreshTokenBaseDTO(
        refresh_token=token,
        expire_date=datetime.datetime.fromtimestamp(payload.get('exp')),
        token_family=payload.get('token_family'),
    )
    await RefreshTokenBlacklistService().create_one(
        uow,
        creation_bl_schema
    )
