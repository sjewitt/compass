from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# declare SQLite DB for persistent storage:
# DATABASE_URI = "sqlite:///./database/db.sqlite"
# DATABASE_URI = "sqlite:///./database/test.sqlite"
# DATABASE_URI = "sqlite:///./database/test2.sqlite"
# DATABASE_URI = "sqlite:///./database/test3.sqlite"    # CURRENT SCHEMA
# DATABASE_URI = "sqlite:///./database/test4.sqlite"
# DATABASE_URI = "sqlite:///./database/test5.sqlite" # EMPTY
DATABASE_URI = "sqlite:///./database/test6.sqlite"  # schema v2 
engine = create_engine(DATABASE_URI, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# https://fastapitutorial.com/blog/dependencies-in-fastapi-coursefor-book/
def get_engine():
    return engine



