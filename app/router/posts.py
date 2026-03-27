from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.post import Post
from app.schema.post import PostCreate, PostUpdate, PostOut

router = APIRouter(prefix="/posts", tags=["Posts"])

# List all posts
@router.get("/", response_model=list[PostOut])
def list_posts(db: Session = Depends(get_db)):
    try:
        posts = db.query(Post).filter(Post.is_deleted == False).all()
        return posts
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching posts: {ex}")

# Get post by ID
@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(Post).filter(Post.post_id == post_id, Post.is_deleted == False).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching post: {ex}")

# Create post
@router.post("/", response_model=PostOut)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    try:
        new_post = Post(**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating post: {ex}")

# Update post
@router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        for key, value in post_update.dict(exclude_unset=True).items():
            setattr(post, key, value)
        db.commit()
        db.refresh(post)
        return post
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating post: {ex}")

# Soft delete post
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        post.is_deleted = True
        db.commit()
        return {"message": "Post soft deleted"}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting post: {ex}")

# Restore post
@router.patch("/{post_id}/restore", response_model=PostOut)
def restore_post(post_id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        post.is_deleted = False
        db.commit()
        db.refresh(post)
        return post
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error restoring post: {ex}")
