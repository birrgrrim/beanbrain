from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Coffee, GrinderSetting
from ..schemas import GrinderSettingCreate, GrinderSettingOut
from ._helpers import get_or_404

router = APIRouter(prefix="/coffees/{coffee_id}/settings", tags=["grinder settings"])


@router.get("/", response_model=list[GrinderSettingOut])
def list_grinder_settings(coffee_id: int, db: Session = Depends(get_db)):
    get_or_404(db, Coffee, coffee_id, "Coffee not found")

    return (
        db.query(GrinderSetting)
        .options(
            joinedload(GrinderSetting.grinder),
            joinedload(GrinderSetting.brew_setup),
        )
        .filter(GrinderSetting.coffee_id == coffee_id)
        .all()
    )


@router.post("/", response_model=GrinderSettingOut, status_code=201)
def create_grinder_setting(
    coffee_id: int, data: GrinderSettingCreate, db: Session = Depends(get_db)
):
    get_or_404(db, Coffee, coffee_id, "Coffee not found")

    setting = GrinderSetting(
        coffee_id=coffee_id,
        grinder_id=data.grinder_id,
        brew_setup_id=data.brew_setup_id,
        setting=data.setting,
        notes=data.notes,
    )
    db.add(setting)
    db.commit()
    db.refresh(setting)

    return (
        db.query(GrinderSetting)
        .options(
            joinedload(GrinderSetting.grinder),
            joinedload(GrinderSetting.brew_setup),
        )
        .filter(GrinderSetting.id == setting.id)
        .first()
    )


@router.delete("/{setting_id}", status_code=204)
def delete_grinder_setting(
    coffee_id: int, setting_id: int, db: Session = Depends(get_db)
):
    setting = (
        db.query(GrinderSetting)
        .filter(GrinderSetting.id == setting_id, GrinderSetting.coffee_id == coffee_id)
        .first()
    )
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    db.delete(setting)
    db.commit()
