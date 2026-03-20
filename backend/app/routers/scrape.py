from fastapi import APIRouter, HTTPException, Query

from ..schemas import ScrapeResult
from ..scrapers.registry import scrape_url

router = APIRouter(prefix="/scrape", tags=["scrape"])


@router.get("/", response_model=ScrapeResult)
async def scrape(url: str = Query(..., description="Product URL to scrape")):
    try:
        return await scrape_url(url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception:
        raise HTTPException(status_code=502, detail="Unexpected error while scraping")
