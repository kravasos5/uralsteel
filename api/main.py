from fastapi import FastAPI

from routers import profile

api = FastAPI()


api.include_router(profile.router)


@api.get("/")
async def root():
    return {"message": "Hello World"}