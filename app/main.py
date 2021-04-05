from functools import lru_cache
from logging import DEBUG, INFO, basicConfig, getLogger

from fastapi import FastAPI
from uvicorn import run

from app.routers.links import links_router
from app.routers.redirect import redirect_router
from app.services.geoip2.wrapper import GeoIP2Wrapper
from app.services.keycloak.wrapper import KeycloakWrapper
from app.services.mongodb.indexes import create_mongodb_indexes
from app.services.mongodb.wrapper import MongoDBWrapper
from app.settings import get_settings

settings = get_settings()
basicConfig(level=DEBUG if settings.debug else INFO)
logger = getLogger(__name__)


def add_event_handlers(app: FastAPI) -> None:
    wrappers = (
        MongoDBWrapper(),
        KeycloakWrapper(),
        GeoIP2Wrapper(),
    )
    for wrapper in wrappers:
        app.add_event_handler("startup", wrapper.startup_event_handler)
        app.add_event_handler("shutdown", wrapper.shutdown_event_handler)
    app.add_event_handler("startup", create_mongodb_indexes)


def add_routers(app: FastAPI) -> None:
    app.include_router(router=links_router, prefix="/links")
    app.include_router(router=redirect_router, prefix="/r")


def add_middlewares(app: FastAPI) -> None:  # pylint: disable=unused-argument
    ...


@lru_cache
def create_app() -> FastAPI:
    app = FastAPI(title=settings.title, version=settings.version, debug=settings.debug)
    add_event_handlers(app)
    add_routers(app)
    add_middlewares(app)
    return app


def main() -> None:
    logger.info(f"Start {settings.title} {settings.version} http://{settings.host}:{settings.port}")
    logger.debug(f"=== DEBUG IS {str(settings.debug).upper()} ===")
    run(app="app:app", log_level="warning")
