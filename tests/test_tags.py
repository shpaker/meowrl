from httpx import Response
from pytest import mark


@mark.asyncio
async def test_tags(auth_client):
    response: Response = await auth_client.post("/links", json=dict(url="https://ya.ru", tags=["foo", "bar", "baz"]))
    data = response.json()
    assert len(data["tags"]) == 3, response.text
