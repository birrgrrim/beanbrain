from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Coffee, Descriptor, GrinderSetting, Tasting
from ..schemas import CoffeeCreate, CoffeeListOut, CoffeeOut, CoffeeUpdate

router = APIRouter(prefix="/coffees", tags=["coffees"])


@router.get("/", response_model=list[CoffeeListOut])
def list_coffees(
    search: str | None = Query(None, description="Search by name or roastery"),
    roastery: str | None = Query(None),
    descriptor_id: int | None = Query(None, description="Filter by roastery descriptor"),
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

    return query.order_by(Coffee.created_at.desc()).all()


@router.get("/{coffee_id}", response_model=CoffeeOut)
def get_coffee(coffee_id: int, db: Session = Depends(get_db)):
    coffee = (
        db.query(Coffee)
        .options(
            joinedload(Coffee.roastery_descriptors),
            joinedload(Coffee.tastings).joinedload(Tasting.descriptors),
            joinedload(Coffee.grinder_settings).joinedload(GrinderSetting.equipment),
            joinedload(Coffee.grinder_settings).joinedload(GrinderSetting.brew_method),
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
        notes=data.notes,
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
