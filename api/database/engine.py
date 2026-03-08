from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# declare SQLite DB for persistent storage:
DATABASE_URI = "sqlite:///./database/db.sqlite"
engine = create_engine(DATABASE_URI, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# https://fastapitutorial.com/blog/dependencies-in-fastapi-coursefor-book/
def get_engine():
    return engine



