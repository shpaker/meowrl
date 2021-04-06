from fastapi import APIRouter, HTTPException, Path, Request
from starlette import status
from starlette.responses import RedirectResponse

from app.libs.clicks import create_click
from app.libs.links import read_link_by_alias
from app.settings import get_settings

redirect_router = APIRouter()
settings = get_settings()


@redirect_router.get("/{alias}")
async def follow_url_handler(
    request: Request,
    alias: str = Path(...),
):
    record = await read_link_by_alias(alias)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if record.archived:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await create_click(alias, request.client.host)
    return RedirectResponse(url=record.url)
