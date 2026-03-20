from unittest.mock import AsyncMock, patch

from app.schemas import ScrapeResult


MOCK_RESULT = ScrapeResult(
    name="Ethiopia Sidamo",
    roastery="MadHeads",
    origin="Ethiopia",
    process="Natural",
    roast_level="Light",
    roastery_url="https://madheadscoffee.com/p/test",
    image_url="https://api.madheadscoffee.com/cdn/img/large.png",
    score=85.5,
    sweetness=4,
    acidity=3,
    bitterness=2,
    price=350,
    price_wholesale=280,
    flavor_descriptors={"en": ["Chocolate", "Berry"], "uk": ["Шоколад", "Ягоди"]},
    name_i18n={"en": "Ethiopia Sidamo", "uk": "Ефіопія Сідамо"},
    roaster_comment={"en": "Great coffee", "uk": "Чудова кава"},
)


def test_scrape_success(client):
    with patch("app.routers.scrape.scrape_url", new_callable=AsyncMock, return_value=MOCK_RESULT):
        resp = client.get("/scrape/", params={"url": "https://madheadscoffee.com/p/test"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Ethiopia Sidamo"
    assert data["roastery"] == "MadHeads"
    assert data["score"] == 85.5
    assert data["price"] == 350
    assert data["flavor_descriptors"]["en"] == ["Chocolate", "Berry"]


def test_scrape_bad_url(client):
    with patch(
        "app.routers.scrape.scrape_url",
        new_callable=AsyncMock,
        side_effect=ValueError("No scraper available for URL: https://unknown.com/coffee"),
    ):
        resp = client.get("/scrape/", params={"url": "https://unknown.com/coffee"})
    assert resp.status_code == 400
    assert "No scraper available" in resp.json()["detail"]


def test_scrape_network_failure(client):
    with patch(
        "app.routers.scrape.scrape_url",
        new_callable=AsyncMock,
        side_effect=ConnectionError("Connection refused"),
    ):
        resp = client.get("/scrape/", params={"url": "https://madheadscoffee.com/p/test"})
    assert resp.status_code == 502
    assert "Failed to scrape" in resp.json()["detail"]


def test_scrape_missing_url_param(client):
    resp = client.get("/scrape/")
    assert resp.status_code == 422
