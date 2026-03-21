from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Taster, Review
from ..schemas import TasterCreate, TasterOut

router = APIRouter(prefix="/tasters", tags=["tasters"])


@router.get("/", response_model=list[TasterOut])
def list_tasters(db: Session = Depends(get_db)):
    return db.query(Taster).order_by(Taster.name).all()


@router.post("/", response_model=TasterOut, status_code=201)
def create_taster(data: TasterCreate, db: Session = Depends(get_db)):
    existing = db.query(Taster).filter(Taster.name == data.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Taster already exists")
    taster = Taster(name=data.name)
    db.add(taster)
    db.commit()
    db.refresh(taster)
    return taster


@router.put("/{taster_id}", response_model=TasterOut)
def update_taster(taster_id: int, data: TasterCreate, db: Session = Depends(get_db)):
    taster = db.query(Taster).filter(Taster.id == taster_id).first()
    if not taster:
        raise HTTPException(status_code=404, detail="Taster not found")
    taster.name = data.name
    taster.avatar = data.avatar
    db.commit()
    db.refresh(taster)
    return taster


@router.delete("/{taster_id}", status_code=204)
def delete_taster(taster_id: int, db: Session = Depends(get_db)):
    taster = db.query(Taster).filter(Taster.id == taster_id).first()
    if not taster:
        raise HTTPException(status_code=404, detail="Taster not found")
    db.delete(taster)
    db.commit()


@router.get("/{taster_id}/dependents")
def taster_dependents(taster_id: int, db: Session = Depends(get_db)):
    """Count records that would be deleted if this taster is removed."""
    reviews = db.query(Review).filter(Review.taster_id == taster_id).count()
    return {"reviews": reviews}


