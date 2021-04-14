from fastapi import Query

from app.models.pagination import PaginationParametersModel
from app.settings import get_settings

settings = get_settings()


async def pagination_parameters(
    page: int = Query(1, ge=1),
    per_page: int = Query(
        settings.pagination.per_page_default,
        ge=1,
        le=settings.pagination.per_page_maximum,
    ),
) -> PaginationParametersModel:
    return PaginationParametersModel(page=page - 1, per_page=per_page)
