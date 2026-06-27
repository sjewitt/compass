import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# declare SQLite DB for persistent storage:
# DATABASE_URI = "sqlite:///./database/db.sqlite"
# DATABASE_URI = "sqlite:///./database/test.sqlite"
# DATABASE_URI = "sqlite:///./database/test2.sqlite"
# DATABASE_URI = "sqlite:///./database/test3.sqlite"    # CURRENT SCHEMA
# DATABASE_URI = "sqlite:///./database/test4.sqlite"
# DATABASE_URI = "sqlite:///./database/test5.sqlite" # EMPTY
# DATABASE_URI = "sqlite:///./database/test6.sqlite"  # schema v0.2 
DATABASE_URI = "sqlite:///./database/test7.sqlite"  # schema v0.3 (competenies with compass ID) 
engine = create_engine(DATABASE_URI, echo=False)  
# echo=True for debugging, future=True for SQLAlchemy 2.0 style
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# https://fastapitutorial.com/blog/dependencies-in-fastapi-coursefor-book/
def get_engine():
    logging.info(f"get_engine() called, returning engine: {engine}")
    return engine



