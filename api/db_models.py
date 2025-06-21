# this is where the databae models (not pydantic model!) are kept
# - they will MIRROR the pydantic models, but will be used to actually crraete the database tables 
# https://www.geeksforgeeks.org/python/fastapi-sqlite-databases/
# https://plainenglish.io/blog/understanding-sqlalchemys-declarative-base-and-metadata-in-python

from sqlalchemy import create_engine, Column, Integer, String
# import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData

Base = declarative_base()

# from sqlalchemy.orm import sessionmaker, Session 
# # User
# def get_engine():
#     DATABASE_URI = "sqlite:///../database/db.sqlite"
#     engine = create_engine(DATABASE_URI)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#     return engine

class DB_User(Base):
    pass