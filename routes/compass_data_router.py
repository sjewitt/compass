from fastapi import APIRouter

from api.models import Quadrant, QuadrantIn, QuadrantBase, QuadrantTitles, \
        QuadrantTitlesIn, Sector, SectorIn, \
        SectorTitles,SectorTitlesIn,CompassData, CompassDefinition, CompassDefinitionIn, CompassSummary, \
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
@router.get("/{id}", response_model=CompassData|None)
def get_data(id:int) -> CompassData:
    ''' retrieve the definition by ID and compose the actual data in the handler '''
    try:
        result = handlers.get_compass(engine,id)
        return result
    except Exception as ex:
        print(ex)
        # return handlers.get_compass(engine,0)   # return a dummy to prevent errors (TO FIX PROPERLY!)
        return None

@router.post("/")
def set_data(definition:CompassDefinitionIn) -> CompassSummary:
    result = handlers.set_compass(engine,definition)
    return CompassSummary(id=result,name=definition.name)

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
    ''' 
    ** Update a quadrant\n
     The sector array can be empty (API will be updated to not require this at all at some point - models are in flux...)
    '''
    result = handlers.update_quadrant(engine,quadrant)
    return result

# retrieve quads, without  assigned titles
@router.get("/quadrants/")
def get_quadrants()->list[Quadrant]:
    ''' get all quadrants defined in the database '''
    result = handlers.get_quadrants(engine)
    return result

# # retrieve quads, without  assigned titles
# @router.get("/quadrants/no_titles/")
# def get_quadrants()->list[Quadrant]:
#     result = handlers.get_quadrants(engine,include_titles=False)
#     return result


# retrieve all quadrant titles (as list, not assigned (rename this endpoint?))

@router.post("/quadrants/title/")
def add_quadrant_title(quadrant_title:QuadrantTitlesIn) -> QuadrantTitles:
    ''' get all quadrant titles in the database '''
    result = handlers.add_quadrant_title(engine,quadrant_title)
    return result

@router.post("/quadrants/title/update/")
def update_quadrant_title(quadrant_title:QuadrantTitles) -> QuadrantTitles:
    ''' get all quadrant titles in the database '''
    result = handlers.update_quadrant_title(engine,quadrant_title)
    return result


@router.get("/quadrants/titles/")
def get_quadrant_titles() -> list[QuadrantTitles]:
    ''' get all quadrant titles in the database '''
    result = handlers.get_quadrant_titles(engine)
    return result

@router.get("/quadrants/{id}/", response_model=QuadrantBase)
def get_quadrant(id:int)->QuadrantBase:
    result = handlers.get_quadrant(engine,id)
    return result

################################################
# SECTOR TITLES
# (method order is important here!)
################################################
@router.get("/sectors/titles/")
def get_sector_titles() -> list[SectorTitles]:
    ''' get all sector titles defined in the database '''
    result = handlers.get_sector_titles(engine)
    return result

@router.get("/sectors/titles/{id}")
def get_sector_title(id:int) -> SectorTitles:
    ''' 
    ## get specified sector title defined in the database 
    '''
    result = handlers.get_sector_title(engine, id)
    return result

@router.post("/sectors/titles/update")
def update_sector_title(updated_sector_title:SectorTitles) -> SectorTitles:
    ''' ## get specified sector title defined in the database '''
    result = handlers.update_sector_title(engine, updated_sector_title)
    return result

@router.post("/sectors/titles/")
def add_sector_titles(sectortitles:list[SectorTitlesIn]) -> bool:
    '''
      ## Add one or more sector title\n 
      Expects a list of SectorTitles
    '''
    result = handlers.add_sector_titles(engine,sectortitles)
    return result

################################################
# SECTORS
################
@router.post("/sectors/")
def add_sector(sector:SectorIn):
    result = handlers.add_sector(engine,sector)
    return result

@router.get("/sectors/")
def get_sectors()->list[Sector]:
    ''' get all sectors defined in the database '''
    result = handlers.get_sectors(engine)
    return result


@router.get("/sectors/{id}/")
def get_sector(id:int)->Sector:
    ''' get a sector by database ID '''
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