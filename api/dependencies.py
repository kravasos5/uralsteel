import datetime
from datetime import time
from enum import Enum
from http import HTTPStatus
from typing import Annotated, Any

from fastapi import Depends, Path, HTTPException, Query, Form, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt import InvalidTokenError
from pydantic import EmailStr, ValidationError
from cryptography.fernet import InvalidToken as InvalidResetToken

from models.employees import Posts
from schemas.aggregates import AggregatesUpdatePatchDTO
from schemas.auth import TokenScopesData
from schemas.cranes import CranesUpdatePatchDTO
from schemas.employees import EmployeesReadDTO, EmployeesAdminReadDTO, EmployeePasswordResetDTO, EmployeeResetPayloadDTO
from schemas.ladles import LadlesUpdatePatchDTO
from services.accidents import CranesAccidentService, LadlesAccidentService, AggregatesAccidentService
from services.cranes import CranesService
from services.dynamic import ActiveDynamicTableService, ArchiveDynamicTableService, LadleOperationTypes
from services.aggregates import AggregatesGMPService, AggregatesUKPService, AggregatesUVSService, \
    AggregatesMNLZService, AggregatesLService, AggregatesBurnerService, AggregatesAllService
from services.employees import EmployeesService
from services.jwt import RefreshTokenService
from services.ladles import LadlesService
from utils import auth_utils
from utils.service_base import ServiceBase
from utils.unitofwork import AbstractUnitOfWork, UnitOfWork
from utils import password_reset_utils


UOWDep = Annotated[AbstractUnitOfWork, Depends(UnitOfWork)]


async def get_object_id(object_id: Annotated[int, Path(gt=0)]):
    """object_id зависимость"""
    return object_id


GetIdDEP = Annotated[int, Depends(get_object_id)]


class AccidentType(str, Enum):
    """Типы инцидентов"""
    crane: str = 'Cranes'
    ladle: str = 'Ladles'
    aggregate: str = 'Aggregates'


async def get_accident_type(accident_type: Annotated[AccidentType, Query()]):
    """Зависимость типа инцидента"""
    return accident_type


GetAccTypeDEP = Annotated[AccidentType, Depends(get_accident_type)]


async def error_raiser_if_none(obj: Any, message_name: str = 'Object'):
    """Вызывает ошибку, если нет такого объекта"""
    if not obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"{message_name} not found"
        )


async def is_object(uow, object_id: int, service: ServiceBase, message: str = 'Object'):
    """Проверка есть ли объект с таким id"""
    obj = await service.retrieve_one(uow, id=object_id)
    await error_raiser_if_none(obj, message)


async def is_author_and_accident_object(
        uow: AbstractUnitOfWork,
        author_id: int,
        object_id: int,
        service: ServiceBase
):
    """Проверка наличия автора и агрегата с таким id"""
    await is_object(uow, author_id, EmployeesService(), 'Author')
    object_service = None
    if type(service) == AggregatesAccidentService:
        object_service = AggregatesAllService()
    elif type(service) == LadlesAccidentService:
        object_service = LadlesService()
    elif type(service) == CranesAccidentService:
        object_service = CranesService()
    await is_object(uow, object_id, object_service)


async def make_object_broken(
    uow: AbstractUnitOfWork,
    service: ServiceBase,
    object_id: int,
):
    """Отмечает объект сломанным при создании отчёта"""
    object_service = None
    object_schema = None
    if type(service) == AggregatesAccidentService:
        object_service = AggregatesAllService()
        object_schema = AggregatesUpdatePatchDTO(is_broken=True)
    elif type(service) == LadlesAccidentService:
        object_service = LadlesService()
        object_schema = LadlesUpdatePatchDTO(is_broken=True)
    elif type(service) == CranesAccidentService:
        object_service = CranesService()
        object_schema = CranesUpdatePatchDTO(is_broken=True)
    await object_service.update_one(uow, object_schema, id=object_id)


async def get_accident_service(acc_type: GetAccTypeDEP):
    """Зависимость сервиса происшествий"""
    service = None
    match acc_type:
        case AccidentType.crane:
            service = CranesAccidentService()
        case AccidentType.ladle:
            service = LadlesAccidentService()
        case AccidentType.aggregate:
            service = AggregatesAccidentService()
    return service


