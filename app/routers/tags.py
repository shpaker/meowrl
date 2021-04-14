from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from app.libs.links import read_link_by_alias
from app.libs.tags import ensure_tag, pull_aliases_from_tag, read_tags_for_link
from app.models.routers.tags import TagsEnsureRequestModel, TagsEnsureResponseModel, TagsRemoveResponseModel
from app.services.keycloak.depends import strict_bearer_auth
from app.services.keycloak.models import JWTTokenModel
from app.settings import get_settings

tags_router = APIRouter()
settings = get_settings()


@tags_router.post(
    "/",
    response_model=TagsEnsureResponseModel,
    description="Append tag to link",
)
async def add_handler(
    request: TagsEnsureRequestModel,
    token_payload: JWTTokenModel = Depends(strict_bearer_auth),
):
    link = await read_link_by_alias(request.alias)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    tags = await read_tags_for_link(request.alias)
    if len(tags) + 1 > settings.tags.max_tags_by_link:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"tag": "too much count of tags"})
    result = await ensure_tag(name=request.tag, owner=token_payload.sub, aliases=request.alias)
    return result


@tags_router.delete(
    "/",
    response_model=TagsRemoveResponseModel,
    description="Remove tag from link",
)
async def remove_handler(
    tag: str = Query(...),
    alias: str = Query(...),
    token_payload: JWTTokenModel = Depends(strict_bearer_auth),
):
    result = await pull_aliases_from_tag(name=tag, owner=token_payload.sub, aliases=alias)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result
