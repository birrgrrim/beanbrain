from fastapi import HTTPException
from sqlalchemy.orm import Session


def get_or_404(db: Session, model, id: int, detail: str = "Not found"):
    obj = db.query(model).filter(model.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=detail)
    return obj


def clear_default(db: Session, model) -> None:
    db.query(model).filter(model.is_default.is_(True)).update({"is_default": False})
