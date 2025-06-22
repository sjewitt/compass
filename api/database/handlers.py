# up three levels to api:
from compass import User, Competency    #  DB_User, DB_Competency, C
from api.db_models import DB_Competency, DB_User
from api.exceptions import UserNotFound, CompetencyNotFound, CompetenciesForUserNotFound
from sqlalchemy import select, update
from sqlalchemy.orm import Session
import logging


def check_quadrant_bounds(index:int) -> bool:
    if index < 0 or index > 3:
        logging.warning("Quadrant is out of bounds")
        return False
    return True


# NOTE: Quadrant 0 has 5 sectors, all other s have 4
def check_sector_bounds(quadrant_index:int, sector_index) -> bool:
    upper_bound = 3
    if quadrant_index == 0:
        upper_bound = 4
    if sector_index < 0 or sector_index > upper_bound:
        logging.warning("Sector is out of bounds")
        return False
    return True

def check_ratings_bounds(rating:int):
    if rating < 1 or rating > 6:
        logging.warning("Rating is out of bounds")
        return False
    return True

# note: `session` comes from main handler function
def check_user_exists(engine, user_id:int) -> bool:
    if get_user(engine, user_id):
        return True
    logging.warning("User does not exist")
    return False

def check_competency_is_applied_to_user_already(engine,competency:DB_Competency) -> bool:
    ''' check whether a competency for user_id, quadrant and sector is present already. ''' 
    with Session(engine) as session:
        stmt = select(DB_Competency).where(
                DB_Competency.user_id == competency.user_id).where(
                DB_Competency.quadrant == competency.quadrant).where(
                DB_Competency.sector == competency.sector)
        # print(stmt)
        result = session.execute(stmt).first()
        # print(result)
        if result:
            return True
        return False
        # session.add(user)
        # session.commit()


def add_user(engine,user:DB_User):
    # eventually, this all needs to go in database.py
    with Session(engine) as session:
        # new_user = user
        session.add(user)
        session.commit()


def add_competency(engine, competency:DB_Competency) -> dict:   # status object
    if check_user_exists(engine,competency.user_id)                                 \
                and check_quadrant_bounds(competency.quadrant)                      \
                and check_sector_bounds(competency.quadrant,competency.sector)      \
                and check_ratings_bounds(competency.rating):
        # here, check whetherthe competency is already applied to user:
        # - if so, UPDATE
        # - if NOT, add new (logic to change!)
        # print(check_competency_is_applied_to_user_already(engine,competency))
        if not check_competency_is_applied_to_user_already(engine,competency):
            # print("ADDING NEW COMPETENCY")
            with Session(engine) as session:
                session.add(competency)
                # does this honour the foreign key?
                session.commit()
                return {"status":"added", "message":"Added competency to user"}
            # might fail also
            # TODO

        else:
            # UPDATE competency
            # print("UPDATING COMPETENCY")
            stmt = (update(DB_Competency)
                    .where(DB_Competency.user_id==competency.user_id)
                    .where(DB_Competency.quadrant==competency.quadrant)
                    .where(DB_Competency.sector == competency.sector)
                    .values(rating=competency.rating)
            )
            # print(stmt)
            with Session(engine) as session:
                session.execute(stmt)
                session.commit()
            
                return {"status":"updated", "message":"user competency updated TODO"}
            return {"status":"update failed","message":"update failed"}

    else:
        # print("values OOB %s, %s or User does not exist %s" % (competency.quadrant, competency.sector, competency.user_id))
        return {"status":"failed", "message":"Bounds or user check failed."}


def get_users(engine) -> list[User]|None:
    
    with Session(engine) as session:
        # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html
        stmt = select(DB_User)
        result = []
        # need to convert the DB_User into a User, so th epydantic validation works
        for row in session.scalars(stmt):
            # print(row.id,row.name,row.username,row.email)
            # print(row.name)
            # print(row.username)
            # print(row.email)
            # _usr = User(id=row.id,name=row.name,username=row.username, email=row.email)
            # breakpoint()
            result.append(row)

        if result:
            # print("FOUND ", result[0])

            return result    # the first found user
        logging.warning("no users found")
        # raise UserNotFound("user with id %s not found" % user_id)
        return None



def get_user(engine, user_id:int) -> User|None:
    # eventually, this all needs to go in database.py
    # print(engine)
    with Session(engine) as session:
        # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html
        stmt = select(DB_User).where(DB_User.id == user_id)
        result = []
        # need to convert the DB_User into a User, so th epydantic validation works
        for row in session.scalars(stmt):
            # print(row.id,row.name,row.username,row.email)
            # print(row.name)
            # print(row.username)
            # print(row.email)
            _usr = User(id=row.id,name=row.name,username=row.username, email=row.email)
            # breakpoint()
            result.append(row)

        if result:
            # print("FOUND ", result[0])

            return result[0]    # the first found user
        logging.warning(f"user with id {user_id} not found")
        # raise UserNotFound("user with id %s not found" % user_id)
        return None


def get_competency(engine, competency_id:int) -> Competency|None:
    with Session(engine) as session:
        # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html
        stmt = select(DB_Competency).where(DB_Competency.id == competency_id)
        result = []
        # need to convert the DB_User into a User, so th epydantic validation works
        for row in session.scalars(stmt):
            result.append(row)

        if result:
            return result[0]    # the first found user
        print(f"competency with id {competency_id} not found")
        raise CompetencyNotFound("Competency with id %s not found" % competency_id)
    
def get_competencies_for_user(engine, user_id:int) -> list[Competency]:
    with Session(engine) as session:
        # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html
        stmt = select(DB_Competency).where(DB_Competency.user_id == user_id)
        result = []
        # need to convert the DB_User into a User, so th epydantic validation works
        for row in session.scalars(stmt):
            result.append(row)

        if result:
            return result
        print(f"No competencies found for user with id {user_id}")
        raise CompetenciesForUserNotFound("Competencies for user_id %s not found" % (user_id,))


# https://docs.sqlalchemy.org/en/20/tutorial/data_update.html
def update_user(engine, user:User) -> User|None:

    with Session(engine) as session:
        # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html
        # extract the incoming User data and construct 
        stmt = update(DB_User).where(DB_User.id == user.id).values(name=user.name, username=user.username, email=user.email)
        
        result = session.execute(stmt)

        # # need to convert the DB_User into a User, so th epydantic validation works
        # for row in session.scalars(stmt):
        #     # print(row.id,row.name,row.username,row.email)
        #     print(row.name)
        #     print(row.username)
        #     print(row.email)
        #     _usr = User(name=row.name,username=row.username, email=row.email)
        #     # breakpoint()
        #     result.append(row)

        # if result:
        #     # print("FOUND ", result[0])
        #     # print("FOUND ", result[0]["username"])

        #     return result[0]    # the first found user
        # print(f"user with id {user_id} not found")
        # raise UserNotFound("user with id %s not found" % user_id)