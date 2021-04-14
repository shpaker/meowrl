from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.base import LinkBaseModel, LinkFullModel, LinkSettingsModel
from app.models.pagination import PaginationResponseModel
from app.settings import get_settings

settings = get_settings()


class LinkWithTagsModel(LinkFullModel):
    tags: List[str] = Field(default_factory=list)  # type: ignore


class LinksCreateRequestModel(
    LinkSettingsModel,
    LinkBaseModel,
):
    alias: Optional[str] = Field(None, min_length=2, max_length=64)  # type: ignore
    tags: List[str] = Field(default_factory=list, max_items=settings.tags.max_tags_by_link)  # type: ignore


class LinksCreateResponseModel(LinkWithTagsModel):
    ...


class LinksReadResponseModel(PaginationResponseModel):
    links: List[LinkWithTagsModel] = Field(default_factory=list)


class LinksUpdateRequestUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    archived: Optional[bool] = None


class LinksUpdateRequest(BaseModel):
    alias: str
    update: LinksUpdateRequestUpdateModel


class LinksUpdateResponseModel(
    LinkFullModel,
):
    ...
