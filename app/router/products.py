from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Product
from app.schema import ProductCreate, ProductUpdate, ProductOut
from app.utils.crud import get_category_or_404
from app.sevices.service import create_product_service, update_product_service



router = APIRouter(prefix="/products", tags=["Products"])


# Create product
@router.post("/", response_model=ProductOut, status_code=201, operation_id="create_product") 
def create_product(product: ProductCreate, db: Session = Depends(get_db)): 
    try:
        # Ensure category_id is provided 
        if product.category_id is None: 
            raise HTTPException(status_code=400, detail="Category ID required") 
        # Ensure stock is provided and non-negative 
        if product.stock is None: 
            raise HTTPException(status_code=400, detail="Stock is required") 
        if product.stock < 0: 
            raise HTTPException(status_code=400, detail="Stock cannot be negative") 
        # Validation: ensure category exists 
        get_category_or_404(db, product.category_id) 
        # Create product 
        db_product = Product(**product.model_dump()) 
        db.add(db_product) 
        db.commit() 
        db.refresh(db_product) 
        return db_product 
    except HTTPException: 
        # Re-raise known HTTP errors without wrapping 
        raise 
    except Exception as ex: 
        raise HTTPException(status_code=500, detail=f"Product creation failed: {str(ex)}")

# Get all products
@router.get("/", response_model=list[ProductOut], operation_id="get_products")
def get_products(skip: int = 0, limit: int = 20,db: Session = Depends(get_db)):
    try:
        return db.query(Product).offset(skip).limit(limit).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Fetching products failed: {str(ex)}")


# Get product by ID
@router.get("/{product_id}", response_model=ProductOut, operation_id="get_product") 
def get_product(product_id: int, db: Session = Depends(get_db)): 
    try: 
        product = db.query(Product).filter(Product.product_id == product_id).first() 
        if not product: 
            raise HTTPException(status_code=404, detail="Product not found") 
        return product 
    except Exception as ex: raise HTTPException(status_code=500, detail=f"Fetching product failed: {str(ex)}")

# Update product
@router.put("/{product_id}", response_model=ProductOut, operation_id="update_product") 
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)): 
    try: 
        db_product = db.query(Product).filter(Product.product_id == product_id).first() 
        if not db_product: 
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found") 
        
        # Apply only provided fields
        for key, value in product.model_dump(exclude_unset=True).items(): 
            setattr(db_product, key, value) 
        
        db.commit() 
        db.refresh(db_product) 
        return db_product 
    
    except HTTPException: 
        raise 
    except Exception as ex: 
        raise HTTPException(status_code=500, detail=f"Product update failed: {str(ex)}")



# Delete product
@router.delete("/{product_id}", operation_id="delete_product")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        db_product = db.query(Product).filter(Product.product_id == product_id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Deleting product failed: {str(ex)}")

# dashboard products
@router.get("/dashboard/products", operation_id="dashboard_products")
def dashboard_products(db: Session = Depends(get_db)):
    try:
        products = db.query(Product).limit(50).all()
        return {"products": products}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Fetching products failed : {str(ex)}")
    