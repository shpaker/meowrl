from fastapi import status
from httpx import Response
from pytest import mark


@mark.asyncio
async def test_root(client):
    response: Response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text


@mark.asyncio
async def test_healthz(client):
    response: Response = await client.get("/healthz")
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json()["healthy"] is True, response.text
