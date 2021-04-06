from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from starlette import status
from starlette.responses import RedirectResponse

from app.libs.clicks import create_click, read_clicks
from app.libs.links import read_link_by_alias
from app.models.routers.clicks import ClicksReadResponseModel
from app.models.routers.links import LinkPreviewResponseModel
from app.services.keycloak.depends import strict_bearer_auth
from app.services.keycloak.models import JWTTokenModel
from app.settings import get_settings

redirect_router = APIRouter()
settings = get_settings()


@redirect_router.get("/{alias}")
async def follow_url_handler(
    request: Request,
    alias: str = Path(str),
):
    record = await read_link_by_alias(alias)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if record.archived:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await create_click(alias, request.client.host)
    return RedirectResponse(url=record.url)


@redirect_router.get("/{alias}/clicks", response_model=ClicksReadResponseModel)
async def read_clicks_handler(
    alias: str = Path(str),
    page: int = Query(1, ge=1),
    per_page: int = Query(
        settings.pagination.per_page_default,
        ge=1,
        le=settings.pagination.per_page_maximum,
    ),
    from_ts: Optional[datetime] = Query(None),
    to_ts: Optional[datetime] = Query(None),
    token_payload: JWTTokenModel = Depends(strict_bearer_auth),  # noqa, pylint: disable=unused-argument
):
    if not to_ts:
        to_ts = datetime.now(timezone.utc)
    if not from_ts:
        from_ts = to_ts - settings.clicks.time_range_default
    clicks, total = await read_clicks(
        alias,
        from_ts=from_ts,
        to_ts=to_ts,
        page=page,
        per_page=per_page,
    )
    return ClicksReadResponseModel(
        from_ts=from_ts,
        to_ts=to_ts,
        page=page,
        per_page=per_page,
        total=total,
        clicks=clicks,
    )


@redirect_router.get("/{alias}/preview", response_model=LinkPreviewResponseModel)
async def preview_handler(
    alias: str = Path(str),
):
    record = await read_link_by_alias(alias)
    if not record or record.archived:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return record
