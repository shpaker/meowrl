from datetime import datetime, timezone
from typing import List, Optional, Union

from pydantic import UUID4

from app.models.tags import TagDbModel
from app.services.mongodb.depends import get_tags_collection


async def read_tag(name: str, owner: UUID4) -> Optional[TagDbModel]:
    collection = get_tags_collection()
    result = await collection.find_one(dict(owner={"$eq": owner}, name={"$eq": name}))
    return TagDbModel(**result) if result else None


async def create_tag(name: str, owner: UUID4, aliases: Union[str, list[str]]) -> TagDbModel:
    if isinstance(aliases, str):
        aliases = [aliases]
    collection = get_tags_collection()
    tag = TagDbModel(name=name, owner=owner, aliases=aliases)  # noqa
    doc = tag.dict()
    await collection.insert_one(doc)
    return tag


async def append_aliases_to_tag(name: str, owner: UUID4, aliases: list[str]) -> None:
    collection = get_tags_collection()
    await collection.update(
        dict(name=name, owner=owner),
        {"$addToSet": dict(aliases=aliases), "updated_at": datetime.now(tz=timezone.utc)},
    )


async def pull_aliases_from_tag(name: str, owner: UUID4, aliases: list[str]) -> None:
    collection = get_tags_collection()
    await collection.update(
        dict(name=name, owner=owner),
        {"$pull": dict(aliases=aliases), "updated_at": datetime.now(tz=timezone.utc)},
    )


async def ensure_tag(name: str, owner: UUID4, aliases: Union[str, Optional[list[str]]] = None) -> TagDbModel:
    tag = await read_tag(name, owner=owner)
    if not aliases:
        aliases = list()
    if isinstance(aliases, str):
        aliases = [aliases]
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
