from fastapi import APIRouter

from api.database.engine import get_engine
from utilities.data_utilities import load_config_data

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"],
)

engine = get_engine()
# This needs to change to call with a compass ID as well
# TODO:
# compass_config_data = load_config_data(engine=engine, caller="ratings")


# @router.get("/")
# async def get_ratings():
#     '''return all rating descriptions 
#     THIS NEEDS SORTING AS THE RATINGS ARE NOW INDEPENDENT!
#     Use a handler that calls teh DB. This may have unforseen consequences...
#     '''
#     return False

# @router.get("/{rating_idx}/")
# async def get_rating(rating_idx:int):
#     '''return a competency description by index 
#     THIS NEEDS SORTING AS THE RATINGS ARE NOW INDEPENDENT!
#     '''
#     try:
#         return {
#             "rating":{
#                 "idx":rating_idx,
#                 # "value":compass_config_data["configuration"]["rating_description_lookup"][rating_id],
#                 "value":compass_config_data["configuration"].rating_description_lookup[rating_idx],
#             },
#         }
#     except IndexError as ex:
#         # TODO: construct more informative return values
#         return {
#             "error":f"rating out of range. {ex}"
#         }
    
#     except Exception as ex:
#         return {
#             "error":f"An unexpected error occurred: {ex}"
#         }

# # TODO: only used by API so far
# @router.get("/{compass_id}/{rating_idx}/")
# async def get_rating_by_compass(compass_id:int, rating_idx:int):
#     '''return a competency description by index 
#     THIS NEEDS SORTING AS THE RATINGS ARE NOW INDEPENDENT!
#     '''
#     try:
#         return {
#             "rating":{
#                 "idx":rating_idx,
#                 # "value":compass_config_data["configuration"]["rating_description_lookup"][rating_id],
#                 "value":compass_config_data["configuration"].rating_description_lookup[rating_idx],
#             },
#         }
#     except IndexError as ex:
#         # TODO: construct more informative return values
#         return {
#             "error":f"rating out of range. {ex}"
#         }
    
#     except Exception as ex:
#         return {
#             "error":f"An unexpected error occurred: {ex}"
#         }