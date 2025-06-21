from fastapi import FastAPI
# from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from api.models import User, Competency, UserCompetencies
# from api.db_models import get_engine

from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session 

from api.database import handlers
from api.exceptions import UserNotFound

app = FastAPI()

app.mount("/api/",app)
app.mount("/static", StaticFiles(directory="static", html=True, ),name="static")

# https://stackoverflow.com/questions/65916537/a-minimal-fastapi-example-loading-index-html
# @app.get("/")
# async def read_index():
#     return FileResponse('svg3.html')






from typing import List
from pydantic import EmailStr
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
class Base(DeclarativeBase):
    pass

# using declarative:
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
### https://docs.sqlalchemy.org/en/20/orm/quickstart.html



# child 1
class DB_User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(50))
    username : Mapped[str] = mapped_column(String(50))
    email : Mapped[str] = mapped_column(String(50))
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

@app.get("/users/{userid}/competencies/") 
async def competencies(userid:int) -> UserCompetencies:
    ''' retrieve user's competencies from database '''
    return {"user":1,"competencies":[{"quadrant":1, "sector":1, "rating":1}]}

@app.post("/users/new/")
async def adduser(userdata:User):    #translate this to a DB_User
    ''' Add a user to database '''
    # convert from pydantic model to DB model:
    _user = DB_User(name=userdata.name, email=userdata.email, username=userdata.username)
    handlers.add_user(engine,_user)
    return {"usercreated":True}

@app.post("/users/competency/")
async def update_or_add_competency(competency:Competency):    #todo: make pydantic model
    ''' Add a user to database '''
    print(competency)
    return {"updated":True}



# https://www.uvicorn.org/#command-line-options
if __name__ == "__main__":
    uvicorn.run("compass:app", host="0.0.0.0", port=8080, reload=True)
