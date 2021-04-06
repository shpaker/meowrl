from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from app.libs.clicks import read_clicks
from app.libs.links import read_link_by_alias
from app.models.routers.clicks import ClicksReadResponseModel
from app.services.keycloak.depends import strict_bearer_auth
from app.services.keycloak.models import JWTTokenModel
from app.settings import get_settings

clicks_router = APIRouter()
settings = get_settings()


@clicks_router.get(
    "/",
    response_model=ClicksReadResponseModel,
    description="Read statistics by clicks from the specified time range",
)
async def range_handler(
    alias: str = Query(str),
    page: int = Query(1, ge=1),
    per_page: int = Query(
        settings.pagination.per_page_default,
        ge=1,
        le=settings.pagination.per_page_maximum,
    ),
    from_ts: Optional[datetime] = Query(None),
    to_ts: Optional[datetime] = Query(None),
    token_payload: JWTTokenModel = Depends(strict_bearer_auth),
):
    link = await read_link_by_alias(alias)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not link.owner == token_payload.sub:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if not to_ts:
        to_ts = datetime.now(timezone.utc)
    if not from_ts:
        from_ts = link.created_at
    common_params = dict(
        from_ts=from_ts,
        to_ts=to_ts,
        page=page,
        per_page=per_page,
    )
    clicks, total = await read_clicks(alias, **common_params)  # type: ignore
    return ClicksReadResponseModel(
        total=total,
        clicks=clicks,
        **common_params,  # type: ignore
    )