AccServiceDEP = Annotated[ServiceBase, Depends(get_accident_service)]


class AggregateType(str, Enum):
    """Перечисление агрегатов"""
    gmp: str = 'GMP'
    ukp: str = 'UKP'
    uvs: str = 'UVS'
    mnlz: str = 'MNLZ'
    l: str = 'L'
    burner: str = 'Burner'


async def get_aggregate_type(aggregate_type: Annotated[AggregateType, Query()]):
    """Зависимость типа агрегата"""
    return aggregate_type


GetAggTypeDEP = Annotated[AggregateType, Depends(get_aggregate_type)]


async def get_aggregate_service(agg_type: GetAggTypeDEP):
    """Зависимость сервиса агрегатов"""
    service = None
    match agg_type:
        case AggregateType.gmp:
            service = AggregatesGMPService()
        case AggregateType.ukp:
            service = AggregatesUKPService()
        case AggregateType.uvs:
            service = AggregatesUVSService()
        case AggregateType.mnlz:
            service = AggregatesMNLZService()
        case AggregateType.l:
            service = AggregatesLService()
        case AggregateType.burner:
            service = AggregatesBurnerService()
    return service


AggregatesServiceDEP = Annotated[ServiceBase, Depends(get_aggregate_service)]


class DynamicTableType(str, Enum):
    """Перечисление типов динамических таблиц"""
    active: str = 'active'
    archive: str = 'archive'


async def get_dynamic_type(dynamic_type: Annotated[DynamicTableType, Query()]):
    """Зависимость типов динамических таблиц"""
    return dynamic_type


GetDynTypeDEP = Annotated[DynamicTableType, Depends(get_dynamic_type)]


async def get_dynamic_service(dyn_type: GetDynTypeDEP):
    """Зависимость сервиса динамических таблиц"""
    service = None
    match dyn_type:
        case DynamicTableType.active:
            service = ActiveDynamicTableService()
        case DynamicTableType.archive:
            service = ArchiveDynamicTableService()
    return service


DynamicServiceDEP = Annotated[ServiceBase, Depends(get_dynamic_service)]


async def get_ladle_operation_type(ladle_operation_type: Annotated[LadleOperationTypes, Query()]):
    """Зависимость типов операций над ковшами"""
    return ladle_operation_type


GetOpTypeDEP = Annotated[LadleOperationTypes, Depends(get_ladle_operation_type)]


async def crane_fields_getter(
    title: Annotated[str, Form(max_length=100)],
    size_x: Annotated[int, Form(gt=0)],
    size_y: Annotated[int, Form(gt=0)],
    is_broken: Annotated[bool, Form()],
):
    """Зависимость полей кранов"""
    return dict(title=title, size_x=size_x,
                size_y=size_y, is_broken=is_broken)


CraneFieldsDEP = Annotated[dict, Depends(crane_fields_getter)]


async def crane_fields_patch_getter(
    title: Annotated[str | None, Form(max_length=100)] = None,
    size_x: Annotated[int | None, Form(gt=0)] = None,
    size_y: Annotated[int | None, Form(gt=0)] = None,
    is_broken: Annotated[bool | None, Form()] = None,
):
    """Зависимость полей кранов"""
    return dict(title=title, size_x=size_x,
                size_y=size_y, is_broken=is_broken)


CraneFieldsPatchDEP = Annotated[dict, Depends(crane_fields_patch_getter)]


async def aggregates_fields_getter(
    title: Annotated[str, Form(max_length=100)],
    num_agg: Annotated[str, Form(max_length=100)],
    num_pos: Annotated[str, Form(max_length=100)],
    coord_x: Annotated[int, Form(gt=0)],
    coord_y: Annotated[int, Form(gt=0)],
    stay_time: Annotated[time, Form()],
    is_broken: Annotated[bool, Form()] = False,
):
    """Зависимость полей агрегатов"""
    return dict(
        title=title,
        num_agg=num_agg,
        num_pos=num_pos,
        coord_x=coord_x,
        coord_y=coord_y,
        stay_time=stay_time,
        is_broken=is_broken,
    )


AggFieldsDEP = Annotated[dict, Depends(aggregates_fields_getter)]


