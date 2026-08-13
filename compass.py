import logging
import re
import datetime
import json
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse, RedirectResponse, PlainTextResponse

# see https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import uvicorn

# https://fastapi.tiangolo.com/advanced/templates/
from fastapi.templating import Jinja2Templates

from utilities.download_utilities import get_sector_title_from_data
from utilities.data_utilities import load_config_data 
from utilities.template_utils import Funcs

from routers import competency_router, ratings_router, user_router, \
    settings_router,compass_data_router  #,api_router

from api.models import User,  UserCompetencies
from api.database import handlers
from api.database.engine import get_engine
from api.db_models import  Base

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError, ResponseValidationError

# https://github.com/fastapi/fastapi/discussions/12254
# This doesn't quite feel right...
engine = get_engine()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# from https://fastapi.tiangolo.com/advanced/events/#lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code
    logger.info(f"startup event")# why does this only run on browser refresh? 
    #I think it is because the app is not actually started until the first request is made. 
    # #Therefore, the startup event is not actually run until the first request is made. 
    # #This is a bit of a problem, because we want to load the config data into memory at startup,
    # # so that it is available for all requests. Therefore, we need to find a way to run the 
    # #startup event before the first request is made. I think this can be done by using a 
    # #middleware that runs before the first request is made. I will investigate this further.
    yield
    # shutdown code
    logger.info(f"shutdown event")

# NOTE: I can add arbitrary properties to `app`, but making an application-wide
# global (app.state) may be an option.
# See https://starlette.dev/applications/#accessing-the-app-instance
app = FastAPI(
    lifespan=lifespan, 
    title="Compass Application", 
    description="A web application for managing user competencies and compass data.", 
    version="0.5.0")    # it's still beta.

# exception handlers for app:
# see https://fastapi.tiangolo.com/tutorial/handling-errors/#override-request-validation-exceptions
# TODO: move to module?

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request,exc:RequestValidationError):
    logger.error(request)
    logger.error(f"RequestValidationError occurred: {exc}")
    # https://fastapi.tiangolo.com/tutorial/handling-errors/#override-request-validation-exceptions
    # https://stackoverflow.com/questions/62986778/fastapi-handling-and-redirecting-404
    # return RedirectResponse("/static/404.html")
    ## FFS! This has been working all along!
    '''
    
    '''


    x = f"{{\"message\":\"{str(exc)}\"}}"

    # extract the message manually from the exc object:
    _msg = exc.args[0][0]["msg"]

    # _json = x.replace("'",'"')
    # _jsonobject = json.loads(_json)
    # _jsonstring = json.dumps(_jsonobject)
    # exc = json.loads(str(exc).replace("'",'"'))
    # ARSE! it looks like I need to build the response object myself because the JSON has single quotes...]
    # Hmmm... I think this might be a bug in FastAPI - i'm getting 'json' with single quotes for fieldnames.
    # This may be wy the example in the fasapi docs is using a PlainTextResponse...
    return JSONResponse({
        "status_code": 422,
        "error":"RequestValidationError",
        # "message": str(exc),
        "message": _msg
    })
    return PlainTextResponse(f"{{\"message\":\"{str(exc)}\"}}", status_code=422)

@app.exception_handler(ResponseValidationError)
async def handle_response_validation_error(request,exc:ResponseValidationError):
    logger.error(f"ResponseValidationError occurred: {exc}")
    # As advised by Copilot code review, we should return a JSON response with the error message and a 500 status code. This will help in debugging and provide
    # a clear indication of what went wrong. 
    return JSONResponse({"error":"ResponseValidationError occurred","message": str(exc)}, status_code=500)
    # return RedirectResponse("/static/404.html") # could pass error here to a template and display the error?


app.include_router(user_router.router)
app.include_router(settings_router.router)
app.include_router(competency_router.router)
app.include_router(ratings_router.router)
app.include_router(compass_data_router.router)
# lets separate the API routes from the template routes, so we can mount the API at /api/ and the templates at /
# There's only one...
# app.include_router(api_router.router)

# compass_config_data = load_config_data(engine=engine, caller="root")
app.mount("/static", StaticFiles(directory="static", html=True, ),name="static")

# declare location of template(s)
templates = Jinja2Templates(directory="templates")

# and generate the SQL:
Base.metadata.create_all(engine)

'''
Templated routes for the compass application
'''
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request,name="home.html", context={}
    )


@app.get("/{user_id}")
async def compass_for_user(request: Request,user_id:int):
    _user = handlers.get_user(engine, user_id)
    _compass = handlers.get_compass(engine, _user.compass_id)
    # If we get here with _compass == {}, then there is currently no compass applied to the user. We need to handle this at the template...
    return templates.TemplateResponse(
        request=request,name="index.html", context={"user":_user, "compass":_compass}
    )


