from fastapi import FastAPI

from routers import profile
from routers import cranes as cranes_employee
from routers import ladles as ladles_employee
from routers.admin import employees, accidents
from routers.admin import ladles as ladles_admin
from routers.admin import cranes as cranes_admin

api = FastAPI()


api.include_router(profile.router)
api.include_router(employees.router)
api.include_router(ladles_admin.router)
api.include_router(cranes_admin.router)
api.include_router(accidents.router)
api.include_router(cranes_employee.router)
api.include_router(ladles_employee.router)


@api.get("/")
async def root():
    return {"message": "Hello World"}
