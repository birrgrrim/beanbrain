from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import BREW_METHOD_TYPES, BrewSetup
from ..schemas import BrewMethodTypeOut, BrewSetupCreate, BrewSetupOut, BrewSetupUpdate
from ._helpers import clear_default, get_or_404

router = APIRouter(tags=["brew setups"])


@router.get("/brew-method-types", response_model=list[BrewMethodTypeOut])
def list_brew_method_types():
    return [
        BrewMethodTypeOut(key=key, icon=info["icon"], has_basket=info["has_basket"])
        for key, info in BREW_METHOD_TYPES.items()
    ]


@router.get("/brew-setups/", response_model=list[BrewSetupOut])
def list_brew_setups(db: Session = Depends(get_db)):
    return db.query(BrewSetup).all()


@router.post("/brew-setups/", response_model=BrewSetupOut, status_code=201)
def create_brew_setup(data: BrewSetupCreate, db: Session = Depends(get_db)):
    if data.method_type not in BREW_METHOD_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid method_type: {data.method_type}")
    if data.is_default:
        clear_default(db, BrewSetup)
    setup = BrewSetup(**data.model_dump())
    db.add(setup)
    db.commit()
    db.refresh(setup)
    return setup


@router.put("/brew-setups/{setup_id}", response_model=BrewSetupOut)
def update_brew_setup(setup_id: int, data: BrewSetupUpdate, db: Session = Depends(get_db)):
    setup = get_or_404(db, BrewSetup, setup_id, "Brew setup not found")
    update = data.model_dump(exclude_unset=True)
    if update.get("is_default"):
        clear_default(db, BrewSetup)
    for k, v in update.items():
        setattr(setup, k, v)
    db.commit()
    db.refresh(setup)
    return setup


@router.delete("/brew-setups/{setup_id}", status_code=204)
def delete_brew_setup(setup_id: int, db: Session = Depends(get_db)):
    setup = get_or_404(db, BrewSetup, setup_id, "Brew setup not found")
    db.delete(setup)
    db.commit()
