import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from routers import profile, auth
from routers import cranes as cranes_employee
from routers import ladles as ladles_employee
from routers.admin import admin

api = FastAPI()

api.include_router(auth.router)
api.include_router(profile.router)
api.include_router(profile.password_reset_router)
api.include_router(cranes_employee.router)
api.include_router(ladles_employee.router)
api.include_router(admin.router)


@api.middleware('http')
async def put_patch_create_unique_constraint_handler(request: Request, call_next):
    """Отлавливает ошибку при несоблюдении уникальности столбца в бд"""
    try:
        # попытка выполнения эндпоинта
        response = await call_next(request)
        return response
    except IntegrityError as ex:
        # если ошибка IntegrityError, то пользователь ввёл неправильные данные
        # if isinstance(ex.orig, UniqueViolationError):
        if 'UniqueViolationError' in str(ex.orig):
            error_message = 'Unique violation'
        else:
            error_message = 'Invalid data'
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={'detail': error_message})


@api.get("/")
async def root():
    return {"message": "Hello World"}
