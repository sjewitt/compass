from fastapi import APIRouter
from utilities.data_utilities import load_config_data
from api.database.engine import get_engine

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)

engine = get_engine()
compass_config_data = load_config_data(engine=engine, caller="settings")

  
# endpoint for settings/json config retrieval
# not even sure I need this any more.
@router.get("/compass_config/") 
def get_json_config_as_dict(compass_id:int=None):
    return load_config_data(engine=engine, caller="settings",compass_id=compass_id)


# reload config data so we don't need to restart:
@router.get("/compass_config/reload/") 
def reload_json_config():
    load_config_data(engine=engine, caller="settings (reload)")
    return {"message":"loaded config data","status":"ok"}
