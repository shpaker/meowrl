from fastapi import status
from httpx import Response
from pytest import mark


@mark.asyncio
async def test_auth(client):
    response: Response = await client.get(f"/clicks", params=dict(alias="alias"))
    assert response.status_code == status.HTTP_403_FORBIDDEN, response.text


@mark.asyncio
async def test_range(auth_client, client):
    response: Response = await auth_client.post("/links", json=dict(url="https://facebook1.com"))
    alias = response.json()["alias"]
    await client.get(f"/r/{alias}", allow_redirects=False)
    await client.get(f"/r/{alias}", allow_redirects=False)
    await client.get(f"/r/{alias}", allow_redirects=False)
    # await sleep(1)
    response: Response = await auth_client.get(f"/clicks", params=dict(alias=alias))
    data = response.json()
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json()["total"] == 3, response.text
