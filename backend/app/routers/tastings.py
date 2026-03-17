from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Coffee, Descriptor, Tasting
from ..schemas import TastingCreate, TastingOut

router = APIRouter(prefix="/coffees/{coffee_id}/tastings", tags=["tastings"])


@router.get("/", response_model=list[TastingOut])
def list_tastings(coffee_id: int, db: Session = Depends(get_db)):
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    return (
        db.query(Tasting)
        .options(joinedload(Tasting.descriptors))
        .filter(Tasting.coffee_id == coffee_id)
        .order_by(Tasting.tasted_at.desc())
        .all()
    )


@router.post("/", response_model=TastingOut, status_code=201)
def create_tasting(coffee_id: int, data: TastingCreate, db: Session = Depends(get_db)):
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    tasting = Tasting(
        coffee_id=coffee_id,
        taster_name=data.taster_name,
        rating=data.rating,
        comment=data.comment,
    )

    if data.descriptor_ids:
        descriptors = db.query(Descriptor).filter(
            Descriptor.id.in_(data.descriptor_ids)
        ).all()
        tasting.descriptors = descriptors

    db.add(tasting)
    db.commit()
    db.refresh(tasting)

    return (
        db.query(Tasting)
        .options(joinedload(Tasting.descriptors))
        .filter(Tasting.id == tasting.id)
        .first()
    )


@router.delete("/{tasting_id}", status_code=204)
def delete_tasting(coffee_id: int, tasting_id: int, db: Session = Depends(get_db)):
    tasting = (
        db.query(Tasting)
        .filter(Tasting.id == tasting_id, Tasting.coffee_id == coffee_id)
        .first()
    )
    if not tasting:
        raise HTTPException(status_code=404, detail="Tasting not found")
    db.delete(tasting)
    db.commit()
