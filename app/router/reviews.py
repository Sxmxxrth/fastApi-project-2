from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app import models, schema

router = APIRouter(prefix="/reviews", tags=["reviews"])

# Create review
@router.post("/", response_model=schema.ReviewOut)
def create_review(review: schema.ReviewCreate, db: Session = Depends(get_db), user_id: int = 1):
    try:
        new_review = models.Review(
            user_id=user_id,
            product_id=review.product_id,
            rating=review.rating,
            description=review.description,
            fit_feedback=review.fit_feedback,
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating review: {ex}")

# Get single review
@router.get("/{review_id}", response_model=schema.ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    try:
        review = db.query(models.Review).filter(
            models.Review.review_id == review_id,
            models.Review.is_deleted == False
        ).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return review
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching review: {ex}")

# Get reviews for a product
@router.get("/product/{product_id}", response_model=list[schema.ReviewOut])
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    try:
        return db.query(models.Review).filter(
            models.Review.product_id == product_id,
            models.Review.is_deleted == False
        ).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching product reviews: {ex}")

# Update review
@router.put("/{review_id}", response_model=schema.ReviewOut)
def update_review(review_id: int, updated: schema.ReviewUpdate, db: Session = Depends(get_db), user_id: int = 1):
    try:
        review = db.query(models.Review).filter(
            models.Review.review_id == review_id,
            models.Review.user_id == user_id
        ).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found or not authorized")
        for key, value in updated.dict(exclude_unset=True).items():
            setattr(review, key, value)
        db.commit()
        db.refresh(review)
        return review
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating review: {ex}")

# Soft delete review
@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), user_id: int = 1):
    try:
        review = db.query(models.Review).filter(
            models.Review.review_id == review_id,
            models.Review.user_id == user_id
        ).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found or not authorized")
        review.is_deleted = True
        db.commit()
        return {"message": "Review deleted successfully"}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting review: {ex}")
