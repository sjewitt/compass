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

class DB_Competency(Base):
    __tablename__ = "competencies"
    id : Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    quadrant = mapped_column(Integer)
    sector = mapped_column(Integer)
    rating = mapped_column(Integer)
    user:Mapped["DB_User"] = relationship(back_populates="competencies")

class DB_Quadrant(Base):
    __tablename__ = "quandrants"
    id : Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["DB_QuadrantTitles"]] = relationship(back_populates='parent')
    quadrant_summary: Mapped[str] = mapped_column(String)
    quadrant_css_class: Mapped[str] = mapped_column(String)
    quadrant_elem_coords: Mapped[str] = mapped_column(String)

# titles may be > 1 line, so we need lookup option
class DB_QuadrantTitles(Base):
    __tablename__ = "quandrant_titles"
    id : Mapped[int] = mapped_column(primary_key=True)
    quadrant_id : Mapped[int] = mapped_column(ForeignKey("quandrants.id"))
    title_part : Mapped[str] = mapped_column(String)
    parent: Mapped["DB_Quadrant"] = relationship(back_populates="children")

class DB_Sector(Base):
    __tablename__ = "sectors"
    id : Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["DB_SectorTitles"]] = relationship(back_populates='parent')
    # each sector belongs to a quadrant:
    quadrant_id : Mapped[int] = mapped_column(ForeignKey("quandrants.id"))
    summary: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

class DB_SectorTitles(Base):
    __tablename__ = "sector_titles"
    id : Mapped[int] = mapped_column(primary_key=True)
    sector_id : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    title_part : Mapped[str] = mapped_column(String)
    coord_x :  Mapped[int] = mapped_column(Integer)
    coord_y :  Mapped[int] = mapped_column(Integer)
    parent: Mapped["DB_Sector"] = relationship(back_populates="children")


