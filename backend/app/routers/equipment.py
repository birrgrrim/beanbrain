from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import BasketSize, BrewMethod, Equipment
from ..schemas import BasketSizeOut, BrewMethodOut, EquipmentOut

router = APIRouter(tags=["equipment"])


@router.get("/equipment", response_model=list[EquipmentOut])
def list_equipment(db: Session = Depends(get_db)):
    return db.query(Equipment).filter(Equipment.is_active == True).all()


@router.get("/brew-methods", response_model=list[BrewMethodOut])
def list_brew_methods(db: Session = Depends(get_db)):
    return db.query(BrewMethod).all()


@router.get("/basket-sizes", response_model=list[BasketSizeOut])
def list_basket_sizes(db: Session = Depends(get_db)):
    return db.query(BasketSize).order_by(BasketSize.size_grams).all()
