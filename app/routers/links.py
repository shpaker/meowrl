from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from app.libs.links import create_link, read_link_by_url, read_user_links, update_link
from app.models.routers import (
    LinksCreateRequestModel,
    LinksCreateResponseModel,
    LinksReadResponseModel,
    LinksUpdateRequest,
    LinksUpdateResponseModel,
)
from app.services.keycloak.depends import strict_bearer_auth
from app.services.keycloak.models import JWTTokenModel
from app.settings import LinksFilterEnum, get_settings

links_router = APIRouter()
settings = get_settings()


@links_router.post(
    path="/",
    response_model=LinksCreateResponseModel,
    summary="Shorten a link",
)
async def create_link_handler(
    request: LinksCreateRequestModel,
    token_payload: JWTTokenModel = Depends(strict_bearer_auth),
):
    record = await read_link_by_url(owner=token_payload.sub, url=request.url, title=request.title)
    if record:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Already exists as {record.alias}",
        )
    record = await create_link(
        owner=token_payload.sub,
        url=request.url,
        title=request.title,
        description=request.description,
        alias=request.alias,
    )
    return record


@links_router.get(
    path="/",
    response_model=LinksReadResponseModel,
    summary="Read links created bu current user",
)
async def read_link_handler(
    page: int = Query(1, ge=1),
    per_page: int = Query(
        settings.pagination.per_page_default,
        ge=1,
        le=settings.pagination.per_page_maximum,
    ),
    links_filter: Optional[LinksFilterEnum] = Query(None, alias="filter"),
    token_payload: JWTTokenModel = Depends(strict_bearer_auth),  # noqa, pylint: disable=unused-argument
):
    page -= 1
    links, total = await read_user_links(
        owner=token_payload.sub,
        links_filter=links_filter,
        page=page,
        per_page=per_page,
    )
    return LinksReadResponseModel(
        page=page,
        per_page=per_page,
        total=total,
        links=links,  # type: ignore
    )


@links_router.patch(
    path="/",
    response_model=LinksUpdateResponseModel,
    summary="Update shorten link data",
)
async def update_link_handler(
    request: LinksUpdateRequest,
    token_payload: JWTTokenModel = Depends(strict_bearer_auth),  # noqa, pylint: disable=unused-argument
):
    updated = await update_link(alias=request.alias, **request.settings.dict())
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"alias": "unknown"},
        )
    return updated
