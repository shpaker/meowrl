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
    clicks_collection: str = "clicks"
    links_collection: str = "links"
    tags_collection: str = "tags"


class PaginationSubSettings(BaseModel):
    per_page_default: int = 16
    per_page_maximum: int = 64


class ClicksSubSettings(BaseModel):
    time_range_default: timedelta = timedelta(weeks=1)


class TagsSubSettings(BaseModel):
    regex: str = r"^([^ ][а-яА-Яa-zA-Z\d_ ]*[^ ])$"
    min_length: int = 2
    max_length: int = 64
    max_tags_by_link: int = 8


class SpecsUrlsSubSettings(BaseModel):
    redoc: str = "/api"
    openapi: str = "/api.json"


class Settings(ServiceSettingsBase):
    title: str = "meowrl"
    version: str = "0.1.0"
    host: str = "0.0.0.0"
    port: int = 8000
    root_path: str = ""
    debug: bool = False
    enable_specs: bool = False

    mongodb: MongoDBSubSettings = MongoDBSubSettings()
    pagination: PaginationSubSettings = PaginationSubSettings()
    clicks: ClicksSubSettings = ClicksSubSettings()
    specs: SpecsUrlsSubSettings = SpecsUrlsSubSettings()
    tags: TagsSubSettings = TagsSubSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
