# pylint: disable=redefined-outer-name
from logging import basicConfig, getLogger
from pathlib import Path
from sys import path
from uuid import uuid4

from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from jose import jwt
from pytest import fixture

from app.main import create_app
from app.services.mongodb.depends import get_clicks_collection, get_links_collection
from app.settings import get_settings

path.insert(0, str(Path(__file__).parent.parent.resolve()))
logger = getLogger("tests")
basicConfig(level="DEBUG")


@fixture(scope="function", autouse=True)
def logs_config(caplog):
    caplog.set_level("DEBUG", logger="tests")


@fixture
async def client():
    app = create_app()
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://service") as test_client:
            yield test_client


@fixture
async def auth_client(generated_auth_header: dict):
    app = create_app()
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://service", headers=generated_auth_header) as test_client:
            yield test_client


@fixture
async def settings():
    return get_settings()


@fixture
def generated_uuid4():
    return str(uuid4())


@fixture
def sso_user_id(generated_uuid4: str):
    return generated_uuid4


@fixture
def generated_token_payload(sso_user_id: str):
    return dict(
        sub=sso_user_id,
        azp=0,
        exp=0,
        iat=1,
        preferred_username="test",
    )


@fixture
def generated_token(generated_token_payload: dict):
    return jwt.encode(
        claims=generated_token_payload,
        key="INVALID-DECODING-KEY",
    )


@fixture
def generated_auth_header(generated_token: str):
    return dict(
        Authorization=f"Bearer {generated_token}",
    )


@fixture(scope="function", autouse=True)
async def remove_collection(generated_token: str):
    yield
    coll = get_links_collection()
    await coll.delete_many({})
    coll = get_clicks_collection()
    await coll.delete_many({})
