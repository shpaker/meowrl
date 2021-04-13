from datetime import datetime
from typing import List

from pydantic import Field

from app.models.base import ClickDBModel
from app.models.pagination import PaginationResponseModel


class ClicksReadResponseModel(PaginationResponseModel):
    from_ts: datetime
    to_ts: datetime
    clicks: List[ClickDBModel] = Field(default_factory=list)
