import sys
import asyncio
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
from app.core.database import get_db
from app.core.security import  verify_password, create_access_token
from app.router import products, reviews, categories, orders, employees, tasks, posts, roles, auth, users, admin, attendence, carts, favorites, inventory, order_item, payment, salary,  shipping,  analytics, security_ac, fraud, invoice, marketing, audit_trail , system_log
from app.router.auth import  create_access_token, verify_password
from app.schema.post import PostCreate, PostResponse
from app.models import User, Task, Post
from fastapi.middleware.cors import CORSMiddleware
# from app.utils.security import verify_password, create_access_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(" App is starting up...") # e.g. connect to DB, initialize cache, load configs
    yield
    # Shutdown
    print("App is shutting down gracefully...") # e.g. close DB connections, flush logs, cleanup tasks

app = FastAPI(
    title="Shoes E-Commerce API",
    description="Backend API for managing products, users, and reviews",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )




# Routers
app.include_router(products)
app.include_router(reviews)
app.include_router(users)
app.include_router(categories)
app.include_router(orders)
app.include_router(employees)
app.include_router(tasks)
app.include_router(posts)
app.include_router(roles)
app.include_router(auth.router)
app.include_router(admin)
app.include_router(attendence)
app.include_router(carts)
app.include_router(favorites)
app.include_router(inventory)
app.include_router(order_item)
app.include_router(payment)
app.include_router(salary)
app.include_router(analytics)
app.include_router(shipping)
# app.include_router(log)
app.include_router(security_ac)
app.include_router(fraud)
app.include_router(invoice)
app.include_router(marketing)
app.include_router(audit_trail)
app.include_router(system_log)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application"}



class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login" )
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == data.email).first()
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}
    except Exception as ex:
        print(f"Error occurred: {ex}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {ex}")



@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    try:
        users = db.query(User).limit(50).all()
        tasks = db.query(Task).limit(50).all()

        users_data: List[Dict[str, Any]] = [
            {"user_id": u.user_id, "username": u.username, "email": u.email}
            for u in users
        ]
        tasks_data: List[Dict[str, Any]] = [
            {"id": t.id, "title": t.title, "status": t.status}
            for t in tasks
        ]

        return {"users": users_data, "tasks": tasks_data}

    except Exception as ex:
        print(f"Error occurred: {ex}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {ex}"
        )

# Create Post
@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    try:
        #  In production, get user_id from JWT token
        user_id = 1  # Replace with actual authentication logic

        new_post = Post(
            title=post.title,
            content=post.content,
            user_id=user_id
        )

        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return new_post
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")



# Get All Posts
@app.get("/posts", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    try:
        posts = db.query(Post).all()
        return posts
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


if sys.platform.startswith("win"): 
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
