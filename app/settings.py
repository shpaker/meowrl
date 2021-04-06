from datetime import timedelta
from enum import Enum
from functools import lru_cache

from pydantic import BaseModel

from app.utils import ServiceSettingsBase


class LinksFilterEnum(str, Enum):
    ARCHIVED = "archived"
    ACTIVE = "active"


class MongoDBSubSettings(BaseModel):
    database: str = "meowrl"
    links_collection: str = "links"
    clicks_collection: str = "clicks"


class PaginationSubSettings(BaseModel):
    per_page_default: int = 16
    per_page_maximum: int = 64


class ClicksSubSettings(BaseModel):
    time_range_default: timedelta = timedelta(weeks=1)


class SpecsUrlsSubSettings(BaseModel):
    redoc: str = "/api"
    openapi: str = "/api.json"


class Settings(ServiceSettingsBase):

    title: str = "meowrl"
    version: str = "0.1.0"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    enable_specs: bool = False

    mongodb: MongoDBSubSettings = MongoDBSubSettings()
    pagination: PaginationSubSettings = PaginationSubSettings()
    clicks: ClicksSubSettings = ClicksSubSettings()
    specs: SpecsUrlsSubSettings = SpecsUrlsSubSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
