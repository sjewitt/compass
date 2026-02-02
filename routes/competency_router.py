from fastapi import APIRouter

from api.models import Competency  # adde usercompetencies model
from api.db_models import DB_Competency
from api.database.engine import get_engine
from api.database import handlers
from utilities.download_utilities import get_sector_title_from_data
from utilities.data_utilities import load_config_data

router = APIRouter(
    prefix="/competencies",
    tags=["Competencies"],
)

engine = get_engine()
compass_config_data = load_config_data()

@router.post("/add/")
async def add_competency(competency:Competency):    #todo: make pydantic model
    ''' Add a user competency to database. Note this includes a user_id, so we end up
     with a 1:many relationship. This should fail if an unknown user_id is passed, and if the various
      indices for the values are out of bounds or if this competency is already applied
      to specified user. '''
    _competency = DB_Competency(user_id=competency.user_id,quadrant=competency.quadrant, sector=competency.sector, rating=competency.rating)
    result = handlers.add_competency(engine,_competency)
    return result

# TODO: This needs to use the loaded data, not the python mappr
@router.get("/{quadrant}/{sector}/")
async def get_competency(quadrant:int, sector:int):
    '''return a competency description by index '''
    try:
        return {
            "quadrant":{
                "id":quadrant,
                "value":get_sector_title_from_data(compass_config_data["configuration"]["data_quadrant_titles"][quadrant]["title_parts"]),
            },
            "sector":{
                "id":sector,
                "value":get_sector_title_from_data(compass_config_data["configuration"]["data_quadrant_titles"][quadrant]["sector_parts"][sector]),
            }
        }
    except IndexError as ex:
        # TODO: construct more informative return values
        return {
            "error":f"out of range got quadrant:{quadrant}, sector:{sector}. IndexError Exception was {ex}."
        }
    except KeyError as ex:
        # TODO: construct more informative return values
        return {
            "error":f"No match for competency at quadrant:{quadrant}, sector:{sector}. KeyError Exception was {ex}. "
        }
    except Exception as ex:
        return {
            "error":f"An unexpected error occurred: {ex}"
        }
