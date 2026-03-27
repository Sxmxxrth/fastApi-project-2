
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.review import Review
from app.models.order import Order
from app.models.task import Task
from app.models.post import Post
from app.models.employees import Employee
from app.models.roles import Role
from app.schema.user import UserCreate
from app.core.security import get_password_hash, verify_password #create_access_token, verify_token


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_or_404(db: Session, user_id: int) -> User:
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password   # ✅ consistent naming
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> User | bool:
    user = get_user_by_username(db, username=username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):  # ✅ consistent naming
        return False
    return user


def get_category_or_404(db: Session, category_id: int) -> Category: 
    category = db.query(Category).filter(Category.category_id == category_id).first() 
    if not category: 
        raise HTTPException(status_code=404, detail="Category not found") 
    return category

def get_product_or_404(db: Session, product_id: int) -> Product: 
    product = db.query(Product).filter(Product.product_id == product_id).first() 
    if not product: 
        raise HTTPException(status_code=404, detail="Product not found") 
    return product

def get_review_or_404(db: Session, review_id: int) -> Review: 
    review = db.query(Review).filter(Review.review_id == review_id).first() 
    if not review: 
        raise HTTPException(status_code=404, detail="Review not found") 
    return review

def get_order_or_404(db: Session, order_id: int) -> Order: 
    order = db.query(Order).filter(Order.order_id == order_id).first() 
    if not order: 
        raise HTTPException(status_code=404, detail="Order not found") 
    return order

def get_employee_or_404(db: Session, employee_id: int) -> Employee: 
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first() 
    if not employee: 
        raise HTTPException(status_code=404, detail="Employee not found") 
    return employee

def get_task_or_404(db: Session, task_id: int) -> Task: 
    task = db.query(Task).filter(Task.task_id == task_id).first() 
    if not task: 
        raise HTTPException(status_code=404, detail="Task not found") 
    return task

def get_post_or_404(db: Session, post_id: int) -> Post: 
    post = db.query(Post).filter(Post.post_id == post_id).first() 
    if not post: 
        raise HTTPException(status_code=404, detail="Post not found") 
    return post

def get_role_or_404(db: Session, role_id: int) -> Role: 
    role = db.query(Role).filter(Role.role_id == role_id).first() 
    if not role: 
        raise HTTPException(status_code=404, detail="Role not found") 
    return role



