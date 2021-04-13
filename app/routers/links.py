from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from app.libs.depends import pagination_parameters
from app.libs.links import create_link, read_link_by_url, read_user_links, update_link
from app.libs.tags import ensure_tag
from app.models.pagination import PaginationParametersModel
from app.models.routers.links import (
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
    status_code=status.HTTP_201_CREATED,
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
    response = LinksCreateResponseModel(**record.dict())
    for tag_name in request.tags:
        tag = await ensure_tag(name=tag_name, owner=token_payload.sub, aliases=record.alias)
        response.tags.append(tag)

    return response


@links_router.get(
    path="/",
    response_model=LinksReadResponseModel,
    summary="Read links created by current user",
)
async def read_link_handler(
    pagination: PaginationParametersModel = Depends(pagination_parameters),
    links_filter: Optional[LinksFilterEnum] = Query(None, alias="filter"),
    token_payload: JWTTokenModel = Depends(strict_bearer_auth),  # noqa, pylint: disable=unused-argument
):
    links, total = await read_user_links(
        owner=token_payload.sub,
        links_filter=links_filter,
        page=pagination.page,
        per_page=pagination.per_page,
    )
    return LinksReadResponseModel(
        page=pagination.page,
        per_page=pagination.per_page,
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
    updatable = dict((key, value) for key, value in request.update.dict().items() if value is not None)
    updated = await update_link(alias=request.alias, **updatable)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=dict(alias="unknown alias"),
        )
    return updated
