from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Coffee, Descriptor, GrinderSetting, Review, Grinder, BrewSetup
from ..schemas import CoffeeCreate, CoffeeListOut, CoffeeOut, CoffeeUpdate
from ..scrapers.registry import scrape_url

router = APIRouter(prefix="/coffees", tags=["coffees"])


def _get_default_grind(db: Session, coffee_id: int) -> float | None:
    """Get grind setting for default grinder + default brew setup."""
    default_grinder = db.query(Grinder).filter(Grinder.is_default.is_(True)).first()
    default_setup = db.query(BrewSetup).filter(BrewSetup.is_default.is_(True)).first()
    if not default_grinder or not default_setup:
        return None
    setting = db.query(GrinderSetting).filter(
        GrinderSetting.coffee_id == coffee_id,
        GrinderSetting.grinder_id == default_grinder.id,
        GrinderSetting.brew_setup_id == default_setup.id,
    ).first()
    return setting.setting if setting else None


def _get_avg_rating(db: Session, coffee_id: int) -> float | None:
    result = db.query(func.avg(Review.rating)).filter(
        Review.coffee_id == coffee_id
    ).scalar()
    return round(result, 1) if result else None


def _get_person_rating(db: Session, coffee_id: int, taster_id: int) -> int | None:
    review = db.query(Review).filter(
        Review.coffee_id == coffee_id,
        Review.taster_id == taster_id,
    ).first()
    return review.rating if review else None


@router.get("/", response_model=list[CoffeeListOut])
def list_coffees(
    search: str | None = Query(None, description="Search by name or roastery"),
    descriptor_id: int | None = Query(None, description="Filter by roastery descriptor"),
    taster_id: int | None = Query(None, description="Active person — returns their rating"),
    grinder_id: int | None = Query(None, description="Active grinder — returns grind setting"),
    brew_setup_id: int | None = Query(None, description="Active brew setup — filters ratings and grind"),
    db: Session = Depends(get_db),
):
    query = db.query(Coffee).options(
        joinedload(Coffee.origin_ref),
        joinedload(Coffee.roastery_ref),
        joinedload(Coffee.roastery_descriptors),
    )

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            Coffee.name.ilike(pattern)
        )
    if descriptor_id:
        query = query.filter(Coffee.roastery_descriptors.any(Descriptor.id == descriptor_id))

    coffees = query.order_by(
        Coffee.in_stock.desc(), Coffee.in_store.desc(), Coffee.created_at.desc()
    ).all()

    if not coffees:
        return []

    coffee_ids = [c.id for c in coffees]

    # Bulk: avg ratings (1 query)
    avg_ratings = dict(
        db.query(Review.coffee_id, func.avg(Review.rating))
        .filter(Review.coffee_id.in_(coffee_ids))
        .group_by(Review.coffee_id)
        .all()
    )

    # Resolve active equipment (explicit IDs or fallback to is_default)
    active_grinder = (
        db.query(Grinder).filter(Grinder.id == grinder_id).first() if grinder_id
        else db.query(Grinder).filter(Grinder.is_default.is_(True)).first()
    )
    active_setup = (
        db.query(BrewSetup).filter(BrewSetup.id == brew_setup_id).first() if brew_setup_id
        else db.query(BrewSetup).filter(BrewSetup.is_default.is_(True)).first()
    )

    # Bulk: person ratings for active brew setup (1 query)
    person_ratings = {}
    if taster_id and active_setup:
        person_ratings = dict(
            db.query(Review.coffee_id, Review.rating)
            .filter(
                Review.coffee_id.in_(coffee_ids),
                Review.taster_id == taster_id,
                Review.brew_setup_id == active_setup.id,
            )
            .all()
        )

    # Bulk: grind settings for active grinder + brew setup
    default_grinds: dict[int, float] = {}
    if active_grinder and active_setup:
        for row in db.query(GrinderSetting.coffee_id, GrinderSetting.setting).filter(
            GrinderSetting.coffee_id.in_(coffee_ids),
            GrinderSetting.grinder_id == active_grinder.id,
            GrinderSetting.brew_setup_id == active_setup.id,
        ).all():
            default_grinds[row.coffee_id] = row.setting

    result = []
    for c in coffees:
        data = CoffeeListOut.model_validate(c)
        avg = avg_ratings.get(c.id)
        data.avg_rating = round(avg, 1) if avg else None
        data.person_rating = person_ratings.get(c.id)
        data.default_grind = default_grinds.get(c.id)
        if active_grinder:
            data.default_grind_step = active_grinder.step or 1
        result.append(data)
    return result


