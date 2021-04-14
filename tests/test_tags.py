from httpx import Response
from pytest import mark
from starlette import status


@mark.asyncio
async def test_tags(auth_client):
    tags_1 = ["foo", "bar"]
    tags_2 = ["bar"]
    await auth_client.post("/links", json=dict(url="https://ya1.ru", tags=tags_1))
    await auth_client.post("/links", json=dict(url="https://ya2.ru", tags=tags_1))
    response: Response = await auth_client.post("/links", json=dict(url="https://ya3.ru", tags=tags_2))
    data = response.json()
    assert len(data["tags"]) == 1, response.text
    await auth_client.post("/links", json=dict(url="https://ya4.ru"))
    response: Response = await auth_client.get("/links")
    assert len(response.json()["links"]) == 4
    response: Response = await auth_client.get("/links", params=dict(tag="foo"))
    assert len(response.json()["links"]) == 2
    response: Response = await auth_client.get("/links", params=dict(tag="bar"))
    assert len(response.json()["links"]) == 3


@mark.asyncio
async def test_append_tag(auth_client):
    tags_1 = ["foo", "bar"]
    response: Response = await auth_client.post("/links", json=dict(url="https://ya1.ru", tags=tags_1))
    data = response.json()
    assert len(data["tags"]) == 2, response.text
    response: Response = await auth_client.post("/tags", json=dict(tag="bat", alias=data["alias"]))
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["name"] == "bat", response.text


@mark.asyncio
async def test_delete_tag(auth_client):
    tags_1 = ["foo", "bar"]
    response: Response = await auth_client.post("/links", json=dict(url="https://ya.ru", tags=tags_1))
    alias = response.json()["alias"]
    response: Response = await auth_client.get("/links")
    assert len(response.json()["links"][0]["tags"]) == 2
    response: Response = await auth_client.delete("/tags", params=dict(tag="bareeee", alias=alias))
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    response: Response = await auth_client.delete("/tags", params=dict(tag="bar", alias=alias))
    assert response.status_code == status.HTTP_200_OK, response.text
    response: Response = await auth_client.get("/links")
    assert len(response.json()["links"][0]["tags"]) == 1
