from typing import Any, Dict, List, Optional, Tuple

from fastapi import Query
from hashids import Hashids
from pydantic import UUID4, AnyUrl
from pymongo import DESCENDING
from pymongo.results import UpdateResult

from app.libs.tags import read_tag
from app.models.base import LinkDbModel
from app.services.mongodb.depends import get_links_collection, mongodb_paginated_find
from app.settings import LinksFilterEnum, get_settings

hashids = Hashids()
settings = get_settings()


async def links_count(query: Optional[Dict[str, Any]] = None) -> int:
    if not query:
        query = dict()
    collection = get_links_collection()
    return await collection.count_documents(query)  # type: ignore


async def read_link_by_url(
    owner: UUID4,
    url: AnyUrl,
    title: Optional[str],
) -> Optional[LinkDbModel]:
    collection = get_links_collection()
    req_filter = {
        "$and": [
            dict(url={"$eq": url}),
            dict(owner={"$eq": owner}),
            dict(title={"$eq": title}),
        ]
    }
    document = await collection.find_one(req_filter)
    return LinkDbModel(**document) if document else None


async def read_link_by_alias(
    alias: str,
) -> Optional[LinkDbModel]:
    collection = get_links_collection()
    document = await collection.find_one(dict(alias={"$eq": alias}))
    return LinkDbModel(**document) if document else None


async def read_user_links(
    owner: UUID4,
    links_filter: Optional[LinksFilterEnum],
    page: int,
    per_page: int,
    tag: Optional[str] = Query(..., regex=settings.tags.regex),  # type: ignore
) -> Tuple[List[LinkDbModel], int]:
    collection = get_links_collection()
    query: Dict[str, Any] = dict(owner=owner)

    if tag:
        tag_data = await read_tag(name=tag, owner=owner)
        if not tag_data:
            raise ValueError(f'Unknown tag "{tag}"')
        query.update({"$or": []})
        for alias in tag_data.aliases:
            query["$or"].append(dict(alias=alias))

    if links_filter:
        expression = "$ne" if links_filter.ARCHIVED else "$eq"
        query.update(archived={expression: False})

    documents = await mongodb_paginated_find(
        collection=collection,
        query=query,
        page=page,
        per_page=per_page,
        sort=[("created_at", DESCENDING)],
    )

    total = await links_count(query)
    return [LinkDbModel(**doc) for doc in documents], total


async def create_link(
    owner: UUID4,
    url: AnyUrl,
    title: str,
    description: str,
    alias: Optional[str],
) -> LinkDbModel:
    collection = get_links_collection()
    num = await links_count() + 1
    if alias is None:
        alias = hashids.encode(num)
    link = LinkDbModel(
        url=url,
        alias=alias,
        owner=owner,
        title=title,
        description=description,
    )
    await collection.insert_one(link.dict())
    return link


async def update_link(
    alias: str,
    **updatable_fields: Any,
) -> Optional[LinkDbModel]:
    collection = get_links_collection()
    res: UpdateResult = await collection.update_one(
        {"alias": alias},
        {"$set": updatable_fields},
    )
    if not res.modified_count:
        return None
    return await read_link_by_alias(alias=alias)
