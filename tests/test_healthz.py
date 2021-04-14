from fastapi import status
from httpx import Response
from pytest import mark


@mark.asyncio
async def test_root(client):
    response: Response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text


@mark.asyncio
async def test_ping(client):
    response: Response = await client.get("/ping")
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.text == "pong"


@mark.asyncio
async def test_healthz(client):
    response: Response = await client.get("/health")
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json()["healthy"] is True, response.text
