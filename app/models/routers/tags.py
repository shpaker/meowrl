from pydantic import BaseModel, Field

from app.models.tags import TagModel
from app.settings import get_settings

settings = get_settings()


class TagsEnsureRequestModel(BaseModel):
    alias: str
    tag: str = Field(..., regex=settings.tags.regex)  # type: ignore


class TagsEnsureResponseModel(TagModel):
    ...


class TagsRemoveResponseModel(TagModel):
    ...
