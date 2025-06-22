from fastapi import FastAPI
# from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import APIRouter

from api.models import User, Competency, UserCompetencies
# from api.db_models import get_engine

from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session 

# from routes import admin_routes
from api.database import handlers
from api.db_models import DB_Competency, DB_User
from api.exceptions import UserNotFound, CompetencyNotFound, CompetenciesForUserNotFound

app = FastAPI()

app.mount("/api/",app)
app.mount("/static", StaticFiles(directory="static", html=True, ),name="static")

# include the subrouter(s)
# app.include_router(
#     admin_routes.router,
#     prefix="/admin"
# )

# https://stackoverflow.com/questions/65916537/a-minimal-fastapi-example-loading-index-html
# @app.get("/")
# async def read_index():
#     return FileResponse('svg3.html')


# from typing import List
# from pydantic import EmailStr
# from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
class Base(DeclarativeBase):
    pass

# using declarative:
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
### https://docs.sqlalchemy.org/en/20/orm/quickstart.html



# # child 1
# class DB_User(Base):
#     __tablename__ = "users"
#     id : Mapped[int] = mapped_column(primary_key=True)
#     name : Mapped[str] = mapped_column(String(50))
#     username : Mapped[str] = mapped_column(String(50))
#     email : Mapped[str] = mapped_column(String(50))
#     competencies : Mapped[List["DB_Competency"]] = relationship(
#         back_populates= "user",cascade="all, delete-orphan"
#     )


# # child 2
# class DB_Competency(Base):
#     __tablename__ = "competencies"
#     id : Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     quadrant = mapped_column(Integer)
#     sector = mapped_column(Integer)
#     rating = mapped_column(Integer)
#     user:Mapped["DB_User"] = relationship(back_populates="competencies")


# # parent
# class DB_UserCompetencies(Base):
#     __tablename__ = "user_competencies"
#     id = mapped_column(Integer, primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     user: Mapped["User"] = relationship(back_populates=)
#     competency_id = Mapped[int] = mapped_column(ForeignKey("competencies.id"))
#     rating = mapped_column(Integer, min=0, max=5)

# test DB
DATABASE_URI = "sqlite:///./database/db.sqlite"
engine = create_engine(DATABASE_URI, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# print(engine, SessionLocal, Base)

# and generate teh SQL:
Base.metadata.create_all(engine)


# return engine


@app.get("/")
async def root():
    return {"api":"root"}

@app.get("/users/{userid}/")
async def user(userid:int):
    ''' retrieve user from database '''
    try:
        result = handlers.get_user(engine, userid)
        return result
    except UserNotFound as ex:
        return {"An exception ocurred":ex}  # to fix later...

@app.get("/users/{userid}/exists/")
async def check_user_exists(userid:int):
    result = handlers.check_user_exists(engine, userid)
    return result
    

@app.get("/users/{user_id}/competencies/") 
async def competencies(user_id:int) -> list[Competency]:
    ''' retrieve user's competencies from database '''
    # return {"user":1,"competencies":[{"quadrant":1, "sector":1, "rating":1}]}
    try:
        result = handlers.get_competencies_for_user(engine, user_id)
        return result
    except CompetenciesForUserNotFound as ex:
        return []
        return {"An exception ocurred":ex}  # to fix later... 


@app.post("/users/new/")
async def adduser(userdata:User):    #translate this to a DB_User
    ''' Add a user to database '''
    # convert from pydantic model to DB model:
    _user = DB_User(name=userdata.name, email=userdata.email, username=userdata.username)
    handlers.add_user(engine,_user)
    return {"usercreated":True}

@app.get("/competencies/{competency_id}")
async def competency(competency_id:int) -> Competency:
    ''' retrieve competency from database '''
    try:
        result = handlers.get_competency(engine, competency_id)
        return result
    except CompetencyNotFound as ex:
        return {"An exception ocurred":ex}  # to fix later...    
    

# # https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
# @app.get("/competencies/{user_id}")
# async def get_competencies_for_user(user_id:int) -> list[Competency]:
#     ''' retrieve competencies for user from database '''
#     try:
#         result = handlers.get_competencies_for_user(engine, user_id)
#         return result
#     except CompetencyNotFound as ex:
#         return []
#         return {"An exception ocurred":ex}  # to fix later... 


@app.post("/competencies/add/")
async def add_competency(competency:Competency):    #todo: make pydantic model
    ''' Add a user competency to database. Note this includes a user_id, so we end up
     with a 1:many relationship. This should fail if an unknown user_id is passed, and if the various
      indices for the values are out of bounds or if this competency is already applied
      to specified user. '''
    _competency = DB_Competency(user_id=competency.user_id,quadrant=competency.quadrant, sector=competency.sector, rating=competency.rating)
    result = handlers.add_competency(engine,_competency)
    return result

# TES
@app.post("/competency/{user_id}") 
async def competencies(competency:Competency):
    result = handlers.check_competency_is_applied_to_user_already(engine=engine,competency=competency)
    return result



# https://www.uvicorn.org/#command-line-options
if __name__ == "__main__":
    uvicorn.run("compass:app", host="0.0.0.0", port=8080, reload=True)
