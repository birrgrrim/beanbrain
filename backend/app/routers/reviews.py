from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Coffee, Descriptor, Review
from ..schemas import ReviewUpsert, ReviewOut

router = APIRouter(prefix="/coffees/{coffee_id}/reviews", tags=["reviews"])


@router.get("/", response_model=list[ReviewOut])
def list_reviews(coffee_id: int, db: Session = Depends(get_db)):
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    return (
        db.query(Review)
        .options(joinedload(Review.descriptors), joinedload(Review.taster))
        .filter(Review.coffee_id == coffee_id)
        .all()
    )


@router.put("/", response_model=ReviewOut)
def upsert_review(coffee_id: int, data: ReviewUpsert, db: Session = Depends(get_db)):
    """Create or update a review. One review per person per coffee."""
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    review = (
        db.query(Review)
        .filter(Review.coffee_id == coffee_id, Review.taster_id == data.taster_id)
        .first()
    )

    if review:
        review.rating = data.rating
        review.comment = data.comment
    else:
        review = Review(
            coffee_id=coffee_id,
            taster_id=data.taster_id,
            rating=data.rating,
            comment=data.comment,
        )
        db.add(review)

    if data.descriptor_ids:
        descriptors = db.query(Descriptor).filter(
            Descriptor.id.in_(data.descriptor_ids)
        ).all()
        review.descriptors = descriptors
    else:
        review.descriptors = []

    db.commit()
    db.refresh(review)

    return (
        db.query(Review)
        .options(joinedload(Review.descriptors), joinedload(Review.taster))
        .filter(Review.id == review.id)
        .first()
    )


@router.delete("/{review_id}", status_code=204)
def delete_review(coffee_id: int, review_id: int, db: Session = Depends(get_db)):
    review = (
        db.query(Review)
        .filter(Review.id == review_id, Review.coffee_id == coffee_id)
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
