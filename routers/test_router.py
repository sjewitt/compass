from fastapi import APIRouter
from api.database import handlers
from fastapi import FastAPI, Request, Depends
from api.models import User, Competency, CreateUser, UserCompetencies
# from ..compass import get_engine
from api.database.engine import get_engine

router = APIRouter(
    prefix="/test",
    tags=["TEST"],
    # dependencies=[Depends(get_engine)]
)

engine = get_engine()

@router.get("/")
async def test():
    return {"about":"router test"}

@router.get("/{user_id}/data")
async def get_user_data(user_id:int) -> UserCompetencies:
    user_data = handlers.get_user_data(  engine=engine,user_id=user_id, )
    return user_data