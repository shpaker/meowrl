from fastapi import status
from httpx import Response
from pytest import mark


@mark.asyncio
async def test_create_link(
    client,
    auth_client,
):
    response: Response = await auth_client.post("/links", json=dict(url="https://ya.ru"))
    link_data = response.json()
    assert response.status_code == status.HTTP_200_OK, response.text
    response: Response = await client.get(f"/r/{link_data['alias']}", allow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT, response.text
    assert response.next_request.url == "https://ya.ru", response.text


@mark.asyncio
async def test_create_duplicate_link(
    auth_client,
):
    response: Response = await auth_client.post("/links", json=dict(url="https://goo.gl", title="test1"))
    assert response.status_code == status.HTTP_200_OK, response.text
    response: Response = await auth_client.post("/links", json=dict(url="https://goo.gl", title="test1"))
    assert response.status_code == status.HTTP_409_CONFLICT, response.text


@mark.asyncio
async def test_read_links(
    auth_client,
):
    await auth_client.post("/links", json=dict(url="https://facebook1.com"))
    await auth_client.post("/links", json=dict(url="https://facebook2.com"))
    await auth_client.post("/links", json=dict(url="https://facebook3.com"))
    await auth_client.post("/links", json=dict(url="https://facebook4.com"))
    response: Response = await auth_client.get("/links", params=dict(page=1, per_page=8))
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json()["total"] == 4, response.text
    await auth_client.post("/links", json=dict(url="https://facebook5.com"))
    response: Response = await auth_client.get("/links", params=dict(page=1, per_page=8))
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json()["total"] == 5, response.text
    assert len(response.json()["links"]) == 5, response.text


@mark.asyncio
async def test_update_link(
    auth_client,
):
    response: Response = await auth_client.post("/links", json=dict(url="https://testt.com"))
    link_data = response.json()
    data_for_update = dict(
        title="test",
        description="test test",
        archived=True,
    )
    response: Response = await auth_client.patch(
        "/links", json=dict(alias=link_data["alias"], settings=data_for_update)
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    link_data = response.json()
    for key in data_for_update:
        assert link_data[key] == data_for_update[key], response.text


@mark.asyncio
async def test_archived_link(
    client,
    auth_client,
):
    url = "https://t.ttt"
    response: Response = await auth_client.post("/links", json=dict(url=url))
    alias = response.json()["alias"]
    await auth_client.patch("/links", json=dict(alias=alias, settings=dict(archived=True)))
    response: Response = await client.get(f"/r/{alias}", allow_redirects=False)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response.text
    await auth_client.patch("/links", json=dict(alias=alias, settings=dict(archived=False)))
    response: Response = await client.get(f"/r/{alias}", allow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT, response.text


@mark.asyncio
async def test_read_clicks(
    auth_client,
    client,
):
    response: Response = await auth_client.post("/links", json=dict(url="https://facebook1.com"))
    alias = response.json()["alias"]
    await client.get(f"/r/{alias}", allow_redirects=False)
    await client.get(f"/r/{alias}", allow_redirects=False)
    await client.get(f"/r/{alias}", allow_redirects=False)
    # await sleep(1)
    response: Response = await auth_client.get(f"/r/{alias}/clicks")
    data = response.json()
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json()["total"] == 3, response.text


@mark.asyncio
async def test_link_preview(
    client,
    auth_client,
):
    response: Response = await auth_client.post("/links", json=dict(url="https://ywwwwa.ru"))
    alias = response.json()["alias"]
    response: Response = await client.get(f"/r/{alias}/preview")
    data = response.json()
    assert response.status_code == status.HTTP_200_OK, response.text
