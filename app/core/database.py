from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# import os
from dotenv import load_dotenv
# from app.models import *
from sqlalchemy.orm  import DeclarativeBase


load_dotenv()


# mysql+mysqlconnector://username:Paliwal_jii@localhost:3306/fastapi_app


DATABASE_URL = "mysql+pymysql://root:Paliwal_jii%404522@localhost:3306/tpm_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Base(DeclarativeBase):
    pass

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


