import re
import datetime
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse, RedirectResponse

# see https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import uvicorn

# https://fastapi.tiangolo.com/advanced/templates/
from fastapi.templating import Jinja2Templates

from utilities.download_utilities import get_sector_title_from_data
from utilities.data_utilities import load_config_data 
from api.models import User,  UserCompetencies
from api.database import handlers
from api.database.engine import get_engine
from api.db_models import  Base

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError, ResponseValidationError

# # https://fastapitutorial.com/blog/dependencies-in-fastapi-coursefor-book/
# https://github.com/fastapi/fastapi/discussions/12254

# This doesn't quite feel right...
engine = get_engine()

app = FastAPI()

# exception handlers for app:
# see https://fastapi.tiangolo.com/tutorial/handling-errors/#override-request-validation-exceptions
# TODO: move to module?

@app.exception_handler(RequestValidationError)
async def test(request,exc:RequestValidationError):
    print(f"RequestValidationError occurred: {exc}")
    # https://stackoverflow.com/questions/62986778/fastapi-handling-and-redirecting-404
    return RedirectResponse("/static/404.html")

@app.exception_handler(ResponseValidationError)
async def test(request,exc:ResponseValidationError):
    print(f"ResponseValidationError occurred: {exc}")
    return "BROKEN" 

from routes import competency_router, ratings_router, user_router, settings_router,compass_data_router
app.include_router(user_router.router)
app.include_router(settings_router.router)
app.include_router(competency_router.router)
app.include_router(ratings_router.router)
app.include_router(compass_data_router.router)

compass_config_data = load_config_data(engine=engine, caller="root")
app.mount("/api/",app)
app.mount("/static", StaticFiles(directory="static", html=True, ),name="static")

# declare location of template(s)
templates = Jinja2Templates(directory="templates")

# and generate the SQL:
Base.metadata.create_all(engine)

# load JSON data on startup:
# load_config_data()

# test of jinja template function calling:
# To move to imported lib
class Funcs():
    
    def replace_empty_string(str_in):
        if not str_in:
            return "[empty]"
        return str_in


@app.get("/")
async def root(request: Request):
    # return RedirectResponse("/static/")
    return templates.TemplateResponse(
        request=request,name="home.html", context={}
    )

# template test:
@app.get("/{user_id}")
async def template_test(request: Request,user_id:int):
    _user = handlers.get_user(engine, user_id)
    return templates.TemplateResponse(
        request=request,name="index.html", context={"user":_user}
    )

@app.get("/{user_id}/edit/")
async def update_user(request: Request,user_id:int) -> User:
    ''' update user's competencies in database '''
    _user = handlers.get_user(engine, user_id)  # get current state of user
    _compasses = handlers.get_all_compasses(engine)
    return templates.TemplateResponse(
        request=request,name="user_edit.html", context={"user":_user,"compasses":_compasses}
    )

# jumpoff page to select or create a compass definition
# so here, we need to pass in the compass list only
@app.get("/configure/")
async def compass_summaries(request: Request):
    # retrieve data we need

    compass_summaries = handlers.get_all_compasses(engine=engine) # to sort. we can't have hardcoded IDs floating about...
    return templates.TemplateResponse(
        request=request,
        name="compass_summaries.html",
        context={"compass_summaries":compass_summaries}
    )

@app.get("/configure/new/")
async def compass_new(request: Request):
    # retrieve data we need
    try:
        # compass_data = handlers.get_compass(engine=engine) # to sort. we can't have hardcoded IDs floating about...
        # I also need the current data for the various components so I can generate the dropdowns as well:
        quadrants = handlers.get_quadrants(engine=engine)
        quadrant_titles = handlers.get_quadrant_titles(engine=engine)
        sectors = handlers.get_sectors(engine=engine)
        sector_titles = handlers.get_sector_titles(engine=engine)
        ratings = handlers.get_ratings(engine=engine)
        return templates.TemplateResponse(
            request=request,
            name="configure.html",
            context={
                "compass_data":None,
                "quadrants":quadrants,
                "quadrant_titles":quadrant_titles,
                "sectors":sectors, 
                "sector_titles":sector_titles,
                "ratings":ratings,
                "funcs":Funcs,
            }
        )
    except IndexError as ex:
        print(f"IndexError: {ex}")
    except Exception as ex:
        print(f"configure/new  Exception: {ex}")

