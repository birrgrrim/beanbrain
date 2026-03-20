import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Coffee, Descriptor, Roastery
from ..schemas import RoasteryCreate, RoasteryOut, RoasteryUpdate
from ..scrapers.registry import scrape_url
from ._helpers import get_or_404

router = APIRouter(prefix="/roasteries", tags=["roasteries"])


@router.get("/", response_model=list[RoasteryOut])
def list_roasteries(db: Session = Depends(get_db)):
    return db.query(Roastery).filter(Roastery.is_active.is_(True)).order_by(Roastery.name).all()


@router.post("/", response_model=RoasteryOut, status_code=201)
def create_roastery(data: RoasteryCreate, db: Session = Depends(get_db)):
    roastery = Roastery(**data.model_dump())
    db.add(roastery)
    db.commit()
    db.refresh(roastery)
    return roastery


@router.put("/{roastery_id}", response_model=RoasteryOut)
def update_roastery(roastery_id: int, data: RoasteryUpdate, db: Session = Depends(get_db)):
    roastery = get_or_404(db, Roastery, roastery_id, "Roastery not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(roastery, k, v)
    db.commit()
    db.refresh(roastery)
    return roastery


@router.post("/{roastery_id}/refresh")
async def refresh_roastery_coffees(roastery_id: int, db: Session = Depends(get_db)):
    """Re-scrape all coffees with a roastery_url for this roastery."""
    get_or_404(db, Roastery, roastery_id, "Roastery not found")
    coffees = db.query(Coffee).filter(
        Coffee.roastery_id == roastery_id,
        Coffee.roastery_url.isnot(None),
    ).all()

    results = {"refreshed": 0, "failed": 0, "total": len(coffees), "errors": []}
    for i, coffee in enumerate(coffees):
        if i > 0:
            await asyncio.sleep(3)  # polite delay between requests
        try:
            result = await scrape_url(coffee.roastery_url)
            coffee.name = result.name or coffee.name
            coffee.process = result.process
            coffee.roast_level = result.roast_level
            coffee.image_url = result.image_url
            coffee.score = result.score
            coffee.sweetness = result.sweetness
            coffee.acidity = result.acidity
            coffee.bitterness = result.bitterness
            coffee.roaster_comment = result.roaster_comment or coffee.roaster_comment
            coffee.price = result.price
            coffee.price_wholesale = result.price_wholesale
            coffee.fetched_at = datetime.now(timezone.utc)

            if result.flavor_descriptors:
                en_descriptors = result.flavor_descriptors.get("en", [])
                if en_descriptors:
                    matched = db.query(Descriptor).filter(
                        func.lower(Descriptor.name).in_([d.lower() for d in en_descriptors])
                    ).all()
                    coffee.roastery_descriptors = matched

            results["refreshed"] += 1
        except Exception as e:
            results["failed"] += 1
            results["errors"].append(f"{coffee.name}: {e}")

    db.commit()
    return results


@router.delete("/{roastery_id}", status_code=204)
def delete_roastery(roastery_id: int, db: Session = Depends(get_db)):
    roastery = get_or_404(db, Roastery, roastery_id, "Roastery not found")
    roastery.is_active = False
    db.commit()
