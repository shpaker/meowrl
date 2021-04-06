from fastapi import status
from httpx import Response
from pytest import mark


@mark.asyncio
async def test_redoc(client):
    response: Response = await client.get("/api")
    assert response.status_code == status.HTTP_200_OK, response.text


@mark.asyncio
async def test_openapi(client):
    response: Response = await client.get("/api.json")
    assert response.status_code == status.HTTP_200_OK, response.text
