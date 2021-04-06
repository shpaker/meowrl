from datetime import datetime, timezone
from typing import Optional

from pydantic import UUID4, AnyUrl, BaseModel, Field


class PaginationModel(
    BaseModel,
):
    page: int
    per_page: int
    total: int


class LinkSettingsModel(
    BaseModel,
):
    title: Optional[str] = Field("")
    description: Optional[str] = Field("")
    archived: bool = Field(False)


class LinkBaseModel(
    BaseModel,
):
    url: AnyUrl
    alias: str = Field(..., min_length=2, max_length=64)


class LinkFullModel(
    LinkBaseModel,
    LinkSettingsModel,
):
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))


class LinkDbModel(
    LinkFullModel,
):
    owner: UUID4


class GeoIpModel(
    BaseModel,
):
    city_name: Optional[str]
    country_name: Optional[str]
    country_iso_code: Optional[str]


class ClickModel(
    BaseModel,
):
    alias: str
    ip_address: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    geo: Optional[GeoIpModel]


class ClickDBModel(
    ClickModel,
):
    ...
