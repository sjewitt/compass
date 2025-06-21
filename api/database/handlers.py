# up three levels to api:
from compass import DB_User, User
from api.exceptions import UserNotFound
from sqlalchemy import select
from sqlalchemy.orm import Session

def add_user(engine,user:DB_User):
    # eventually, this all needs to go in database.py
    with Session(engine) as session:
        new_user = user
        session.add(user)
        session.commit()

def get_user(engine, user_id:int) -> User|None:
    # eventually, this all needs to go in database.py
    print(engine)
    with Session(engine) as session:
        # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html
        stmt = select(DB_User).where(DB_User.id == user_id)
        result = []
        # need to convert the DB_User into a User, so th epydantic validation works
        for row in session.scalars(stmt):
            # print(row.id,row.name,row.username,row.email)
            print(row.name)
            print(row.username)
            print(row.email)
            _usr = User(name=row.name,username=row.username, email=row.email)
            # breakpoint()
            result.append(row)

        if result:
            # print("FOUND ", result[0])
            # print("FOUND ", result[0]["username"])

            return result[0]    # the first found user
        print(f"user with id {user_id} not found")
        raise UserNotFound("user with id %s not found" % user_id)
