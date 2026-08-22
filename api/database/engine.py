import logging
import os

from sqlalchemy import event, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

# set up module logging:
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# refer to enrty in compose file:
DATABASE_URI = os.getenv("COMPASS_DATABASE_URL")
# see e.g. https://medium.com/flowe-ita/logging-should-be-lazy-bc6ac9816906 for lazy evaluation syntax:
logger.info("=======================================")
logger.info("Using database URI '%s'",DATABASE_URI)
logger.info("=======================================")

engine = create_engine(DATABASE_URI, echo=False)  
# Note: set echo=True for debugging, future=True for SQLAlchemy 2.0 style
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Enforce FK checking at runtime:
# see https://www.lesinskis.com/enforcing-foreign-key-constraints-with-sqlite.html,
# https://stackoverflow.com/questions/2614984/sqlite-sqlalchemy-how-to-enforce-foreign-keys
# and https://pythonfriday.dev/2024/06/232-update-sqlalchemy-to-version-2-x/
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    logger.info("Setting SQLite PRAGMA foreign_keys=ON")
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# https://fastapitutorial.com/blog/dependencies-in-fastapi-coursefor-book/
def get_engine():
    logger.info("get_engine() called, returning engine '%s'",engine)
    return engine
