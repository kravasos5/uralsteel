from http import HTTPStatus

from fastapi import APIRouter

from dependencies import UOWDep, GetIdDEP, error_raiser_if_none, JwtServiceDEP
from schemas.auth import RefreshTokenCreateUpdateDTO, RefreshTokenReadDTO, \
    RefreshTokenUpdatePatchDTO
from services.jwt import RefreshTokenService


router = APIRouter(
    prefix='/jwt',
)


@router.get('/tokens', response_model=list[RefreshTokenReadDTO])
async def get_tokens(
        uow: UOWDep,
        service: JwtServiceDEP,
        offset: int = 0,
        limit: int = 100,
):
    """Получение всех токенов"""
    tokens = await service.retrieve_all(uow, offset, limit)
    return tokens


@router.post('/create', response_model=RefreshTokenReadDTO)
async def create_token(
        uow: UOWDep,
        service: JwtServiceDEP,
        ladle_data: RefreshTokenCreateUpdateDTO,
):
    """Создание токена"""
    new_token = await service.create_one(uow, ladle_data)
    return new_token


@router.get('/{object_id}', response_model=RefreshTokenReadDTO)
async def get_token(uow: UOWDep, object_id: GetIdDEP, service: JwtServiceDEP):
    """Получение токена"""
    token = await service.retrieve_one(uow, id=object_id)
    await error_raiser_if_none(token)
    return token


@router.put('/update/{object_id}', response_model=RefreshTokenReadDTO)
async def update_token_put(
        uow: UOWDep,
        object_id: GetIdDEP,
        token_data: RefreshTokenCreateUpdateDTO,
        service: JwtServiceDEP,
):
    """Обновление токена методом put"""
    updated_token = await service.update_one(uow, token_data, id=object_id)
    await error_raiser_if_none(updated_token, 'token')
    return updated_token


@router.patch('/update/{object_id}', response_model=RefreshTokenReadDTO)
async def update_token_patch(
        uow: UOWDep,
        object_id: GetIdDEP,
        token_data: RefreshTokenUpdatePatchDTO,
        service: JwtServiceDEP,
):
    """Обновление токена методом patch"""
    updated_token = await service.update_one(uow, token_data, id=object_id)
    await error_raiser_if_none(updated_token, 'token')
    return updated_token


@router.delete('/delete/{object_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_ladle(uow: UOWDep, object_id: GetIdDEP, service: JwtServiceDEP):
    """Удаление токена по id"""
    deleted_token = await service.delete_one(uow, id=object_id)
    await error_raiser_if_none(deleted_token)
