from unittest.mock import AsyncMock, patch

from app.schemas import ScrapeResult


def _create_roastery(client, name="Test Roastery"):
    return client.post("/roasteries/", json={"name": name}).json()["id"]


def _create_coffee(client, roastery_id, name="Test Coffee", **kwargs):
    payload = {"name": name, "roastery_id": roastery_id, **kwargs}
    return client.post("/coffees/", json=payload).json()


MOCK_RESULT = ScrapeResult(
    name="Updated Name",
    roastery="MadHeads",
    origin="Ethiopia",
    process="Washed",
    roast_level="Medium",
    roastery_url="https://madheadscoffee.com/p/test",
    image_url="https://cdn.example.com/new.png",
    score=87.0,
    sweetness=4,
    acidity=3,
    bitterness=2,
    price=400,
    price_wholesale=320,
    flavor_descriptors={"en": ["Chocolate", "Berry"]},
    name_i18n={"en": "Updated Name"},
    roaster_comment={"en": "Tasting notes"},
)


# --- Coffee refresh ---


def test_refresh_coffee_success(client):
    rid = _create_roastery(client)
    coffee = _create_coffee(client, rid, roastery_url="https://madheadscoffee.com/p/test")

    with patch("app.routers.coffees.scrape_url", new_callable=AsyncMock, return_value=MOCK_RESULT):
        resp = client.post(f"/coffees/{coffee['id']}/refresh")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Updated Name"
    assert data["process"] == "Washed"
    assert data["roast_level"] == "Medium"
    assert data["score"] == 87.0
    assert data["price"] == 400


def test_refresh_coffee_preserves_name_when_scrape_returns_empty(client):
    rid = _create_roastery(client)
    coffee = _create_coffee(client, rid, name="Original", roastery_url="https://madheadscoffee.com/p/test")

    empty_name_result = MOCK_RESULT.model_copy(update={"name": ""})
    with patch("app.routers.coffees.scrape_url", new_callable=AsyncMock, return_value=empty_name_result):
        resp = client.post(f"/coffees/{coffee['id']}/refresh")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Original"


def test_refresh_coffee_matches_descriptors(client):
    rid = _create_roastery(client)
    coffee = _create_coffee(client, rid, roastery_url="https://madheadscoffee.com/p/test")

    with patch("app.routers.coffees.scrape_url", new_callable=AsyncMock, return_value=MOCK_RESULT):
        resp = client.post(f"/coffees/{coffee['id']}/refresh")
    assert resp.status_code == 200
    names = {d["name"] for d in resp.json()["roastery_descriptors"]}
    assert "Chocolate" in names
    assert "Berry" in names


def test_refresh_coffee_no_url(client):
    rid = _create_roastery(client)
    coffee = _create_coffee(client, rid)

    resp = client.post(f"/coffees/{coffee['id']}/refresh")
    assert resp.status_code == 400
    assert "no roastery URL" in resp.json()["detail"]


def test_refresh_coffee_not_found(client):
    resp = client.post("/coffees/9999/refresh")
    assert resp.status_code == 404


def test_refresh_coffee_scrape_failure(client):
    rid = _create_roastery(client)
    coffee = _create_coffee(client, rid, roastery_url="https://madheadscoffee.com/p/test")

    with patch(
        "app.routers.coffees.scrape_url",
        new_callable=AsyncMock,
        side_effect=ConnectionError("timeout"),
    ):
        resp = client.post(f"/coffees/{coffee['id']}/refresh")
    assert resp.status_code == 502


# --- Roastery refresh ---


def test_refresh_roastery_success(client):
    rid = _create_roastery(client)
    _create_coffee(client, rid, name="Coffee A", roastery_url="https://madheadscoffee.com/p/a")
    _create_coffee(client, rid, name="Coffee B", roastery_url="https://madheadscoffee.com/p/b")

    with patch("app.routers.roasteries.scrape_url", new_callable=AsyncMock, return_value=MOCK_RESULT):
        resp = client.post(f"/roasteries/{rid}/refresh")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert data["refreshed"] == 2
    assert data["failed"] == 0


def test_refresh_roastery_partial_failure(client):
    rid = _create_roastery(client)
    _create_coffee(client, rid, name="Good", roastery_url="https://madheadscoffee.com/p/good")
    _create_coffee(client, rid, name="Bad", roastery_url="https://madheadscoffee.com/p/bad")

    call_count = 0

    async def flaky_scrape(url):
        nonlocal call_count
        call_count += 1
        if call_count == 2:
            raise ConnectionError("timeout")
        return MOCK_RESULT

    with patch("app.routers.roasteries.scrape_url", side_effect=flaky_scrape):
        resp = client.post(f"/roasteries/{rid}/refresh")
    assert resp.status_code == 200
    data = resp.json()
    assert data["refreshed"] == 1
    assert data["failed"] == 1
    assert len(data["errors"]) == 1


def test_refresh_roastery_no_coffees_with_url(client):
    rid = _create_roastery(client)
    _create_coffee(client, rid, name="No URL coffee")

    with patch("app.routers.roasteries.scrape_url", new_callable=AsyncMock) as mock:
        resp = client.post(f"/roasteries/{rid}/refresh")
    assert resp.status_code == 200
    assert resp.json()["total"] == 0
    mock.assert_not_called()


def test_refresh_roastery_not_found(client):
    resp = client.post("/roasteries/9999/refresh")
    assert resp.status_code == 404
