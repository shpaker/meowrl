from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.base import LinkBaseModel, LinkFullModel, LinkSettingsModel, PaginationModel


class LinksCreateRequestModel(
    LinkSettingsModel,
    LinkBaseModel,
):
    alias: Optional[str] = Field(None, min_length=2, max_length=64)  # type: ignore


class LinksCreateResponseModel(
    LinkFullModel,
):
    ...


class LinksReadResponseModel(PaginationModel):
    links: List[LinkFullModel] = Field(default_factory=list)


class LinksUpdateRequest(BaseModel):
    alias: str
    settings: LinkSettingsModel


class LinksUpdateResponseModel(
    LinkFullModel,
):
    ...
