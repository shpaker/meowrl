from datetime import datetime, timezone
from typing import List, Optional, Union

from pydantic import UUID4
from pymongo.results import UpdateResult

from app.models.tags import TagDbModel
from app.services.mongodb.depends import get_tags_collection
from app.settings import get_settings

settings = get_settings()


async def read_tag(name: str, owner: UUID4) -> Optional[TagDbModel]:
    collection = get_tags_collection()
    result = await collection.find_one(dict(name={"$eq": name}, owner={"$eq": owner}))
    return TagDbModel(**result) if result else None


async def create_tag(name: str, owner: UUID4, aliases: Union[str, list[str]]) -> TagDbModel:
    if isinstance(aliases, str):
        aliases = [aliases]
    collection = get_tags_collection()
    tag = TagDbModel(name=name, owner=owner, aliases=aliases)  # noqa
    doc = tag.dict()
    await collection.insert_one(doc)
    return tag


async def append_aliases_to_tag(name: str, owner: UUID4, aliases: Union[str, list[str]]) -> Optional[TagDbModel]:
    collection = get_tags_collection()
    if isinstance(aliases, str):
        aliases = [aliases]
    result: UpdateResult = await collection.update_one(
        dict(name=name, owner=owner),
        {"$addToSet": dict(aliases={"$each": aliases}), "$set": {"updated_at": datetime.now(tz=timezone.utc)}},
    )
    if result.matched_count == 0:
        return None
    tag: TagDbModel = await read_tag(name, owner)  # type: ignore
    return tag


async def pull_aliases_from_tag(name: str, owner: UUID4, aliases: Union[str, list[str]]) -> Optional[TagDbModel]:
    collection = get_tags_collection()
    if isinstance(aliases, str):
        aliases = [aliases]
    result: UpdateResult = await collection.update_one(
        dict(name=name, owner=owner),
        {"$pull": dict(aliases={"$in": aliases}), "$set": {"updated_at": datetime.now(tz=timezone.utc)}},
    )
    if result.modified_count == 0:
        return None
    tag: TagDbModel = await read_tag(name, owner)  # type: ignore
    if len(tag.aliases) == 0:
        await collection.delete_one(dict(name=name, owner=owner))
    return tag


async def ensure_tag(name: str, owner: UUID4, aliases: Union[str, Optional[list[str]]] = None) -> TagDbModel:
    if not aliases:
        aliases = list()
    if isinstance(aliases, str):
        aliases = [aliases]
    tag = await read_tag(name, owner=owner)
    if not tag:
        return await create_tag(name, owner, aliases)
    if aliases:
        await append_aliases_to_tag(name, owner, aliases)
        tag.aliases.append(*aliases)
    return tag


async def read_tags_for_link(alias: str) -> list[str]:
    collection = get_tags_collection()
    result = collection.find(dict(aliases={"$eq": alias}))
    tags: List[str] = [tag["name"] async for tag in result]
    return tags


# async def read_aliases_for_tag(name: str, owner: UUID4) -> list[str]:
#     collection = get_tags_collection()
#     result = collection.find(dict(name={"$eq": name}, aliases={"$eq": alias}))
#     tags: List[str] = [tag["name"] async for tag in result]
#     return tags
