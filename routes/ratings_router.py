from fastapi import APIRouter

from api.database.engine import get_engine
from utilities.data_utilities import load_config_data

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"],
)

engine = get_engine()
compass_config_data = load_config_data()


# only used by API so far
@router.get("/{rating}/")
async def get_rating(rating_id:int):
    '''return a competency description by index '''
    try:
        return {
            "rating":{
                "id":rating_id,
                "value":compass_config_data["configuration"]["rating_description_lookup"][rating_id],
            },
        }
    except IndexError as ex:
        # TODO: construct more informative return values
        return {
            "error":f"rating out of range. {ex}"
        }
    
    except Exception as ex:
        return {
            "error":f"An unexpected error occurred: {ex}"
        }