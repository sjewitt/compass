import logging
import os

from sqlalchemy import event, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

# declare SQLite DB for persistent storage:
# DATABASE_URI = "sqlite:///./database/db.sqlite"
# DATABASE_URI = "sqlite:///./database/test.sqlite"
# DATABASE_URI = "sqlite:///./database/test2.sqlite"
# DATABASE_URI = "sqlite:///./database/test3.sqlite"    # CURRENT SCHEMA
# DATABASE_URI = "sqlite:///./database/test4.sqlite"
# DATABASE_URI = "sqlite:///./database/test5.sqlite" # EMPTY
# DATABASE_URI = "sqlite:///./database/test6.sqlite"  # schema v0.2 
# DATABASE_URI = "sqlite:///./database/test7.sqlite"  # schema v0.3 (competenies with compass ID) 
# DATABASE_URI = "sqlite:///./database/test8.sqlite"  # schema v0.3 (competenies with compass ID)
# DATABASE_URI = "sqlite:///./database/test11.sqlite"  # schema v0.3 test 

# test retrieval via .env:

# refer to enrty in compose file:
DATABASE_URI = os.getenv("COMPASS_DATABASE_URL")
logging.info("=======================================")
logging.info(DATABASE_URI)
logging.info("=======================================")

engine = create_engine(DATABASE_URI, echo=False)  
# echo=True for debugging, future=True for SQLAlchemy 2.0 style
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# test of https://www.lesinskis.com/enforcing-foreign-key-constraints-with-sqlite.html
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    print("Setting SQLite PRAGMA foreign_keys=ON")
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# https://fastapitutorial.com/blog/dependencies-in-fastapi-coursefor-book/
def get_engine():
    logging.info(f"get_engine() called, returning engine: {engine}")
    # switch on foreign key enforcement:
    # https://stackoverflow.com/questions/2614984/sqlite-sqlalchemy-how-to-enforce-foreign-keys
    # conn = engine.connect()
    # # and see https://pythonfriday.dev/2024/06/232-update-sqlalchemy-to-version-2-x/
    # conn.execute(text("PRAGMA foreign_keys=ON"))
    return engine



