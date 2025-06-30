# this is where the databae models (not pydantic model!) are kept
# - they will MIRROR the pydantic models, but will be used to actually crraete the database tables 
# https://www.geeksforgeeks.org/python/fastapi-sqlite-databases/
# https://plainenglish.io/blog/understanding-sqlalchemys-declarative-base-and-metadata-in-python

# from sqlalchemy import create_engine, Column
# import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from typing import List

# Base = declarative_base()
class Base(DeclarativeBase):
    pass
# from sqlalchemy.orm import sessionmaker, Session 
# # User
# def get_engine():
#     DATABASE_URI = "sqlite:///../database/db.sqlite"
#     engine = create_engine(DATABASE_URI)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#     return engine

# child 1
class DB_User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(50))
    username : Mapped[str] = mapped_column(String(50),unique=True)
    email : Mapped[str] = mapped_column(String(50),unique=True)
    password : Mapped[str] = mapped_column(String(50))
    competencies : Mapped[List["DB_Competency"]] = relationship(
        back_populates= "user",cascade="all, delete-orphan"
    )


# child 2
class DB_Competency(Base):
    __tablename__ = "competencies"
    id : Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    quadrant = mapped_column(Integer)
    sector = mapped_column(Integer)
    rating = mapped_column(Integer)
    user:Mapped["DB_User"] = relationship(back_populates="competencies")