@app.get("/configure/{compass_id}/")
async def configure(request: Request, compass_id: int):

    # retrieve data we need
    print(compass_id)
    try:
        compass_data = handlers.get_compass(engine=engine,id=compass_id) # to sort. we can't have hardcoded IDs floating about...
        # I also need the current data for the various components so I can generate the dropdowns as well:
        quadrants = handlers.get_quadrants(engine=engine)
        quadrant_titles = handlers.get_quadrant_titles(engine=engine)
        sectors = handlers.get_sectors(engine=engine)
        sector_titles = handlers.get_sector_titles(engine=engine)
        ratings = handlers.get_ratings(engine=engine)
        return templates.TemplateResponse(
            request=request,
            name="configure.html",
            context={
                "compass_data":compass_data,
                "quadrants":quadrants,
                "quadrant_titles":quadrant_titles,
                "sectors":sectors, 
                "sector_titles":sector_titles,
                "ratings":ratings,
                "funcs":Funcs,
            }
        )
    except IndexError as ex:
        print(f"IndexError: {ex}")
    except Exception as ex:
        print(f"Exception: {ex}")


@app.get("/{user_id}/data")
async def get_user_data(user_id:int) -> UserCompetencies:
    user_data = handlers.get_user_data(engine, user_id)
    return user_data


@app.get("/{user_id}/data/csv",response_class=StreamingResponse)
async def download_user_data_csv(user_id:int):   # -> UserCompetencies:
    user_data = handlers.get_user_data(engine, user_id)
    config_data = settings_router.get_json_config_as_dict()     # this is needed!
    csv_data = ""
    header = ",".join(['Quadrant','Sector','Rating',"Description"])
    header = header+"\n"
    csv_data = header
    
    for comp in user_data.competencies:
        _test = get_sector_title_from_data(config_data["configuration"].data_quadrants[comp.quadrant].title)
        row = ",".join([
            # get_sector_title_from_data(config_data["configuration"]["data_quadrants"][comp.quadrant]["title_parts"]),
            # get_sector_title_from_data(config_data["configuration"].data_quadrants[comp.quadrant].title),
            _test,
            # see: https://www.geeksforgeeks.org/python/python-program-to-remove-all-control-characters/
            # https://stackoverflow.com/questions/47187792/writing-csv-with-quotes-around-strings-python
            # config_data["configuration"]["data_quadrants"][comp.quadrant]["sector_summaries"][comp.sector]["title"], 
            # config_data["configuration"]["rating_description_lookup"][comp.rating]["title"],
            get_sector_title_from_data(config_data["configuration"].data_quadrants[comp.quadrant].sectors[comp.sector].title), 
            config_data["configuration"].rating_description_lookup[comp.rating].title,
            # remove control chars (TODO: quote the fields - probably use the CSV module...)
            # re.sub(r'[\x00-\x1f]', '', config_data["configuration"]["rating_description_lookup"][comp.rating]["description"])
            re.sub(r'[\x00-\x1f]', '', config_data["configuration"].rating_description_lookup[comp.rating].description)
        ])
        csv_data = csv_data+row+"\n"
    response = StreamingResponse(csv_data)
    
    _cd = f"attachment; filename={user_data.user.username}_{datetime.datetime.now()}.csv"
    response.headers["Content-Disposition"] = _cd

    # TODO: use CSV lib to properly generate quoted data
    return response


@app.get("/{user_id}/data/json",response_class=FileResponse)
async def download_user_data_json(user_id:int):# -> UserCompetencies:
    user_data = handlers.get_user_data(engine, user_id)
    response = JSONResponse(user_data.model_dump())
    _cd = f"attachment; filename={user_data.user.username}_{datetime.datetime.now()}.json"
    response.headers["Content-Disposition"] = _cd
    return response
    # https://www.geeksforgeeks.org/python/stringio-and-bytesio-for-managing-data-as-file-object/
    # https://stackoverflow.com/questions/76047310/how-to-redirect-from-a-post-to-a-get-endpoint-in-fastapi-without-changing-the-re

# https://www.uvicorn.org/#command-line-options
if __name__ == "__main__":
    uvicorn.run("compass:app", host="0.0.0.0", port=8080, reload=True)
