
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# https://fastapi.tiangolo.com/advanced/templates/
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import uvicorn

from api.models import User, Competency, CreateUser, UserCompetencies  # adde usercompetencies model
from api.database import handlers
from api.db_models import DB_Competency, DB_User, Base
from api.exceptions import UserNotFound, CompetenciesForUserNotFound, CompetencyOutOfRange
from api.constants import COMPASS_MAPPER, RATING_MAPPER

app = FastAPI()

# #48:
# load JSON file as used by the front-end to obtain the static values:

with open(mode="r",file="./static/data/display_data.json") as display_data:
    # TODO:
    # print(os.getcwd())
    # print()
    display_data.read()
    print(dict( display_data))
    display_data.close()

app.mount("/api/",app)
app.mount("/static", StaticFiles(directory="static", html=True, ),name="static")

# declare location of template(s)
templates = Jinja2Templates(directory="templates")

# test DB
DATABASE_URI = "sqlite:///./database/db.sqlite"
engine = create_engine(DATABASE_URI, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# and generate teh SQL:
Base.metadata.create_all(engine)


@app.get("/")
async def root():
    return RedirectResponse("/static/")

# template test:
@app.get("/{user_id}")
async def template_test(request: Request,user_id:int):
    _user = handlers.get_user(engine, user_id)
    return templates.TemplateResponse(
        request=request,name="index.html", context={"user":_user}
    )

@app.get("/{user_id}/edit/")
async def update_user(request: Request,user_id:int) -> User:
    ''' update user's competencies in database '''
    _user = handlers.get_user(engine, user_id)  # get current state of user
    return templates.TemplateResponse(
        request=request,name="user_edit.html", context={"user":_user}
    )


@app.get("/{user_id}/data")
async def get_user_data(user_id:int) -> UserCompetencies:
    user_data = handlers.get_user_data(engine, user_id)
    return user_data

from io import StringIO
import datetime
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
@app.get("/{user_id}/data/csv",response_class=StreamingResponse)
async def download_user_data_csv(user_id:int):   # -> UserCompetencies:
    user_data = handlers.get_user_data(engine, user_id)
    csv_data = ""
    header = ",".join(['Quadrant','Sector','Rating'])
    header = header+"\n"
    csv_data = header
    for comp in user_data.competencies:
        row = ",".join([COMPASS_MAPPER[comp.quadrant]['quadrant'], COMPASS_MAPPER[comp.quadrant]['sectors'][comp.sector], RATING_MAPPER[comp.rating]['title']])
        csv_data = csv_data+row+"\n"
    # response = FileResponse(csv_data)
    response = StreamingResponse(csv_data)
    
    _cd = f"attachment; filename={user_data.user.username}_{datetime.datetime.now()}.csv"
    response.headers["Content-Disposition"] = _cd
    print(csv_data)
    # return user_data
    return response


@app.get("/{user_id}/data/json",response_class=FileResponse)
async def download_user_data_json(user_id:int):# -> UserCompetencies:
    user_data = handlers.get_user_data(engine, user_id)
    response = JSONResponse(user_data.model_dump())
    _cd = f"attachment; filename={user_data.user.username}_{datetime.datetime.now()}.json"
    response.headers["Content-Disposition"] = _cd
    return response
    # https://www.geeksforgeeks.org/python/stringio-and-bytesio-for-managing-data-as-file-object/




@app.get("/users/")
async def users():
    ''' retrieve all users from database '''
    try:
        result = handlers.get_users(engine)
        return result
    except UserNotFound as ex:
        return {"An exception ocurred":ex}  # to fix later...


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
# async def competencies(user_id:int) -> UserCompetencies: #TODO make model
async def competencies(user_id:int) -> list[Competency]:        # orig
    ''' retrieve user's competencies from database '''
    try:
        result = handlers.get_competencies_for_user(engine, user_id) # orig
        # result = handlers.get_user_data(engine, user_id)
        return result
    except CompetenciesForUserNotFound as ex:
        return []


@app.post("/users/{user_id}/edit/")
async def update_user(user:User) -> User:
    ''' update user's competencies in database '''
    
    result = handlers.update_user(engine,user)
    print(result)
    # return data to populate the form:
    return user


@app.post("/users/new/")
async def adduser(userdata:CreateUser) -> dict:    #translate this to a DB_User
    ''' Add a user to database '''
    # convert from pydantic model to DB model:
    if userdata.password == userdata.password_check:
        _user = DB_User(
            name=userdata.name, 
            email=userdata.email, 
            username=userdata.username, 
            password=userdata.password)
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


@app.get("/competencies/{quadrant}/{sector}/")
async def get_competency(quadrant:int, sector:int):
    '''return a competency description by index '''
    # print(COMPASS_MAPPER[quadrant]['quadrant'])
    try:
        return {
            "quadrant":{
                "id":quadrant,
                "value":COMPASS_MAPPER[quadrant]['quadrant'],
            },
            "sector":{
                "id":sector,
                "value":COMPASS_MAPPER[quadrant]['sectors'][sector],
            }
        }
    except IndexError:
        # TODO: construct more informative return values
        return {
            "error":"competency out of range"
        }


@app.get("/rating/{rating}/")
async def get_rating(rating:int):
    '''return a competency description by index '''
    # print(COMPASS_MAPPER[quadrant]['quadrant'])
    try:
        return {
            "rating":{
                "id":rating,
                "value":RATING_MAPPER[rating],
            },
        }
    except IndexError:
        # TODO: construct more informative return values
        return {
            "error":"rating out of range"
        }

# https://www.uvicorn.org/#command-line-options
if __name__ == "__main__":
    uvicorn.run("compass:app", host="0.0.0.0", port=8080, reload=True)
