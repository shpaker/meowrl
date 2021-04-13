from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pydantic import UUID4, BaseModel, Field, constr, validator

from app.settings import get_settings

settings = get_settings()
TagNameType = constr(regex=settings.tags.regex)


class TagModel(BaseModel):
    name: TagNameType  # type: ignore
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updated_at: Optional[datetime] = None

    @validator("updated_at", pre=True, always=True)
    def updated_at_validate(  # pylint: disable=no-self-argument
        cls, updated_at: str, values: Dict[str, Any], **kwargs: Any  # noqa, pylint: disable=unused-argument
    ) -> str:
        if updated_at is None:
            updated_at = values.get("created_at")
        return updated_at


class TagDbModel(TagModel):
    owner: UUID4
    aliases: list[str] = Field(default_factory=list)
