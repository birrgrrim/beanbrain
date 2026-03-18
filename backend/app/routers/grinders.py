from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Grinder
from ..schemas import GrinderCreate, GrinderOut, GrinderUpdate

router = APIRouter(prefix="/grinders", tags=["grinders"])


@router.get("/", response_model=list[GrinderOut])
def list_grinders(db: Session = Depends(get_db)):
    return db.query(Grinder).all()


@router.post("/", response_model=GrinderOut, status_code=201)
def create_grinder(data: GrinderCreate, db: Session = Depends(get_db)):
    if data.is_default:
        db.query(Grinder).filter(Grinder.is_default == True).update({"is_default": False})
    grinder = Grinder(**data.model_dump())
    db.add(grinder)
    db.commit()
    db.refresh(grinder)
    return grinder


@router.put("/{grinder_id}", response_model=GrinderOut)
def update_grinder(grinder_id: int, data: GrinderUpdate, db: Session = Depends(get_db)):
    grinder = db.query(Grinder).filter(Grinder.id == grinder_id).first()
    if not grinder:
        raise HTTPException(status_code=404, detail="Grinder not found")
    update = data.model_dump(exclude_unset=True)
    if update.get("is_default"):
        db.query(Grinder).filter(Grinder.is_default == True).update({"is_default": False})
    for k, v in update.items():
        setattr(grinder, k, v)
    db.commit()
    db.refresh(grinder)
    return grinder


@router.delete("/{grinder_id}", status_code=204)
def delete_grinder(grinder_id: int, db: Session = Depends(get_db)):
    grinder = db.query(Grinder).filter(Grinder.id == grinder_id).first()
    if not grinder:
        raise HTTPException(status_code=404, detail="Grinder not found")
    db.delete(grinder)
    db.commit()
