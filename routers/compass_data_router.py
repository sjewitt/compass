import logging

from fastapi import APIRouter, Response, status

from api.models import Quadrant, QuadrantIn, QuadrantBase, QuadrantTitles, \
        QuadrantTitlesIn, Sector, SectorIn, SectorEdit, \
        SectorTitles,SectorTitlesIn,CompassData, CompassDefinition, CompassDefinitionIn, CompassSummary, \
        Rating, RatingIn, APIResponseMessage
from api.exceptions import CompassForUserNotFound, CompassDefinitionIncomplete
from api.database.engine import get_engine
from api.database import handlers

router = APIRouter(
    prefix="/compass",
    tags=["CompassData"],
)

engine = get_engine()


################
# COMPASSES
################
@router.get("/", response_model=list[CompassSummary])
def get_data() -> list[CompassSummary]:
    ''' Retrieve summary data for all compass models defined, return ID and title only  '''
    try:
        result = handlers.get_all_compasses(engine)
        return result
    except Exception as ex:
        print(ex)

 
@router.get("/{id}", response_model=CompassData|APIResponseMessage)
def get_data(id:int, response: Response) -> CompassData:
    ''' retrieve the definition by ID and compose the actual data in the handler '''
    try:
        result = handlers.get_compass(engine,id)
        if not result:
            raise CompassForUserNotFound(status_code=404)   # the API page exists, but no data is returned. see https://stackoverflow.com/questions/9595151 

        return result
    except CompassForUserNotFound as ex:
        # see https://fastapi.tiangolo.com/advanced/response-change-status-code/#use-case
        # and https://fastapi.tiangolo.com/reference/status/#fastapi.status.HTTP_301_MOVED_PERMANENTLY
        response.status_code=status.HTTP_404_NOT_FOUND
        return APIResponseMessage(message=f"Compass with id '{id}' not found", success=False, source="get_data", data={}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return APIResponseMessage(message=f"Error occurred while fetching compass with id '{id}'", success=False, source="get_data", data={})


@router.post("/")
def set_data(definition:CompassDefinitionIn, response:Response) -> CompassSummary|APIResponseMessage:
    try:
        result = handlers.set_compass(engine,definition)
        if result == -1:
            logging.error( Exception(f"Compass name {definition.name} already exists. Cannot add new compass definition."))
            raise CompassDefinitionIncomplete(status_code=status.HTTP_400_BAD_REQUEST)

        return CompassSummary(id=result,name=definition.name)
    except CompassDefinitionIncomplete as ex:
        if result == -1:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return APIResponseMessage(message=f"Duplicate Compass name ({definition.name}). Try another name.", success=False, source="set_data",data={}, status_code = status.HTTP_400_BAD_REQUEST)
        return APIResponseMessage(message=f"something went wrong with the definition!", success=False, source="set_data",data={})
    except Exception as ex:
        return APIResponseMessage(message=f"something went really wrong! (exception was {ex})", success=False, source="set_data",data={})


@router.post("/update/")
def update_data(definition:CompassDefinition) -> CompassSummary: # TODO: Update this object with a status
    result = handlers.update_compass(engine, definition)
    return CompassSummary(id=result,name=definition.name)

################
# QUADRANTS
################
@router.post("/quadrant/")
def add_quadrant(quadrant:QuadrantIn):
    result = handlers.add_quadrant(engine,quadrant)
    return result

@router.post("/quadrant/update/")
def update_quadrant(quadrant:QuadrantBase):
    result = handlers.update_quadrant(engine,quadrant)
    return result


@router.get("/quadrants/")
def get_quadrants()->list[Quadrant]:
    result = handlers.get_quadrants(engine)
    return result


@router.post("/quadrants/title/")
def add_quadrant_title(quadrant_title:QuadrantTitlesIn) -> QuadrantTitles:
    result = handlers.add_quadrant_title(engine,quadrant_title)
    return result


@router.post("/quadrants/title/update/")
def update_quadrant_title(quadrant_title:QuadrantTitles) -> QuadrantTitles:
    result = handlers.update_quadrant_title(engine,quadrant_title)
    return result


@router.get("/quadrants/titles/")
def get_quadrant_titles() -> list[QuadrantTitles]:
    result = handlers.get_quadrant_titles(engine)
    return result


@router.get("/quadrants/{id}/", response_model=QuadrantBase)
def get_quadrant(id:int)->QuadrantBase:
    result = handlers.get_quadrant(engine,id)
    return result


################################################
# SECTOR TITLES
################################################
@router.get("/sectors/titles/")
def get_sector_titles() -> list[SectorTitles]:
    result = handlers.get_sector_titles(engine)
    return result


@router.get("/sectors/titles/{id}")
def get_sector_title(id:int) -> SectorTitles:
    result = handlers.get_sector_title(engine, id)
    return result


@router.post("/sectors/title/update")
def update_sector_title(updated_sector_title:SectorTitles) -> SectorTitles:
    result = handlers.update_sector_title(engine, updated_sector_title)
    return result


@router.post("/sectors/title/")
def add_sector_title(sectortitle:SectorTitlesIn) -> bool:
    result = handlers.add_sector_title(engine,sectortitle)
    return result


################################################
# SECTORS 
################
@router.post("/sectors/")
def add_sector(sector:SectorIn):
    return handlers.add_sector(engine,sector)


# TODO: The model should not have the empty array any more.
# See https://github.com/sjewitt/compass/issues/178
@router.post("/sectors/update/")
def update_sector(sector:SectorEdit):
    return handlers.update_sector(engine,sector)


@router.get("/sectors/")
def get_sectors()->list[Sector]:
    return handlers.get_sectors(engine)


@router.get("/sectors/{id}/")
def get_sector(id:int)->Sector:
    return handlers.get_sector(engine, id)


################
# RATINGS TODO: add response models!
################
@router.post("/rating/")
def add_rating(rating:RatingIn):
    return handlers.add_rating(engine, rating)


@router.post("/rating/update")
def update_rating(rating:Rating):
    return handlers.update_rating(engine, rating)


@router.get("/ratings/", response_model=list[Rating])
def get_ratings()->list[Rating]:
    return handlers.get_ratings(engine)


@router.get("/ratings/{id}", response_model=Rating)
def get_ratings(id:int)->Rating:
    return handlers.get_rating(engine, id)
