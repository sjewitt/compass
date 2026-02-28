from fastapi import APIRouter

from api.models import Quadrant,QuadrantTitles,Sector,SectorTitles
from api.db_models import DB_Quadrant, DB_QuadrantTitles,DB_Sector,DB_SectorTitles
from api.database.engine import get_engine
from api.database import handlers

router = APIRouter(
    prefix="/compass",
    tags=["CompassData"],
)

engine = get_engine()

@router.post("/quadrants/")
def add_quadrant(engine, quadrant:Quadrant):
    breakpoint()
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
    result = handlers.add_quadrant(engine,quadrant)
    print(result)
    pass

@router.get("/quadrants/")
def get_quadrants()->list[Quadrant]:
    pass

@router.get("/quadrants/{id}/")
def get_quadrant(id:int)->Quadrant:
    pass

@router.get("/sectors/")
def get_sectors()->list[Sector]:
    pass

@router.get("/sectors/{id}/")
def get_sector(id:int)->Sector:
    pass

@router.post("/sectors/")
def add_sector(sector:Sector):
    pass
