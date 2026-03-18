from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Coffee, Descriptor, GrinderSetting, Review, Grinder, BrewSetup
from ..schemas import CoffeeCreate, CoffeeListOut, CoffeeOut, CoffeeUpdate

router = APIRouter(prefix="/coffees", tags=["coffees"])


def _get_default_grind(db: Session, coffee_id: int) -> float | None:
    """Get grind setting for default grinder + default brew setup."""
    default_grinder = db.query(Grinder).filter(Grinder.is_default == True).first()
    default_setup = db.query(BrewSetup).filter(BrewSetup.is_default == True).first()
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
    roastery: str | None = Query(None),
    descriptor_id: int | None = Query(None, description="Filter by roastery descriptor"),
    taster_id: int | None = Query(None, description="Active person — returns their rating"),
    db: Session = Depends(get_db),
):
    query = db.query(Coffee).options(joinedload(Coffee.roastery_descriptors))

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            Coffee.name.ilike(pattern) | Coffee.roastery.ilike(pattern)
        )
    if roastery:
        query = query.filter(Coffee.roastery.ilike(f"%{roastery}%"))
    if descriptor_id:
        query = query.filter(Coffee.roastery_descriptors.any(Descriptor.id == descriptor_id))

    coffees = query.order_by(
        Coffee.is_available.desc(), Coffee.created_at.desc()
    ).all()

    result = []
    for c in coffees:
        data = CoffeeListOut.model_validate(c)
        data.avg_rating = _get_avg_rating(db, c.id)
        if taster_id:
            data.person_rating = _get_person_rating(db, c.id, taster_id)
        data.default_grind = _get_default_grind(db, c.id)
        result.append(data)
    return result


@router.get("/{coffee_id}", response_model=CoffeeOut)
def get_coffee(coffee_id: int, db: Session = Depends(get_db)):
    coffee = (
        db.query(Coffee)
        .options(
            joinedload(Coffee.roastery_descriptors),
            joinedload(Coffee.reviews).joinedload(Review.descriptors),
            joinedload(Coffee.reviews).joinedload(Review.taster),
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
        roastery=data.roastery,
        origin=data.origin,
        process=data.process,
        roast_level=data.roast_level,
        roastery_url=data.roastery_url,
        image_url=data.image_url,
        score=data.score,
        sweetness=data.sweetness,
        acidity=data.acidity,
        bitterness=data.bitterness,
        notes=data.notes,
        is_available=data.is_available,
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

    if descriptor_ids is not None:
        descriptors = db.query(Descriptor).filter(
            Descriptor.id.in_(descriptor_ids)
        ).all()
        coffee.roastery_descriptors = descriptors

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
