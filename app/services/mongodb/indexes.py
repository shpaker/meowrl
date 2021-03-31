from logging import getLogger

from pymongo import ASCENDING, DESCENDING

from app.services.mongodb.depends import get_clicks_collection, get_links_collection

logger = getLogger(__name__)


async def create_clicks_collection_indexes() -> None:
    collection = get_clicks_collection()
    logger.info("Create indexes in clicks collection")
    await collection.create_index([("created_at", ASCENDING)])


async def create_links_collection_indexes() -> None:
    collection = get_links_collection()
    logger.info("Create indexes in links collection")
    await collection.create_index([("owner", 1), ("url", 1), ("title", 1)], unique=True)
    await collection.create_index([("alias", 1)], unique=True)
    await collection.create_index([("created_at", DESCENDING)])


async def create_mongodb_indexes() -> None:
    await create_clicks_collection_indexes()
    await create_links_collection_indexes()
