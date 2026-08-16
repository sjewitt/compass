from enum import Enum
import json
import logging

from sqlalchemy.orm import Session

# from .database.handlers import get_compass
from api.database.handlers import get_compass
from api.database.engine import get_engine
from sqlalchemy.orm import Session

import api.database.handlers as handlers
from api.models import Competency, CompassData  # adde usercompetencies model
from api.db_models import DB_Competency
from api.exceptions import CompassNotFound

# enum for data source
class DataSource(Enum):
    FILESYSTEM = 1
    DATABASE = 2

# engine = get_engine()

compass_config_data = {"status":"unset", "configuration":{}}

# TODO: This needs to account for multiple compass IDs
def load_config_data(source:DataSource=DataSource['DATABASE'], engine=None, caller=None,compass_id=None):
    print(f"IN load_config_data(), called by {caller}:")

    with Session(engine) as session:
        try:
            if compass_id:
                compass_config_data["configuration"] = handlers.get_compass(engine,compass_id)
                compass_config_data["status"] = "set"
            else:
                raise IndexError()   # the API page exists, but no data is returned. see https://stackoverflow.com/questions/9595151

        except IndexError as ex:
            logging.warning(f"error: {ex}: Compass with id '{compass_id}' not found")
            compass_config_data["status"] = "unset"
            compass_config_data["configuration"] = {}

        except Exception as ex:
            print(f"error: {ex}: An exception ocurred")

    return compass_config_data