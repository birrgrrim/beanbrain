from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import BasketSize, BrewMethod, Equipment
from ..schemas import (
    BasketSizeCreate, BasketSizeOut, BrewMethodCreate, BrewMethodOut,
    EquipmentCreate, EquipmentOut, EquipmentUpdate,
)

router = APIRouter(tags=["equipment"])


# --- Equipment ---

@router.get("/equipment", response_model=list[EquipmentOut])
def list_equipment(db: Session = Depends(get_db)):
    return db.query(Equipment).filter(Equipment.is_active == True).all()


@router.post("/equipment", response_model=EquipmentOut, status_code=201)
def create_equipment(data: EquipmentCreate, db: Session = Depends(get_db)):
    if data.is_default:
        db.query(Equipment).filter(
            Equipment.type == data.type, Equipment.is_default == True
        ).update({"is_default": False})
    eq = Equipment(**data.model_dump())
    db.add(eq)
    db.commit()
    db.refresh(eq)
    return eq


@router.put("/equipment/{eq_id}", response_model=EquipmentOut)
def update_equipment(eq_id: int, data: EquipmentUpdate, db: Session = Depends(get_db)):
    eq = db.query(Equipment).filter(Equipment.id == eq_id).first()
    if not eq:
        raise HTTPException(status_code=404, detail="Equipment not found")
    update = data.model_dump(exclude_unset=True)
    if update.get("is_default"):
        db.query(Equipment).filter(
            Equipment.type == eq.type, Equipment.is_default == True
        ).update({"is_default": False})
    for k, v in update.items():
        setattr(eq, k, v)
    db.commit()
    db.refresh(eq)
    return eq


@router.delete("/equipment/{eq_id}", status_code=204)
def delete_equipment(eq_id: int, db: Session = Depends(get_db)):
    eq = db.query(Equipment).filter(Equipment.id == eq_id).first()
    if not eq:
        raise HTTPException(status_code=404, detail="Equipment not found")
    eq.is_active = False
    db.commit()


# --- Brew Methods ---

@router.get("/brew-methods", response_model=list[BrewMethodOut])
def list_brew_methods(db: Session = Depends(get_db)):
    return db.query(BrewMethod).all()


@router.post("/brew-methods", response_model=BrewMethodOut, status_code=201)
def create_brew_method(data: BrewMethodCreate, db: Session = Depends(get_db)):
    if data.is_default:
        db.query(BrewMethod).filter(BrewMethod.is_default == True).update({"is_default": False})
    bm = BrewMethod(**data.model_dump())
    db.add(bm)
    db.commit()
    db.refresh(bm)
    return bm


@router.delete("/brew-methods/{bm_id}", status_code=204)
def delete_brew_method(bm_id: int, db: Session = Depends(get_db)):
    bm = db.query(BrewMethod).filter(BrewMethod.id == bm_id).first()
    if not bm:
        raise HTTPException(status_code=404, detail="Brew method not found")
    db.delete(bm)
    db.commit()


# --- Basket Sizes ---

@router.get("/basket-sizes", response_model=list[BasketSizeOut])
def list_basket_sizes(db: Session = Depends(get_db)):
    return db.query(BasketSize).order_by(BasketSize.size_grams).all()


@router.post("/basket-sizes", response_model=BasketSizeOut, status_code=201)
def create_basket_size(data: BasketSizeCreate, db: Session = Depends(get_db)):
    if data.is_default:
        db.query(BasketSize).filter(BasketSize.is_default == True).update({"is_default": False})
    bs = BasketSize(**data.model_dump())
    db.add(bs)
    db.commit()
    db.refresh(bs)
    return bs


@router.delete("/basket-sizes/{bs_id}", status_code=204)
def delete_basket_size(bs_id: int, db: Session = Depends(get_db)):
    bs = db.query(BasketSize).filter(BasketSize.id == bs_id).first()
    if not bs:
        raise HTTPException(status_code=404, detail="Basket size not found")
    db.delete(bs)
    db.commit()
