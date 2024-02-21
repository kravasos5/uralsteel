from fastapi import FastAPI

from routers import profile, auth
from routers import cranes as cranes_employee
from routers import ladles as ladles_employee
from routers.admin import admin

api = FastAPI()


api.include_router(auth.router)
api.include_router(profile.router)
api.include_router(cranes_employee.router)
api.include_router(ladles_employee.router)
api.include_router(admin.router)


@api.get("/")
async def root():
    return {"message": "Hello World"}
