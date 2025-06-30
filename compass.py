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

from api.models import Competency, CreateUser
from api.database import handlers
from api.db_models import DB_Competency, DB_User, Base
from api.exceptions import UserNotFound, CompetenciesForUserNotFound

app = FastAPI()

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


# https://www.uvicorn.org/#command-line-options
if __name__ == "__main__":
    uvicorn.run("compass:app", host="0.0.0.0", port=8080, reload=True)
