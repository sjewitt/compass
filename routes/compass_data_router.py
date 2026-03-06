from fastapi import APIRouter

from api.models import Quadrant, QuadrantTitles,Sector, \
        SectorTitles,CompassData, CompassDefinition, CompassSummary
from api.db_models import DB_Quadrant, DB_QuadrantTitles,\
        DB_Sector,DB_SectorTitles
from api.database.engine import get_engine
from api.database import handlers

router = APIRouter(
    prefix="/compass",
    tags=["CompassData"],
)

engine = get_engine()

@router.get("/", response_model=list[CompassSummary])
def get_data() -> list[CompassSummary]:
    ''' Retrieve summary data for all compass models defined, return ID and title only  '''
    result = handlers.get_all_compasses(engine)
    return result

@router.get("/{id}", response_model=CompassData)
def get_data(id) -> CompassData:
    ''' retrieve the definition by ID and compose the actual data in the handler '''
    result = handlers.get_compass(engine,id)
    return result

@router.post("/")
def set_data(definition:CompassDefinition) -> CompassSummary:
    print(definition)
    result = handlers.set_compass(engine,definition)
    # print(result)
    return CompassSummary(id=result,name=definition.name)
    # return {}


# @router.post("/")
# def set_data(compass_data:CompassData):
#     pass

@router.post("/quadrant/")
def add_quadrant(quadrant:Quadrant):
    # breakpoint()
    print("IN ADD QUAD:")
    print(quadrant)
    # _titles = [QuadrantTitles]
    # for _title in quadrant.title:
    #     _titles.append(DB_QuadrantTitles(_title["title_part"]))
    # _quad = DB_Quadrant(
    #     quadrant_summary = quadrant.quadrant_summary,
    #     quadrant_css_class = quadrant.quadrant_css_class,
    #     quadrant_elem_coords = quadrant.quadrant_elem_coords,
    #     children = _titles
    # )
    print("CALLING HANDLER:")
    result = handlers.add_quadrant(engine,quadrant)
    print("ADD QUAD RESULT:")
    print(result)
    pass

@router.get("/quadrants/")
def get_quadrants()->list[Quadrant]:
    print("CALLING HANDLERS:")
    result = handlers.get_quadrants(engine)
    print(result)
    return result

@router.get("/quadrants/{id}/", response_model=Quadrant)
def get_quadrant(id:int)->Quadrant:
    result = handlers.get_quadrant(engine,id)
    return result

# test:
@router.get("/quadranttitles/")
def get_quadrant_titles() -> list[QuadrantTitles]:
    result = handlers.get_quadrant_titles(engine)
    print(result)
    return result


@router.post("/sectors/")
def add_sector(sector:Sector):
    result = handlers.add_sector(engine,sector)
    return result

@router.get("/sectors/")
def get_sectors()->list[Sector]:
    result = handlers.get_sectors(engine)
    return result

@router.get("/sectors/{id}/")
def get_sector(id:int)->Sector:
    result = handlers.get_sector(engine, id)
    return result


