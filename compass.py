from fastapi import FastAPI
<<<<<<< HEAD
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
=======
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# https://fastapi.tiangolo.com/advanced/templates/
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import uvicorn

from api.models import Competency, CreateUser
from api.database import handlers
from api.db_models import DB_Competency, DB_User, Base
from api.exceptions import UserNotFound, CompetenciesForUserNotFound
>>>>>>> api_build

app = FastAPI()

app.mount("/api/",app)
app.mount("/static", StaticFiles(directory="static", html=True, ),name="static")

<<<<<<< HEAD
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
=======
# declare location of template(s)
templates = Jinja2Templates(directory="templates")
>>>>>>> api_build

# test DB
DATABASE_URI = "sqlite:///./database/db.sqlite"
engine = create_engine(DATABASE_URI, echo=True)
<<<<<<< HEAD
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# print(engine, SessionLocal, Base)
=======
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
>>>>>>> api_build

# and generate teh SQL:
Base.metadata.create_all(engine)


<<<<<<< HEAD
# return engine


@app.get("/")
async def root():
    return {"api":"root"}
=======
@app.get("/")
async def root():
    return RedirectResponse("/static/")

# template test:
@app.get("/{user_id}")
async def template_test(request: Request,user_id:int):
    _user = handlers.get_user(engine, user_id)
    print(f"GETTING USER {user_id}")
    print(_user)
    return templates.TemplateResponse(
        request=request,name="index.html", context={"user":_user}
    )
    


@app.get("/users/")
async def users():
    ''' retrieve all users from database '''
    try:
        result = handlers.get_users(engine)
        return result
    except UserNotFound as ex:
        return {"An exception ocurred":ex}  # to fix later...

>>>>>>> api_build

@app.get("/users/{userid}/")
async def user(userid:int):
    ''' retrieve user from database '''
    try:
        result = handlers.get_user(engine, userid)
        return result
    except UserNotFound as ex:
        return {"An exception ocurred":ex}  # to fix later...

<<<<<<< HEAD
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


=======

@app.get("/users/{userid}/exists/")
async def check_user_exists(userid:int):
    result = handlers.check_user_exists(engine, userid)
    return result
    

@app.get("/users/{user_id}/competencies/") 
async def competencies(user_id:int) -> list[Competency]:
    ''' retrieve user's competencies from database '''
    try:
        result = handlers.get_competencies_for_user(engine, user_id)
        return result
    except CompetenciesForUserNotFound as ex:
        return []


@app.post("/users/new/")
async def adduser(userdata:CreateUser) -> dict:    #translate this to a DB_User
    ''' Add a user to database '''
    # convert from pydantic model to DB model:
    if userdata.password == userdata.password_check:
        _user = DB_User(name=userdata.user.name, email=userdata.user.email, username=userdata.user.username, password=userdata.password)
        result = handlers.add_user(engine,_user)

        # https://stackoverflow.com/questions/76047310/how-to-redirect-from-a-post-to-a-get-endpoint-in-fastapi-without-changing-the-re
        if result['usercreated']:
            return {"usercreated":True, "user_id":result["id"]}
        return result
    return {"usercreated":False, "message":"supplied passwords do not match"}


@app.post("/competencies/add/")
async def add_competency(competency:Competency):    #todo: make pydantic model
    ''' Add a user competency to database. Note this includes a user_id, so we end up
     with a 1:many relationship. This should fail if an unknown user_id is passed, and if the various
      indices for the values are out of bounds or if this competency is already applied
      to specified user. '''
    _competency = DB_Competency(user_id=competency.user_id,quadrant=competency.quadrant, sector=competency.sector, rating=competency.rating)
    result = handlers.add_competency(engine,_competency)
    return result

>>>>>>> api_build

# https://www.uvicorn.org/#command-line-options
if __name__ == "__main__":
    uvicorn.run("compass:app", host="0.0.0.0", port=8080, reload=True)
