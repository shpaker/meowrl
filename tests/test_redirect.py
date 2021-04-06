from fastapi import status
from httpx import Response
from pytest import mark


@mark.asyncio
async def test_redirect(client, auth_client):
    url = "http://foo.bar"
    response: Response = await auth_client.post("/links", json=dict(url=url))
    alias = response.json()["alias"]
    response: Response = await client.get(f"/r/{alias}", allow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT, response.text
    assert response.next_request.url == url, response.text
