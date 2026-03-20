"""Tests for MadHeadsScraper._fetch_with_retry retry/backoff logic."""

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.scrapers.madheads import MadHeadsScraper

URL = "https://madheadscoffee.com/en/p/test"


@pytest.mark.anyio
async def test_retry_succeeds_after_transient_timeout():
    """Retries on timeout and succeeds on second attempt."""
    mock_response = httpx.Response(200, text="ok", request=httpx.Request("GET", URL))
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=[httpx.TimeoutException("timeout"), mock_response])
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("app.scrapers.madheads.httpx.AsyncClient", return_value=mock_client), \
         patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        resp = await MadHeadsScraper._fetch_with_retry(URL, retries=2)

    assert resp.status_code == 200
    mock_sleep.assert_called_once_with(1)


@pytest.mark.anyio
async def test_retry_exhausted_on_timeout():
    """Raises ConnectionError with friendly message after all retries exhausted."""
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("app.scrapers.madheads.httpx.AsyncClient", return_value=mock_client), \
         patch("asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(ConnectionError, match="Roastery site timed out"):
            await MadHeadsScraper._fetch_with_retry(URL, retries=2)


@pytest.mark.anyio
async def test_retry_exhausted_on_connect_error():
    """Raises ConnectionError on connect failure after retries."""
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=httpx.ConnectError("refused"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("app.scrapers.madheads.httpx.AsyncClient", return_value=mock_client), \
         patch("asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(ConnectionError, match="Could not connect"):
            await MadHeadsScraper._fetch_with_retry(URL, retries=2)


@pytest.mark.anyio
async def test_no_retry_on_404():
    """404 is permanent — raises immediately, no retry."""
    mock_response = httpx.Response(404)
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("app.scrapers.madheads.httpx.AsyncClient", return_value=mock_client), \
         patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        with pytest.raises(ValueError, match="Product page not found"):
            await MadHeadsScraper._fetch_with_retry(URL, retries=3)

    mock_sleep.assert_not_called()


@pytest.mark.anyio
async def test_retry_on_500_then_success():
    """Retries on 500, succeeds on next attempt."""
    error_response = httpx.Response(500, request=httpx.Request("GET", URL))
    ok_response = httpx.Response(200, text="ok", request=httpx.Request("GET", URL))
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=[error_response, ok_response])
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("app.scrapers.madheads.httpx.AsyncClient", return_value=mock_client), \
         patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        resp = await MadHeadsScraper._fetch_with_retry(URL, retries=2)

    assert resp.status_code == 200
    mock_sleep.assert_called_once_with(1)


@pytest.mark.anyio
async def test_no_retry_on_403():
    """Non-5xx HTTP errors are permanent — no retry."""
    error_response = httpx.Response(403, request=httpx.Request("GET", URL))
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=error_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("app.scrapers.madheads.httpx.AsyncClient", return_value=mock_client), \
         patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        with pytest.raises(ValueError, match="Roastery returned error 403"):
            await MadHeadsScraper._fetch_with_retry(URL, retries=3)

    mock_sleep.assert_not_called()


@pytest.mark.anyio
async def test_backoff_delays():
    """Verifies exponential backoff delays (1s, 3s)."""
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("app.scrapers.madheads.httpx.AsyncClient", return_value=mock_client), \
         patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        with pytest.raises(ConnectionError):
            await MadHeadsScraper._fetch_with_retry(URL, retries=3)

    assert mock_sleep.call_args_list == [
        ((1,),), ((3,),),
    ]