async def aggregates_fields_patch_getter(
    title: Annotated[str | None, Form(max_length=100)] = None,
    num_agg: Annotated[str | None, Form(max_length=100)] = None,
    num_pos: Annotated[str | None, Form(max_length=100)] = None,
    coord_x: Annotated[int | None, Form(gt=0)] = None,
    coord_y: Annotated[int | None, Form(gt=0)] = None,
    stay_time: Annotated[time | None, Form()] = None,
    is_broken: Annotated[bool | None, Form()] = None,
):
    """Зависимость полей агрегатов для метода patch"""
    return dict(
        title=title,
        num_agg=num_agg,
        num_pos=num_pos,
        coord_x=coord_x,
        coord_y=coord_y,
        stay_time=stay_time,
        is_broken=is_broken,
    )


AggFieldsPatchDEP = Annotated[dict, Depends(aggregates_fields_patch_getter)]


async def employees_create_fields_getter(
    email: Annotated[EmailStr, Form(max_length=254)],
    username: Annotated[str, Form(max_length=150)],
    password: Annotated[str, Form(max_length=128)],
    first_name: Annotated[str, Form(max_length=150)],
    last_name: Annotated[str, Form(max_length=150)],
    patronymic: Annotated[str, Form(max_length=100)],
    send_messages: Annotated[bool, Form()],
    slug: Annotated[str, Form(max_length=200)],
    post: Annotated[Posts, Form()],
):
    """Зависимость полей работника post"""
    return dict(
        email=email,
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic,
        send_messages=send_messages,
        slug=slug,
        post=post,
    )


EmpCreateFieldsDEP = Annotated[dict, Depends(employees_create_fields_getter)]


async def employees_update_fields_getter(
    email: Annotated[EmailStr, Form(max_length=254)],
    username: Annotated[str, Form(max_length=150)],
    first_name: Annotated[str, Form(max_length=150)],
    last_name: Annotated[str, Form(max_length=150)],
    patronymic: Annotated[str, Form(max_length=100)],
    send_messages: Annotated[bool, Form()],
    post: Annotated[Posts, Form()],
):
    """Зависимость полей работника put"""
    return dict(
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic,
        send_messages=send_messages,
        post=post,
    )


EmpUpdateFieldsDEP = Annotated[dict, Depends(employees_update_fields_getter)]


async def employees_update_fields_patch_getter(
        email: Annotated[EmailStr | None, Form(max_length=254)] = None,
        username: Annotated[str | None, Form(max_length=150)] = None,
        first_name: Annotated[str | None, Form(max_length=150)] = None,
        last_name: Annotated[str | None, Form(max_length=150)] = None,
        patronymic: Annotated[str | None, Form(max_length=100)] = None,
        send_messages: Annotated[bool | None, Form()] = None,
        post: Annotated[Posts | None, Form()] = None,
):
    """Зависимость полей работника patch"""
    return dict(
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic,
        send_messages=send_messages,
        post=post,
    )


EmpUpdatePatchFieldsDEP = Annotated[dict, Depends(employees_update_fields_patch_getter)]


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/auth/login',
    # scopes={
    #     'employee': 'Employee permissions. Read, update yourself info, \
    #                 get cranes, ladles location info and create reports',
    #     'admin': 'All permissions.'
    # },
)


invalid_token_exception = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED,
    detail='Invalid token',
    headers={'WWW-Authenticate': 'Bearer'},
)


inactive_user_exception = HTTPException(
    status_code=HTTPStatus.FORBIDDEN,
    detail='Employee inactive'
)


access_denied = HTTPException(
    status_code=HTTPStatus.FORBIDDEN,
    detail='Access denied'
)


