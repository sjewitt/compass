from fastapi import APIRouter
from api.database import handlers
from api.models import User, Competency, CreateUser
from api.database.engine import get_engine

from utilities.download_utilities import get_sector_title_from_data
from api.models import User, Competency, CreateUser
from api.database import handlers
from api.db_models import DB_User
from api.exceptions import UserNotFound, CompetenciesForUserNotFound

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

engine = get_engine()

@router.get("/")
async def users():
    ''' retrieve all users from database '''
    try:
        result = handlers.get_users(engine)
        return result
    except UserNotFound as ex:
        return {"An exception ocurred":ex}  # to fix later...


@router.get("/{userid}/")
async def user(userid:int) -> User:
    ''' retrieve user from database '''
    try:
        result = handlers.get_user(engine, userid)
        return result
    except UserNotFound as ex:
        raise UserNotFound(status_code=404, detail=str(ex))
    except Exception as ex:
        raise Exception("")

# TODO: emulate above.
@router.get("/{userid}/exists/")
async def check_user_exists(userid:int):
    result = handlers.check_user_exists(engine, userid)
    return result
    

@router.get("/{user_id}/competencies/")
# async def competencies(user_id:int) -> UserCompetencies: #TODO make model
async def competencies(user_id:int) -> list[Competency]:        # orig
    ''' retrieve user's competencies from database '''
    try:
        result = handlers.get_competencies_for_user(engine, user_id) # orig
        # result = handlers.get_user_data(engine, user_id)
        return result
    except CompetenciesForUserNotFound as ex:
        return []


@router.post("/{user_id}/edit/")
async def update_user(user:User) -> User:
    ''' update user's competencies in database '''
    
    result = handlers.update_user(engine,user)
    print(result)
    # return data to populate the form:
    return user


@router.post("/new/")
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