from fastapi import APIRouter

from dependencies import AdminPermissionDEP

from . import (
    accidents,
    aggregates,
    brandsteel,
    cranes,
    dynamics,
    employees,
    ladles,
    routes,
    jwt,
)


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[AdminPermissionDEP],
)


router.include_router(accidents.router)
router.include_router(aggregates.router)
router.include_router(brandsteel.router)
router.include_router(cranes.router)
router.include_router(dynamics.router)
router.include_router(employees.router)
router.include_router(ladles.router)
router.include_router(routes.router)
router.include_router(jwt.router)
