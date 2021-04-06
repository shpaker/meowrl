from fastapi import APIRouter
from starlette.background import BackgroundTasks

from app.libs.healthz import call_health_checks
from app.models.routers.healthz import HealthzResponseSchema, RootResponse
from app.services import SERVICE_HEALTH_CHECKS
from app.settings import get_settings

healthz_router = APIRouter()
settings = get_settings()


@healthz_router.get(
    path="/",
    summary="Service version",
    response_model=RootResponse,
)
async def root_handler():
    return RootResponse(
        name=settings.title,
        version=settings.version,
    )


@healthz_router.get(
    path="/healthz",
    summary="Health check",
    response_model=HealthzResponseSchema,
)
async def healthz_handler(background_tasks: BackgroundTasks):
    return await call_health_checks(SERVICE_HEALTH_CHECKS, background_tasks)
