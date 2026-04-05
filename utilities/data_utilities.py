from enum import Enum
import json

from sqlalchemy.orm import Session

# from .database.handlers import get_compass
from api.database.handlers import get_compass
from api.database.engine import get_engine
from sqlalchemy.orm import Session

import api.database.handlers as handlers
from api.models import Competency, CompassData  # adde usercompetencies model
from api.db_models import DB_Competency

# enum for data source
class DataSource(Enum):
    FILESYSTEM = 1
    DATABASE = 2

# engine = get_engine()

compass_config_data = {"status":"unset", "configuration":{}}

# TODO: This needs to account for multiple compass IDs
def load_config_data(source:DataSource=DataSource['DATABASE'], engine=None, caller=None,compass_id=None):
    # print(f"IN load_config_data(), called by {caller}:")
    # print(engine)
    # print(source)
    
    # THIS CAN GO...
    if source == DataSource.FILESYSTEM:
        # This is the container filesystem path:
        with open(mode="r",file="/code/static/data/display_data_rationalised.json") as display_data:
            compass_config_data["configuration"] = json.load(display_data)
            compass_config_data["status"] = "set"

    if source == DataSource.DATABASE:
        with Session(engine) as session:
            try:
                # TO SORT:
                if compass_id:
                    compass_config_data["configuration"] = handlers.get_compass(engine,compass_id)
                else:
                    compass_config_data["configuration"] = handlers.get_compass(engine,2)
                compass_config_data["status"] = "set"
                # # print("DATABASE DRIVEN COMPASS DATA")
                # # _test = session.query(DB_Competency).all()
                # # print(_test)
                # print("set")

            except Exception as ex:
                print(f"error: {ex}")

    return compass_config_data