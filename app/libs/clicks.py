from datetime import datetime
from logging import getLogger
from typing import Any, Dict, List, Optional, Tuple

from geoip2.errors import GeoIP2Error  # pylint: disable=import-error
from pymongo import ASCENDING

from app.models.base import ClickDBModel, GeoIpModel
from app.services.geoip2.depends import get_geoip2_client
from app.services.mongodb.depends import get_clicks_collection, mongodb_paginated_find

logger = getLogger(__name__)


async def clicks_count(query: Optional[Dict[str, Any]] = None) -> int:
    if not query:
        query = dict()
    collection = get_clicks_collection()
    return await collection.count_documents(query)  # type: ignore


async def create_click(
    alias: str,
    ip_address: str,
) -> ClickDBModel:
    collection = get_clicks_collection()
    geoip2_client = get_geoip2_client()
    geoip_data = None
    try:
        if geoip2_client:
            response = await geoip2_client.city(ip_address)
            geoip_data = GeoIpModel(
                city_name=response.city.name,
                country_name=response.country.name,
                country_iso_code=response.country.iso_code,
            )
    except GeoIP2Error as err:
        logger.error(f"GeoIP2 error: {err}", exc_info=err)

    data = ClickDBModel(
        alias=alias,
        ip_address=ip_address,  # noqa
        geo=geoip_data,
    )
    await collection.insert_one(data.dict())
    return data


async def read_clicks(
    alias: str,
    *,
    from_ts: datetime,
    to_ts: datetime,
    page: int,
    per_page: int,
) -> Tuple[List[ClickDBModel], int]:
    query = {
        "alias": alias,
        "$and": [
            dict(created_at={"$gte": from_ts}),
            dict(created_at={"$lt": to_ts}),
        ],
    }
    collection = get_clicks_collection()
    total = await clicks_count(query)
    documents = await mongodb_paginated_find(
        collection=collection,
        query=query,
        page=page,
        per_page=per_page,
        sort=[("created_at", ASCENDING)],
    )
    return [ClickDBModel(**doc) for doc in documents], total
