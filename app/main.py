from functools import lru_cache
from logging import DEBUG, INFO, basicConfig, getLogger
from typing import Dict, Optional

from fastapi import FastAPI
from uvicorn import run

from app.routers.clicks import clicks_router
from app.routers.healthz import healthz_router
from app.routers.links import links_router
from app.routers.redirect import redirect_router
from app.services import SERVICE_WRAPPERS
from app.services.mongodb.indexes import create_mongodb_indexes
from app.settings import get_settings

settings = get_settings()
basicConfig(level=DEBUG if settings.debug else INFO)
logger = getLogger(__name__)


def add_event_handlers(app: FastAPI) -> None:
    for wrapper in SERVICE_WRAPPERS:
        app.add_event_handler("startup", wrapper.startup_event_handler)
        app.add_event_handler("shutdown", wrapper.shutdown_event_handler)
    app.add_event_handler("startup", create_mongodb_indexes)


def add_routers(app: FastAPI) -> None:
    app.include_router(router=links_router, prefix="/links", tags=["Links"])
    app.include_router(router=clicks_router, prefix="/clicks", tags=["Clicks"])
    app.include_router(router=redirect_router, prefix="/r", tags=["Redirect"])
    app.include_router(router=healthz_router, tags=["Health Checks"])


def add_middlewares(app: FastAPI) -> None:  # pylint: disable=unused-argument
    ...


@lru_cache
def create_app() -> FastAPI:
    params: Dict[str, Optional[str]] = dict()
    if settings.enable_specs:
        params.update(openapi_url=settings.specs.openapi, redoc_url=settings.specs.redoc)
    app = FastAPI(
        title=settings.title,
        version=settings.version,
        debug=settings.debug,
        docs_url=None,
        **params,  # type: ignore
    )
    add_event_handlers(app)
    add_routers(app)
    add_middlewares(app)
    return app


def main() -> None:
    logger.info(f"Start {settings.title} {settings.version} http://{settings.host}:{settings.port}")
    logger.debug(f"=== DEBUG IS {str(settings.debug).upper()} ===")
    run(
        app="app:app",
        host=settings.host,
        port=settings.port,
        log_level="warning",
    )
