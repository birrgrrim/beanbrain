from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Roastery
from ..schemas import RoasteryCreate, RoasteryOut, RoasteryUpdate
from ._helpers import get_or_404

router = APIRouter(prefix="/roasteries", tags=["roasteries"])


@router.get("/", response_model=list[RoasteryOut])
def list_roasteries(db: Session = Depends(get_db)):
    return db.query(Roastery).filter(Roastery.is_active == True).order_by(Roastery.name).all()


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


@router.delete("/{roastery_id}", status_code=204)
def delete_roastery(roastery_id: int, db: Session = Depends(get_db)):
    roastery = get_or_404(db, Roastery, roastery_id, "Roastery not found")
    roastery.is_active = False
    db.commit()
