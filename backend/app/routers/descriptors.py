from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Descriptor
from ..schemas import DescriptorOut

router = APIRouter(prefix="/descriptors", tags=["descriptors"])


@router.get("/", response_model=list[DescriptorOut])
def list_descriptors(db: Session = Depends(get_db)):
    return db.query(Descriptor).order_by(Descriptor.category, Descriptor.name).all()
