from typing import Any, Dict, List, Optional, Tuple

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from app.services.mongodb.wrapper import MongoDBWrapper
from app.settings import get_settings

settings = get_settings()


def get_mongodb_client() -> AsyncIOMotorClient:
    return MongoDBWrapper().client


def get_database() -> AsyncIOMotorCollection:
    client = get_mongodb_client()
    return client[settings.mongodb.database]


def get_clicks_collection() -> AsyncIOMotorCollection:
    db = get_database()
    return db[settings.mongodb.clicks_collection]


def get_links_collection() -> AsyncIOMotorCollection:
    db = get_database()
    return db[settings.mongodb.links_collection]


def get_tags_collection() -> AsyncIOMotorCollection:
    db = get_database()
    return db[settings.mongodb.tags_collection]


async def mongodb_paginated_find(
    collection: AsyncIOMotorClient,
    query: Optional[Dict[str, Any]],
    page: int,
    per_page: int,
    sort: Optional[List[Tuple[str, int]]] = None,
    projection: Optional[Dict[str, int]] = None,
) -> List[Dict[str, Any]]:

    cursor = collection.find(query, sort=sort, projection=projection)
    cursor.skip(page * per_page).limit(per_page)
    return [doc async for doc in cursor]