@app.get("/{user_id}/edit/")
async def update_user(request: Request,user_id:int) -> User:
    ''' update user's competencies in database '''
    _user = handlers.get_user(engine, user_id)  # get current state of user
    _compasses = handlers.get_all_compasses(engine)
    return templates.TemplateResponse(
        request=request,name="user_edit.html", context={"user":_user,"compasses":_compasses}
    )


@app.get("/configure/components")
async def compass_summaries(request: Request):
    quadrants = handlers.get_quadrants(engine=engine)
    quadrant_titles = handlers.get_quadrant_titles(engine=engine)
    sectors = handlers.get_sectors(engine=engine)
    sector_titles = handlers.get_sector_titles(engine=engine)
    ratings = handlers.get_ratings(engine=engine)
    return templates.TemplateResponse(
        request=request,
        name="compass_components.html",
        context={
            "quadrants":quadrants,
            "quadrant_titles":quadrant_titles,
            "sectors":sectors, 
            "sector_titles":sector_titles,
            "ratings":ratings,
            "funcs":Funcs,
        }
    )


@app.get("/configure/new")
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
        logger.error(f"IndexError: {ex}")
    except Exception as ex:
        logger.error(f"configure/new  Exception: {ex}")


@app.get("/configure/{compass_id}")
async def configure(request: Request, compass_id: int):

    # retrieve data we need
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
        logger.error(f"IndexError: {ex}")
    except Exception as ex:
        logger.error(f"Exception: {ex}")


# jumpoff page to select or create a compass definition
# so here, we need to pass in the compass list only
@app.get("/configure/")
async def compass_summaries(request: Request):
    # retrieve data we need

    compass_summaries = handlers.get_all_compasses(engine=engine) # to sort. we can't have hardcoded IDs floating about...
    return templates.TemplateResponse(
        request=request,
        name="configure_home.html",
        context={"compass_summaries":compass_summaries}
    )


# do I leave these here? [from Copilot]: I think so, as they are the API endpoints for the user data download. They are not part of the
# template routes, but they are part of the API routes. So I will leave them here for now. Nice Interaction BTW.
@app.get("/{user_id}/data/csv",response_class=StreamingResponse)
async def download_user_data_csv(user_id:int):   # -> UserCompetencies:
    user_data = handlers.get_user_data(engine, user_id)

    # This is needed so we can determine the compass title for the user,
    # and also the sector titles. We need to pass in the compass ID to
    # get the correct config data for this user.
    compass_data = handlers.get_compass(engine, user_data.user.compass_id)
    
    # CONFIG DATA is not being used consistently. It IS needed, but here it is erroneously loaded with
    # incorrect compass ID. Therefore, pass current user compass ID to the settings_router.get_json_config_as_dict() 
    # function to get the correct config data for this user.
    # (note that this is a legacy of the old code, which was loading the config data with a hardcoded compass ID of 1. 
    #  This is not correct, as it will not work for users with different compass IDs.)
    config_data = settings_router.get_json_config_as_dict(compass_id=user_data.user.compass_id)
    csv_data = ""
    header = ",".join(['Compass','Quadrant','Sector','Rating',"Description"])
    header = header+"\n"
    csv_data = header
    
    for comp in user_data.competencies:
        _test = get_sector_title_from_data(config_data["configuration"].data_quadrants[comp.quadrant].title)
        row = ",".join([
            compass_data.title,
            _test,
            # https://stackoverflow.com/questions/47187792/writing-csv-with-quotes-around-strings-python
            get_sector_title_from_data(config_data["configuration"].data_quadrants[comp.quadrant].sectors[comp.sector].title),
            config_data["configuration"].rating_description_lookup[comp.rating].title,
            # remove control chars (TODO: quote the fields - probably use the CSV module...)
            # # see: https://www.geeksforgeeks.org/python/python-program-to-remove-all-control-characters/
            re.sub(r'[\x00-\x1f]', '', config_data["configuration"].rating_description_lookup[comp.rating].description)
        ])
        csv_data = csv_data+row+"\n"
    response = StreamingResponse(csv_data)
    try:
        _dtformat = "%Y-%m-%d_%H-%M-%S"
        _cd = f"attachment; filename={user_data.user.username}_{datetime.datetime.now().strftime(_dtformat)}.csv"
        response.headers["Content-Disposition"] = _cd
        return response
    except Exception as ex:
        logger.error(f"Exception in download_user_data_csv: {ex}")
        return JSONResponse({"error":"Exception in download_user_data_csv","message": str(ex)}, status_code=500)


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
