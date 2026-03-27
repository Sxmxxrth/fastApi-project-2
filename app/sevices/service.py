from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Product
from app.schema import ProductCreate, ProductUpdate
from app.utils.crud import get_category_or_404

def create_product_service(db: Session, product: ProductCreate) -> Product:
    try:
        if product.stock < 0:
            raise HTTPException(status_code=400, detail="Stock cannot be negative")

        # Ensure category exists
        get_category_or_404(db, product.category_id)

        db_product = Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    except HTTPException:
        # Pass through known validation errors
        raise
    except Exception as ex:
        # Catch unexpected errors
        raise HTTPException(status_code=500, detail=f"Product creation failed: {str(ex)}")


def update_product_service(db: Session, product_id: int, product: ProductUpdate) -> Product:
    try:
        db_product = db.query(Product).filter(Product.product_id == product_id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

        for key, value in product.model_dump(exclude_unset=True).items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)
        return db_product

    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Product update failed: {str(ex)}")
