from fastapi import APIRouter

from api.models import Quadrant, QuadrantTitles, Sector, \
        SectorTitles,CompassData, CompassDefinition, CompassSummary, \
        Rating, RatingIn
# from api.db_models import DB_Quadrant, DB_QuadrantTitles,\
#         DB_Sector,DB_SectorTitles, DB_Rating
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

#################
# This is the initial entrypoint.
# Currently, {id} is hardcoded to 2 in the javascript,
# so I need to allow a compass ID to be passed from the currently
# logged-in/selected user. TODO: 
@router.get("/{id}", response_model=CompassData)
def get_data(id:int) -> CompassData:
    ''' retrieve the definition by ID and compose the actual data in the handler '''
    try:
        result = handlers.get_compass(engine,id)
        return result
    except Exception as ex:
        print(ex)

@router.post("/")
def set_data(definition:CompassDefinition) -> CompassSummary:
    result = handlers.set_compass(engine,definition)
    return CompassSummary(id=result,name=definition.name)


################
# QUADRANTS
################
@router.post("/quadrant/")
def add_quadrant(quadrant:Quadrant):
    result = handlers.add_quadrant(engine,quadrant)
    return result

# retrieve quads, including assigned titles
@router.get("/quadrants/")
def get_quadrants()->list[Quadrant]:
    result = handlers.get_quadrants(engine)
    return result

# retrieve quads, without  assigned titles
@router.get("/quadrants/no_titles/")
def get_quadrants()->list[Quadrant]:
    result = handlers.get_quadrants(engine,include_titles=False)
    return result


# retrieve all quadrant titles (as list, not assigned (rename this endpoint?))
@router.get("/quadrants/titles/")
def get_quadrant_titles() -> list[QuadrantTitles]:
    result = handlers.get_quadrant_titles(engine)
    return result

@router.get("/quadrants/{id}/", response_model=Quadrant)
def get_quadrant(id:int)->Quadrant:
    result = handlers.get_quadrant(engine,id)
    return result



################
# SECTORS
################
@router.post("/sectors/")
def add_sector(sector:Sector):
    result = handlers.add_sector(engine,sector)
    return result

@router.get("/sectors/")
def get_sectors()->list[Sector]:
    result = handlers.get_sectors(engine)
    return result

@router.get("/sectors/titles/")
def get_sector_titles() -> list[SectorTitles]:
    result = handlers.get_sector_titles(engine)
    return result

@router.get("/sectors/{id}/")
def get_sector(id:int)->Sector:
    result = handlers.get_sector(engine, id)
    return result



################
# RATINGS
################
@router.post("/rating/")
def add_rating(rating:RatingIn):
    result = handlers.add_rating(engine, rating)
    return result

@router.get("/ratings/", response_model=list[Rating])
def get_ratings()->list[Rating]:
    result = handlers.get_ratings(engine)
    return result

@router.get("/ratings/{id}", response_model=Rating)
def get_ratings(id:int)->Rating:
    result = handlers.get_rating(engine, id)
    return result