from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.favorites import Favorite
from app.schema.favorites import FavoriteCreate, FavoriteUpdate, FavoriteOut

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.get("/", response_model=list[FavoriteOut])
def list_favorites(db: Session = Depends(get_db)):
    try:
        return db.query(Favorite).filter(Favorite.is_deleted == False).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching favorites: {ex}")

@router.get("/{favorite_id}", response_model=FavoriteOut)
def get_favorite(favorite_id: int, db: Session = Depends(get_db)):
    try:
        fav = db.query(Favorite).filter(Favorite.favorite_id == favorite_id, Favorite.is_deleted == False).first()
        if not fav:
            raise HTTPException(status_code=404, detail="Favorite not found")
        return fav
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching favorite: {ex}")

@router.post("/", response_model=FavoriteOut)
def create_favorite(favorite: FavoriteCreate, db: Session = Depends(get_db)):
    try:
        new_fav = Favorite(**favorite.dict())
        db.add(new_fav)
        db.commit()
        db.refresh(new_fav)
        return new_fav
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating favorite: {ex}")

@router.put("/{favorite_id}", response_model=FavoriteOut)
def update_favorite(favorite_id: int, favorite_update: FavoriteUpdate, db: Session = Depends(get_db)):
    try:
        fav = db.query(Favorite).filter(Favorite.favorite_id == favorite_id).first()
        if not fav:
            raise HTTPException(status_code=404, detail="Favorite not found")
        for key, value in favorite_update.dict(exclude_unset=True).items():
            setattr(fav, key, value)
        db.commit()
        db.refresh(fav)
        return fav
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating favorite: {ex}")

@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: int, db: Session = Depends(get_db)):
    try:
        fav = db.query(Favorite).filter(Favorite.favorite_id == favorite_id).first()
        if not fav:
            raise HTTPException(status_code=404, detail="Favorite not found")
        fav.is_deleted = True
        db.commit()
        return {"message": "Favorite soft deleted"}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting favorite: {ex}")

@router.patch("/{favorite_id}/restore", response_model=FavoriteOut)
def restore_favorite(favorite_id: int, db: Session = Depends(get_db)):
    try:
        fav = db.query(Favorite).filter(Favorite.favorite_id == favorite_id).first()
        if not fav:
            raise HTTPException(status_code=404, detail="Favorite not found")
        fav.is_deleted = False
        db.commit()
        db.refresh(fav)
        return fav
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error restoring favorite: {ex}")
