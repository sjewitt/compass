from fastapi import APIRouter
from api.database import handlers
router=APIRouter()

@router.get("/") 
async def competencies():
    return {"admin":"test"}

@router.get("/users") 
async def competencies():
    return {"admin":"users"}

@router.get("/competency/{user_id}") 
async def competencies():
    handlers.check_competency_is_applied_to_user_already
    return {"admin":"users"}
