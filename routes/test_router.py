from fastapi import APIRouter

router = APIRouter(
    prefix="/test",
    tags=["TEST"],
)

@router.get("/")
async def test():
    return {"about":"router test"}