from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import get_db
from app.models import Category
from app.schema import CategoryCreate, CategoryUpdate, CategoryOut, CategorySchema
from typing import List

router = APIRouter(prefix="/categories", tags=["Categories"])



@router.get("/categories/", response_model=List[CategorySchema])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

# POST /categories → Create category
@router.post("/", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        new_category = Category(**category.dict())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except SQLAlchemyError as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create category: {str(ex)}")


# PUT /categories/{id} → Update category
@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, update_data: CategoryUpdate, db: Session = Depends(get_db)):
    try:
        category = db.query(Category).filter(
            Category.category_id == category_id,
            Category.is_deleted == 0
        ).first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(category, key, value)

        db.commit()
        db.refresh(category)
        return category
    except SQLAlchemyError as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update category: {str(ex)}")


# DELETE /categories/{id} → Soft delete category
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        category = db.query(Category).filter(Category.category_id == category_id).first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        category.is_deleted = 1
        db.commit()
        return {"message": "Category soft deleted successfully"}
    except SQLAlchemyError as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete category: {str(ex)}")