@router.get("/{coffee_id}", response_model=CoffeeOut)
def get_coffee(coffee_id: int, db: Session = Depends(get_db)):
    coffee = (
        db.query(Coffee)
        .options(
            joinedload(Coffee.origin_ref),
            joinedload(Coffee.roastery_ref),
            joinedload(Coffee.roastery_descriptors),
            joinedload(Coffee.reviews).joinedload(Review.descriptors),
            joinedload(Coffee.reviews).joinedload(Review.taster),
            joinedload(Coffee.reviews).joinedload(Review.brew_setup),
            joinedload(Coffee.grinder_settings).joinedload(GrinderSetting.grinder),
            joinedload(Coffee.grinder_settings).joinedload(GrinderSetting.brew_setup),
        )
        .filter(Coffee.id == coffee_id)
        .first()
    )
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")
    return coffee


@router.post("/", response_model=CoffeeOut, status_code=201)
def create_coffee(data: CoffeeCreate, db: Session = Depends(get_db)):
    coffee = Coffee(
        name=data.name,
        roastery_id=data.roastery_id,
        origin_id=data.origin_id,
        process=data.process,
        roast_level=data.roast_level,
        roastery_url=data.roastery_url,
        image_url=data.image_url,
        score=data.score,
        sweetness=data.sweetness,
        acidity=data.acidity,
        bitterness=data.bitterness,
        notes=data.notes,
        roaster_comment=data.roaster_comment,
        price=data.price,
        price_wholesale=data.price_wholesale,
        in_stock=data.in_stock,
        in_store=data.in_store,
        fetched_at=datetime.now(timezone.utc) if data.roastery_url else None,
    )

    if data.roastery_descriptor_ids:
        descriptors = db.query(Descriptor).filter(
            Descriptor.id.in_(data.roastery_descriptor_ids)
        ).all()
        coffee.roastery_descriptors = descriptors

    db.add(coffee)
    db.commit()
    db.refresh(coffee)
    return coffee


@router.put("/{coffee_id}", response_model=CoffeeOut)
def update_coffee(coffee_id: int, data: CoffeeUpdate, db: Session = Depends(get_db)):
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    update_data = data.model_dump(exclude_unset=True)
    descriptor_ids = update_data.pop("roastery_descriptor_ids", None)

    for key, value in update_data.items():
        setattr(coffee, key, value)
    coffee.updated_at = datetime.now(timezone.utc)

    if descriptor_ids is not None:
        descriptors = db.query(Descriptor).filter(
            Descriptor.id.in_(descriptor_ids)
        ).all()
        coffee.roastery_descriptors = descriptors

    db.commit()
    db.refresh(coffee)
    return coffee


@router.post("/{coffee_id}/refresh", response_model=CoffeeOut)
async def refresh_coffee(coffee_id: int, db: Session = Depends(get_db)):
    """Re-scrape a coffee from its roastery URL and update all scraped fields."""
    coffee = (
        db.query(Coffee)
        .options(
            joinedload(Coffee.origin_ref),
            joinedload(Coffee.roastery_ref),
            joinedload(Coffee.roastery_descriptors),
            joinedload(Coffee.reviews).joinedload(Review.descriptors),
            joinedload(Coffee.reviews).joinedload(Review.taster),
            joinedload(Coffee.reviews).joinedload(Review.brew_setup),
            joinedload(Coffee.grinder_settings).joinedload(GrinderSetting.grinder),
            joinedload(Coffee.grinder_settings).joinedload(GrinderSetting.brew_setup),
        )
        .filter(Coffee.id == coffee_id)
        .first()
    )
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")
    if not coffee.roastery_url:
        raise HTTPException(status_code=400, detail="Coffee has no roastery URL to refresh from")

    try:
        result = await scrape_url(coffee.roastery_url)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to scrape: {e}")

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

    # Update roastery descriptors from scrape
    if result.flavor_descriptors:
        en_descriptors = result.flavor_descriptors.get("en", [])
        if en_descriptors:
            matched = db.query(Descriptor).filter(
                func.lower(Descriptor.name).in_([d.lower() for d in en_descriptors])
            ).all()
            coffee.roastery_descriptors = matched

    db.commit()
    db.refresh(coffee)
    return coffee


@router.delete("/{coffee_id}", status_code=204)
def delete_coffee(coffee_id: int, db: Session = Depends(get_db)):
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")
    db.delete(coffee)
    db.commit()
