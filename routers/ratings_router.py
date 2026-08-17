from fastapi import APIRouter

from api.database.engine import get_engine
from utilities.data_utilities import load_config_data

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"],
)

engine = get_engine()
