# this is where the databae models (not pydantic model!) are kept
# - they will MIRROR the pydantic models, but will be used to actually crraete the database tables 
# https://www.geeksforgeeks.org/python/fastapi-sqlite-databases/
# https://plainenglish.io/blog/understanding-sqlalchemys-declarative-base-and-metadata-in-python

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from typing import List

class Base(DeclarativeBase): 
    pass


class DB_User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key=True)
    # TO CHECK ON REBUILD:
    compass_id: Mapped[int] = mapped_column(ForeignKey("compass_definition.id"))
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
    def __repr__(self):
        return "<DB_Competency(id='%s', user_id='%s', quadrant='%s', sector='%s', rating='%s')>" % (
            self.id, self.user_id, self.quadrant, self.sector, self.rating
        )

class DB_Quadrant(Base):
    __tablename__ = "quadrants"
    id : Mapped[int] = mapped_column(primary_key=True)
    quadrant_summary: Mapped[str] = mapped_column(String)
    quadrant_description: Mapped[str] = mapped_column(String)
    # quadrant_css_class: Mapped[str] = mapped_column(String)
    # quadrant_elem_coords: Mapped[str] = mapped_column(String)   # not needed
    def __repr__(self):
        return "<DB_Quadrant(id='%s', quadrant_summary='%s', quadrant_description='%s')>" % (
            self.id, self.quadrant_summary, self.quadrant_description
        )


class DB_QuadrantTitles(Base):
    __tablename__ = "quadrant_titles"
    id : Mapped[int] = mapped_column(primary_key=True)
    title_part : Mapped[str] = mapped_column(String)
    # coord_x :  Mapped[int] = mapped_column(Integer)
    # coord_y :  Mapped[int] = mapped_column(Integer)
    def __repr__(self):
        return "<DB_QuadrantTitles(id='%s', title_part='%s')>" % (
            self.id, self.title_part
        )


class DB_Sector(Base):
    __tablename__ = "sectors"
    id : Mapped[int] = mapped_column(primary_key=True)
    summary: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    def __repr__(self):
        return "<DB_Sector(id='%s', summary='%s', description='%s')>" % (
            self.id, self.summary, self.description
        )


class DB_SectorTitles(Base):
    __tablename__ = "sector_titles"
    id : Mapped[int] = mapped_column(primary_key=True)
    title_part : Mapped[str] = mapped_column(String)
    # coord_x :  Mapped[int] = mapped_column(Integer)
    # coord_y :  Mapped[int] = mapped_column(Integer)
    def __repr__(self):
        return "<DB_SectorTitles(id='%s', title_part='%s')>" % (
            self.id, self.title_part
        )


class DB_Rating(Base):
    __tablename__ = "rating"
    id : Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)  # max length?
    description: Mapped[str] = mapped_column(String)
    def __repr__(self):
        return "<DB_Rating(id='%s', title='%s', description='%s')>" % (
            self.id, self.title, self.description
        )

class DB_CompassDefinition(Base):
    __tablename__ = "compass_definition"
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String)
    description : Mapped[str] = mapped_column(String)

    # Specify the quadrants (4)
    quadrant_1 : Mapped[int] = mapped_column(ForeignKey("quadrants.id"))
    quadrant_2 : Mapped[int] = mapped_column(ForeignKey("quadrants.id"))
    quadrant_3 : Mapped[int] = mapped_column(ForeignKey("quadrants.id"))
    quadrant_4 : Mapped[int] = mapped_column(ForeignKey("quadrants.id"))

    # specify quadrant_title parts:
    q1_tp1 : Mapped[int] = mapped_column(ForeignKey("quadrant_titles.id"))
    q1_tp2 : Mapped[int] = mapped_column(ForeignKey("quadrant_titles.id"))
    q2_tp1 : Mapped[int] = mapped_column(ForeignKey("quadrant_titles.id"))
    q2_tp2 : Mapped[int] = mapped_column(ForeignKey("quadrant_titles.id"))
    q3_tp1 : Mapped[int] = mapped_column(ForeignKey("quadrant_titles.id"))
    q3_tp2 : Mapped[int] = mapped_column(ForeignKey("quadrant_titles.id"))
    q4_tp1 : Mapped[int] = mapped_column(ForeignKey("quadrant_titles.id"))
    q4_tp2 : Mapped[int] = mapped_column(ForeignKey("quadrant_titles.id"))

    # specify the sectors per quadrant (5, 4, 4, 4)
    quadrant_1_sector_1 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    quadrant_1_sector_2 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    quadrant_1_sector_3 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    quadrant_1_sector_4 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    quadrant_1_sector_5 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))

    # specify q1 sector titles
    q1_s1_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q1_s1_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q1_s2_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q1_s2_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q1_s3_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q1_s3_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q1_s4_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q1_s4_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q1_s5_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q1_s5_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))

    quadrant_2_sector_1 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    quadrant_2_sector_2 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    quadrant_2_sector_3 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    quadrant_2_sector_4 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))

    # specify q2 sector titles
    q2_s1_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q2_s1_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q2_s2_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q2_s2_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q2_s3_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q2_s3_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q2_s4_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q2_s4_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))

    quadrant_3_sector_1 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    quadrant_3_sector_2 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    quadrant_3_sector_3 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    quadrant_3_sector_4 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))

    # specify q3 sector titles
    q3_s1_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q3_s1_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q3_s2_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q3_s2_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q3_s3_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q3_s3_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q3_s4_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q3_s4_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))

    quadrant_4_sector_1 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    quadrant_4_sector_2 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    quadrant_4_sector_3 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))
    quadrant_4_sector_4 : Mapped[int] = mapped_column(ForeignKey("sectors.id"))

    # specify q4 sector titles
    q4_s1_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q4_s1_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q4_s2_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q4_s2_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q4_s3_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q4_s3_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q4_s4_tp1 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))
    q4_s4_tp2 : Mapped[int] = mapped_column(ForeignKey("sector_titles.id"))

    # and the Ratings (7!!):
    rating_1 : Mapped[int] = mapped_column(ForeignKey("rating.id"))
    rating_2 : Mapped[int] = mapped_column(ForeignKey("rating.id"))
    rating_3 : Mapped[int] = mapped_column(ForeignKey("rating.id"))
    rating_4 : Mapped[int] = mapped_column(ForeignKey("rating.id"))
    rating_5 : Mapped[int] = mapped_column(ForeignKey("rating.id"))
    rating_6 : Mapped[int] = mapped_column(ForeignKey("rating.id"))
    rating_7 : Mapped[int] = mapped_column(ForeignKey("rating.id"))