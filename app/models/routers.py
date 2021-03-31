from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.base import ClickDBModel, LinkBaseModel, LinkFullModel, LinkSettingsModel


class LinksCreateRequestModel(
    LinkSettingsModel,
    LinkBaseModel,
):
    alias: Optional[str] = Field(None, min_length=2, max_length=64)  # type: ignore


class LinksCreateResponseModel(
    LinkFullModel,
):
    ...


class PaginationModel(
    BaseModel,
):
    page: int
    per_page: int
    total: int


class LinksReadResponseModel(PaginationModel):
    links: List[LinkFullModel] = Field(default_factory=list)


class ClicksReadResponseModel(PaginationModel):
    from_ts: datetime
    to_ts: datetime
    clicks: List[ClickDBModel] = Field(default_factory=list)


class LinkPreviewResponseModel(LinkFullModel):
    ...


class LinksUpdateRequest(BaseModel):
    alias: str
    settings: LinkSettingsModel


class LinksUpdateResponseModel(
    LinkFullModel,
):
    ...