async def get_current_token_payload(
    uow: UOWDep,
    token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    """Получить payload токена работника"""
    try:
        payload = auth_utils.decode_jwt(
            token=token
        )
    except InvalidTokenError:
        print('get_current_token_payload')
        print('get_current_token_payload')
        print('get_current_token_payload')
        print('get_current_token_payload')
        print('get_current_token_payload')
        raise invalid_token_exception
    # проверка нет ли токена в blacklist
    if await RefreshTokenService().check_token(uow, token, payload.get('token_family')):
        print('get_current_token_payload 111111111111')
        print('get_current_token_payload 111111111111')
        print('get_current_token_payload 111111111111')
        print('get_current_token_payload 111111111111')
        print('get_current_token_payload 111111111111')
        raise invalid_token_exception
    return payload


async def get_current_auth_user(
    security_scopes: SecurityScopes,
    payload: Annotated[dict, Depends(get_current_token_payload)],
    uow: UOWDep,
) -> EmployeesReadDTO:
    """Получить работника по payload токена"""
    # получение данных о scopes для информации ошибки
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = 'Bearer'
    invalid_token_scopes_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Invalid token',
        headers={'WWW-Authenticate': authenticate_value},
    )
    # валидация scopes и id
    try:
        employee_id: int | None = payload.get('sub')
        scopes: list[str] = payload.get('scopes')
        token_data = TokenScopesData(scopes=scopes, id=employee_id)
    except ValidationError:
        print('get_current_auth_user')
        print('get_current_auth_user')
        print('get_current_auth_user')
        print('get_current_auth_user')
        print('get_current_auth_user')
        raise invalid_token_scopes_exception
    # проверка прав доступа
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Access denied',
                headers={'WWW-Authenticate': authenticate_value},
            )
    # если получилось найти такого пользователя, то вернуть его
    if employee := await EmployeesService().retrieve_one_by_id(uow, token_data.id):
        return employee
    # otherwise вызвать ошибку
    print('get_current_auth_user 1111111111')
    print('get_current_auth_user 1111111111')
    print('get_current_auth_user 1111111111')
    print('get_current_auth_user 1111111111')
    print('get_current_auth_user 1111111111')
    raise invalid_token_exception


async def get_current_active_auth_user(
    employee: Annotated[EmployeesReadDTO, Security(get_current_auth_user, scopes=['employee'])]
) -> EmployeesReadDTO:
    """Получить активного аутентифицированного работника"""
    if employee.is_active:
        return employee
    raise inactive_user_exception


async def get_change_by_slug_permission(
    slug: Annotated[str, Path(max_length=200)],
    cur_employee: Annotated[EmployeesReadDTO, Depends(get_current_active_auth_user)]
):
    """Проверка доступа к функционалу изменения"""
    if cur_employee.slug != slug:
        raise access_denied
    return slug


employeeSlugPermissionDEP = Annotated[EmployeesReadDTO, Depends(get_change_by_slug_permission)]


async def get_admin_permission(
    cur_employee: Annotated[EmployeesAdminReadDTO, Security(get_current_auth_user, scopes=['admin'])]
):
    """Получение доступа к админ контроллерам"""
    pass


AdminPermissionDEP = Depends(get_admin_permission)


async def validate_email(
    uow: UOWDep,
    email: Annotated[EmailStr, Form(max_length=254)]
):
    """Проверка email"""
    if await EmployeesService().retrieve_one(uow, email=email):
        return email
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail="Employee with that email doesn't exist",
    )


emailDEP = Annotated[str, Depends(validate_email)]


async def validate_passwords(
    password: Annotated[str, Form(max_length=128)],
    new_password: Annotated[str, Form(max_length=128)],
) -> EmployeePasswordResetDTO:
    """Валидировать 2 пароля при смене паролей"""
    if password != new_password:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Passwords are different',
        )
    hashed_password = await EmployeesService().hash_password(password)
    return EmployeePasswordResetDTO(password=hashed_password)


ResetPasswordDEP = Annotated[str, Depends(validate_passwords)]


async def validate_reset_token(token: Annotated[str, Path()]) -> EmployeeResetPayloadDTO:
    """Валидация reset токена"""
    invalid_reset_token_exception = HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail='Invalid token',
    )
    try:
        payload = password_reset_utils.decode_token(token)
    except InvalidResetToken:
        raise invalid_reset_token_exception
    # проверка не истёк ли токен
    expire_date = datetime.datetime.fromtimestamp(payload.get('exp'))
    now = datetime.datetime.now()
    if expire_date < now:
        raise invalid_reset_token_exception
    return EmployeeResetPayloadDTO(**payload)


ResetPayloadDEP = Annotated[EmployeeResetPayloadDTO, Depends(validate_reset_token)]
