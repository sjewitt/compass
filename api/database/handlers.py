# up three levels to api:
from api.models import User, Competency, UserCompetencies, Quadrant, QuadrantTitles, \
    Sector, SectorTitles, CompassData, CompassDefinition, CompassSummary, Rating
from api.db_models import DB_Competency, DB_User, DB_Quadrant, DB_QuadrantTitles,  \
    DB_Sector, DB_SectorTitles, DB_CompassDefinition, DB_Rating
from api.exceptions import UserNotFound, CompetencyNotFound, CompetenciesForUserNotFound
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError, ResponseValidationError

from sqlalchemy import select, update
from sqlalchemy.orm import Session
import logging
logging.basicConfig(level=logging.INFO)

def check_quadrant_bounds(index:int) -> bool:
    if index < 0 or index > 3:
        logging.warning("Quadrant is out of bounds")
        return False
    return True

# NOTE: Quadrant 0 has 5 sectors, all others have 4
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
        result = session.execute(stmt).first()
        if result:
            return True
        return False

def add_user(engine,user:DB_User):
    # eventually, this all needs to go in database.py
    with Session(engine) as session:
        try:
            # new_user = user
            session.add(user)
            # https://stackoverflow.com/questions/36014700/sqlalchemy-how-do-i-see-a-primary-key-id-for-a-newly-created-record
            session.flush()
            # we should have an ID now:
            print(user.id)
            new_user_id = user.id
            session.commit()
            return {"action":"usercreate","usercreated":True, "id":new_user_id}
        except Exception as ex:
            print(ex)
            return {f"action":"usercreate","message":"Failed: {ex}", "usercreated":False}        
    return {"action":"usercreate","message":"Failed", "usercreated":False}

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
            print(isinstance(row,User))
            print(isinstance(row,DB_User))
            _usr = User(
                id=row.id,
                compass_id=row.compass_id,
                name=row.name,
                username=row.username,
                email=row.email,
            )
            print(isinstance(_usr,User))
            # result.append(_usr)

            result.append(row)  # original code (a DB_User)
            
        if result:
            # print("FOUND ", result[0])

            return result    # the first found user
        logging.warning("no users found")
        # raise UserNotFound("user with id %s not found" % user_id)
        return []

def get_user(engine, user_id:int) -> User|None:
    # eventually, this all needs to go in database.py
    # print(engine)
    with Session(engine) as session:
        # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html
        stmt = select(DB_User).where(DB_User.id == user_id)
        result = []
        # need to convert the DB_User into a User, so th epydantic validation works
        # also, TODO: need to update this to return ONE result...
        for row in session.scalars(stmt):
            _usr = User(
                id=row.id,
                compass_id=row.compass_id,
                name=row.name,
                username=row.username, 
                email=row.email)
            result.append(_usr)   # new: A User()
            # result.append(row) # orig a DB_User()
        if result:
            return result[0]    # the first found user
        logging.warning(f"user with id {user_id} not found")
        raise UserNotFound(404, "user with id %s not found" % user_id)
    
# All new
def get_user_data(engine, user_id:int) -> UserCompetencies: # to type!
    with Session(engine) as session:
        try:
            result=UserCompetencies(
                user=get_user(engine,user_id),
                competencies=[])
            _competencies = session.query(DB_Competency).where(DB_Competency.user_id == user_id).order_by(DB_Competency.quadrant).all()
            stmt = select(DB_Competency).where(DB_Competency.user_id == user_id)
            # for row in session.scalars(stmt):
            for row in _competencies:
                _competency = Competency(
                    user_id=user_id,
                    quadrant=row.quadrant,
                    sector=row.sector,
                    rating=row.rating,
                    )
                # TODO: Map quadrant and sector to static lookups for names
                result.competencies.append(_competency)
            return result
        except Exception as ex:
            print(ex)
            return {"status":"error", "message":ex}

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
        return []
        # raise CompetenciesForUserNotFound("Competencies for user_id %s not found" % (user_id,))

# https://docs.sqlalchemy.org/en/20/tutorial/data_update.html
def update_user(engine, user:User) -> User|None:

    with Session(engine) as session:
        try:
            # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html
            # extract the incoming User data and construct 

            if get_user(engine,user.id):
                stmt = update(DB_User).where(DB_User.id == user.id).values(
                    name=user.name,
                    compass_id=user.compass_id
                )  #, username=user.username, email=user.email)
                result = session.execute(stmt)
                session.commit()
                # TODO: make testing for user more robust! i.e. GET the user first!
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
                return user
            raise UserNotFound
        except:
            return None

def add_quadrant(engine,quadrant:Quadrant) -> dict:
    with Session(engine) as session:
        try:
            _q = DB_Quadrant(
                children=[],
                quadrant_summary=quadrant.quadrant_summary,
                quadrant_css_class=quadrant.quadrant_css_class,
                quadrant_elem_coords=quadrant.quadrant_elem_coords, # these will be constants?
            )
            session.add(_q)
            # https://stackoverflow.com/questions/36014700/sqlalchemy-how-do-i-see-a-primary-key-id-for-a-newly-created-record
            session.flush()
            # we should have an ID now:
            new_quadrant_id = _q.id
            # and add title parts:
            for quad_title_part in quadrant.title:
                _t = DB_QuadrantTitles(
                    title_part=quad_title_part.title_part,
                    quadrant_id=_q.id,
                )
                session.add(_t)
            session.commit()
            return {"action":"quadrantcreate","quadrantcreated":True, "id":new_quadrant_id}
        except Exception as ex:
            print(ex)
            return {f"action":"quadrantcreate","message":"Failed: {ex}", "quadrantcreated":False}        
    return {"action":"quadrantcreate","message":"Failed", "quadrantcreated":False}

def get_quadrants(engine, include_titles=False) -> list[Quadrant]:
    with Session(engine) as session:
        print("getting quads")
        result = []
        _quads = session.query(DB_Quadrant)
        print(_quads)
        
        # get each quad's title parts:
        for _quad in _quads:
            try:
                _titles = []
                if include_titles:
                    _db_quad_titles = session.query(DB_QuadrantTitles).where(DB_QuadrantTitles.quadrant_id==_quad.id).all()
                    _titleparts=[]
                    for _title_part in _db_quad_titles:
                        _x = QuadrantTitles(id=_title_part.id, title_part = _title_part.title_part)
                        _titleparts.append(_x)
                    _titles = _titleparts

                # build the final output as fully populated Quadrant:
                # there may be scope here for a Quadrant variant taht doesn't include title or sector array
                _res = Quadrant(
                    id=_quad.id,
                    title=_titles,
                    quadrant_summary=_quad.quadrant_summary,
                    quadrant_css_class=_quad.quadrant_css_class,
                    quadrant_elem_coords=_quad.quadrant_elem_coords,
                    )
                result.append(_res)
            except Exception as ex:
                print(ex)
        return result

def get_quadrant(engine, id:int) -> Quadrant:
    ''' get a quadrant by database ID '''
    with Session(engine) as session:
        db_quad = session.query(DB_Quadrant).where(DB_Quadrant.id == id).first()
        # db_quad_titles = session.query(DB_QuadrantTitles).where(DB_QuadrantTitles.quadrant_id==id).all()
        _titleparts=[]
        # for title_part in db_quad_titles:
        #     _x = QuadrantTitles(title_part = title_part.title_part)
        #     # cannot do this in one step!:
        #     # _titleparts.append(QuadrantTitles(title_part.title_part))
        #     # need to do this:
        #     _titleparts.append(_x)

        # build the final output as fully populated Quadrant:
        res = Quadrant(
            id=db_quad.id,
            title=_titleparts,
            quadrant_summary=db_quad.quadrant_summary,
            quadrant_css_class=db_quad.quadrant_css_class,
            quadrant_elem_coords=db_quad.quadrant_elem_coords,
        )
        # now we can return a fully populated object:
        return res
    
# (test) this is fine...
def get_quadrant_titles(engine) -> list[QuadrantTitles]:
    with Session(engine) as session:
        _z = []
        try:
            _x = session.query(DB_QuadrantTitles).all()
            
            for _y in _x:
                print(_y) # db model
                _z.append(QuadrantTitles(id=_y.id, title_part = _y.title_part, coord_x=_y.coord_x, coord_y=_y.coord_y)) # model
            return(_z)
        except Exception as ex:
            print(ex)
        return _z

def add_sector(engine,sector:Sector) -> dict:
    with Session(engine) as session:
        try:
            _s = DB_Sector(
                # quadrant_id = sector.quadrant_id,
                summary = sector.summary,
                description = sector.description,
            )
            session.add(_s) 
            session.flush() # this gives us the ID, which we need to append the title parts:
            new_sector_id = _s.id
            # to update: redirect to a new add title method (which will need an API endpoint too)
            # I also don't need the sector ID because there is no FK relationship now...
            for sector_title_part in sector.title:
                _t = DB_SectorTitles(
                    # sector_id = new_sector_id,
                    title_part = sector_title_part.title_part,
                    coord_x = sector_title_part.coord_x,
                    coord_y = sector_title_part.coord_y,
                )
                session.add(_t)
            session.commit()
            return {"action":"sectorcreate","sectorcreated":True, "id":new_sector_id}
        except Exception as ex:
            print(f"ERROR: {ex}")
            return {f"action":"sectorcreate","message":"Failed: {ex}", "sectorcreated":False}
    return {"action":"sectorcreate","message":"Failed", "sectorcreated":False} 

def get_sectors(engine) -> list[Sector]:
    with Session(engine) as session:
        # I think here I don't want to retrieve the childs (titles)
        # I think also the DB model should be looser?
        # possibly not. The Compass definition does not (YET!!) include
        # a lookup for sector or quadrant title. Therefore, the model should change to
        # remove this dependency comletely].
        # I may be left in the short term with a mismatch between a sector and it's 
        # intrinsically associated titles, and that defined by the Compass itself
        # (same for quad titles I think)
        # This is a big TODO:
        # Although, because I need to return a [Sector] (not a [DB_Sector]) I can
        # filter any childs out HERE as I construct the return data.
        _db_sectors = session.query(DB_Sector).all()
        _out = []
        for _db_sector in _db_sectors:
            _out.append(
                Sector(
                    id = _db_sector.id,
                    # quadrant_id = 0,
                    title=[],
                    summary = _db_sector.summary,
                    description = _db_sector.description,
                )
            )
        return _out

def get_sector(engine,id:int) -> Sector:
    with Session(engine) as session:
        db_sector = session.query(DB_Sector).where(DB_Sector.id == id).first()
        try:
            result = Sector(
                id=db_sector.id,
                # quadrant_id = db_sector.quadrant_id,
                title = [],
                summary = db_sector.summary,
                description = db_sector.description,
            )
            return result
        except Exception as ex:
            print(ex)

def get_sector_titles(engine) -> list[SectorTitles]:
    ''' return all sector titles '''
    with Session(engine) as session:
        _dbresults = session.query(DB_SectorTitles).all()
        _results = []
        for _dbresult in _dbresults:
            _results.append(SectorTitles(
                id=_dbresult.id,
                title_part=_dbresult.title_part, 
                coord_x=_dbresult.coord_x,
                coord_y=_dbresult.coord_y,
            )
        )
        return _results

def add_rating(engine, rating:Rating) -> bool:
    with Session(engine) as session:
        try:
            _r = DB_Rating(
                title = rating.title,
                description = rating.description,
            )
            session.add(_r)
            session.commit()
            return True
        except Exception as ex:
            logging.warning(f"Failed to add rating: {ex}")
            return False

def get_ratings(engine) -> list[Rating]:
    ''' get all ratings defined in database '''
    with Session(engine) as session:
        try:
            _ratings = []
            _db_ratings = session.query(DB_Rating)
            for _db_rating in _db_ratings:
                _rating = Rating(
                    id=_db_rating.id,
                    title = _db_rating.title,
                    description = _db_rating.description,
                )
                _ratings.append(_rating)
            return _ratings
        except Exception as ex:
            logging.warning(f"Failed to retrieve ratings: {ex}")

def get_rating(engine, id:int) -> Rating:
    ''' get a rating by database ID '''
    with Session(engine) as session:
        try:  
            _db_rating = session.query(DB_Rating).where(DB_Rating.id == id).first()
            _rating = Rating(
                id=_db_rating.id,
                title = _db_rating.title,
                description = _db_rating.description,
            )
            return _rating
        except Exception as ex:
            logging.warning(f"Failed to retrieve rating {id}: {ex}")

# get the lists of all configured data to use as dropdowns for compass assembly page:
# (give it an API endpoint too)
def retrieve_all_configured_data():
    all_ratings = get_ratings()
    all_quadrants = get_quadrants()
    all_sectors = get_sectors()

    data = {
        "ratings": all_ratings,
        "quadrants":all_quadrants,
        "sectors":all_sectors,
        }
    return data

# MOVE TO A NEW HANDLER:
# retrieve all compases (summary)
def get_all_compasses(engine) -> list[CompassSummary]:
    with Session(engine) as session:
        # stmt = select(DB_CompassDefinition())
        result = session.query(DB_CompassDefinition.id, DB_CompassDefinition.name)
        returnval = []
        for compass_summary in result:
            _cs = CompassSummary(
                id = compass_summary.id,
                name = compass_summary.name,
            )
            returnval.append(_cs)
        print(returnval)
        return returnval
        # for compass_summary in result:
        #     print(compass_summary)
    print("error")
    return []

# retrieve current compass data
# re #72, this may be a good placve to return the static coords data (I think
# the dababase column is ignored - though returned.)
# Let's add the constants to the models.
def get_compass(engine, id:int) -> CompassData:
    with Session(engine) as session:
        
        # THIS syntax works as a compound query:
        # result = session.query(DB_CompassDefinition,DB_Quadrant).where(DB_CompassDefinition.id==id).where(DB_Quadrant.id==DB_CompassDefinition.quadrant_1).first()
        _db_compass_def = session.query(DB_CompassDefinition).where(DB_CompassDefinition.id==id).first()
        _compass = {}
        if _db_compass_def:

            # explicitly retrieve each quad (even if it's the same one twice):
            _db_quadrants = []
            _db_quadrants.append(session.query(DB_Quadrant).where(DB_Quadrant.id == _db_compass_def.quadrant_1).first())
            _db_quadrants.append(session.query(DB_Quadrant).where(DB_Quadrant.id == _db_compass_def.quadrant_2).first())
            _db_quadrants.append(session.query(DB_Quadrant).where(DB_Quadrant.id == _db_compass_def.quadrant_3).first())
            _db_quadrants.append(session.query(DB_Quadrant).where(DB_Quadrant.id == _db_compass_def.quadrant_4).first())

            _db_quadrant_titles = []
            _db_quadrant_titles.append(_get_quadrant_title_parts(session, _db_compass_def.q1_tp1,_db_compass_def.q1_tp2))
            _db_quadrant_titles.append(_get_quadrant_title_parts(session, _db_compass_def.q2_tp1,_db_compass_def.q2_tp2))
            _db_quadrant_titles.append(_get_quadrant_title_parts(session, _db_compass_def.q3_tp1,_db_compass_def.q3_tp2))
            _db_quadrant_titles.append(_get_quadrant_title_parts(session, _db_compass_def.q4_tp1,_db_compass_def.q4_tp2))

            #likewise for ratings:
            _db_ratings = []
            _db_ratings.append(session.query(DB_Rating).where(DB_Rating.id == _db_compass_def.rating_1).first())
            _db_ratings.append(session.query(DB_Rating).where(DB_Rating.id == _db_compass_def.rating_2).first())
            _db_ratings.append(session.query(DB_Rating).where(DB_Rating.id == _db_compass_def.rating_3).first())
            _db_ratings.append(session.query(DB_Rating).where(DB_Rating.id == _db_compass_def.rating_4).first())
            _db_ratings.append(session.query(DB_Rating).where(DB_Rating.id == _db_compass_def.rating_5).first())
            _db_ratings.append(session.query(DB_Rating).where(DB_Rating.id == _db_compass_def.rating_6).first())
            _db_ratings.append(session.query(DB_Rating).where(DB_Rating.id == _db_compass_def.rating_7).first())

            # then get each quadrant's sectors:
            _db_q1_sectors = [
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_1_sector_1).first(),
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_1_sector_2).first(),
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_1_sector_3).first(),
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_1_sector_4).first(),
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_1_sector_5).first(),
            ]

            # and for each quadrant's sectors, get the titles:
            _q1_sectors_titles = [
                _get_sector_title_parts(session,_db_compass_def.q1_s1_tp1,_db_compass_def.q1_s1_tp2),
                _get_sector_title_parts(session,_db_compass_def.q1_s2_tp1,_db_compass_def.q1_s2_tp2),
                _get_sector_title_parts(session,_db_compass_def.q1_s3_tp1,_db_compass_def.q1_s3_tp2),
                _get_sector_title_parts(session,_db_compass_def.q1_s4_tp1,_db_compass_def.q1_s4_tp2),
                _get_sector_title_parts(session,_db_compass_def.q1_s5_tp1,_db_compass_def.q1_s5_tp2),
            ] 


            _db_q2_sectors = [
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_2_sector_1).first(),
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_2_sector_2).first(),
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_2_sector_3).first(),
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_2_sector_4).first(),
            ]
            
            _q2_sectors_titles = [
                _get_sector_title_parts(session,_db_compass_def.q2_s1_tp1,_db_compass_def.q2_s1_tp2),
                _get_sector_title_parts(session,_db_compass_def.q2_s2_tp1,_db_compass_def.q2_s2_tp2),
                _get_sector_title_parts(session,_db_compass_def.q2_s3_tp1,_db_compass_def.q2_s3_tp2),
                _get_sector_title_parts(session,_db_compass_def.q2_s4_tp1,_db_compass_def.q2_s4_tp2),
            ]

            _db_q3_sectors = [
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_3_sector_1).first(),
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_3_sector_2).first(),
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_3_sector_3).first(),
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_3_sector_4).first(),
            ]

            _q3_sectors_titles = [
                _get_sector_title_parts(session,_db_compass_def.q3_s1_tp1,_db_compass_def.q3_s1_tp2),
                _get_sector_title_parts(session,_db_compass_def.q3_s2_tp1,_db_compass_def.q3_s2_tp2),
                _get_sector_title_parts(session,_db_compass_def.q3_s3_tp1,_db_compass_def.q3_s3_tp2),
                _get_sector_title_parts(session,_db_compass_def.q3_s4_tp1,_db_compass_def.q3_s4_tp2),
            ]

            _db_q4_sectors = [
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_4_sector_1).first(),
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_4_sector_2).first(),
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_4_sector_3).first(),
                session.query(DB_Sector).where(DB_Sector.id == _db_compass_def.quadrant_4_sector_4).first(),
            ]

            _q4_sectors_titles = [
                _get_sector_title_parts(session,_db_compass_def.q4_s1_tp1,_db_compass_def.q4_s1_tp2),
                _get_sector_title_parts(session,_db_compass_def.q4_s2_tp1,_db_compass_def.q4_s2_tp2),
                _get_sector_title_parts(session,_db_compass_def.q4_s3_tp1,_db_compass_def.q4_s3_tp2),
                _get_sector_title_parts(session,_db_compass_def.q4_s4_tp1,_db_compass_def.q4_s4_tp2),
            ]

            # Then construct the pydantic model from the database models returned:
            # [I already have teh title IDs, so use them here?]

            _q1_sectors = _get_sector_models_from_db_models(_db_compass_def.quadrant_1,_db_q1_sectors,_q1_sectors_titles)
            _q2_sectors = _get_sector_models_from_db_models(_db_compass_def.quadrant_2,_db_q2_sectors,_q2_sectors_titles)
            _q3_sectors = _get_sector_models_from_db_models(_db_compass_def.quadrant_3,_db_q3_sectors,_q3_sectors_titles)
            _q4_sectors = _get_sector_models_from_db_models(_db_compass_def.quadrant_4,_db_q4_sectors,_q4_sectors_titles)

            # these are pydantic models:
            _sectors = [_q1_sectors,_q2_sectors,_q3_sectors,_q4_sectors]

            # and THESE are database models (should probably modify to pass same type of data):
            # although it may be OK as all this is doing is attaching the rithr Sectors to each 
            # returned Quadrant.
            # update: as I am building the entire thing here, and I now have the quad titles for each, I
            # can pass them in here (though be careful with model vs db_model types!!)
            _quadrants = _get_quadrant_models_from_db_models(_db_quadrants,_db_quadrant_titles, _sectors)
            
            _ratings = _get_rating_models_from_db_models(_db_ratings)

            try:
                _compass = CompassData(
                    id = _db_compass_def.id,
                    title = _db_compass_def.name,
                    data_quadrants = _quadrants,
                    # and we need the `ratings_description_lookup` field too:
                    rating_description_lookup = _ratings,
                    # titles = [{"points":[1,2,3,4,5,6,7,8], "title":}]
                )

            except RequestValidationError as ex:
                print("request validation error")
                print(ex)

            except ResponseValidationError as ex:
                print("response validation error")
                print(ex)

            except Exception as ex:
                print("Exception")
                print(ex)
            # # retrieve the compass data by ID, then use the FK IDs to reconstruct the actual data
            # # from the stored data (TODO: UI to create...)
            # # get the definition:
            # # now, I SHOULD be able to make a complex query here to do this...
            ############################################################################
            # see https://stackoverflow.com/questions/55053618/sqlalchemy-return-filtered-table-and-corresponding-foreign-table-values
            ############################################################################
            # stmt = select(DB_CompassDefinition).where(DB_CompassDefinition.id == id)
            # result = []
            # counter = 0
            # for row in session.scalars(stmt):
            #     # get the data for each ID
            #     stmt = select(DB_Quadrant).where(DB_Quadrant.id==row.)
            #     result.append()
            #     if counter > 0:
            #         break
            #     counter+=1
            # pass
            print(_compass)
            ## TODO: I meed to model the competency level data - this needs a new table
            return _compass
        else:
            print(f"No compass matching ID {id}")
            # return CompassData()
            raise IndexError(f"No compass matching ID {id}")


def _get_quadrant_models_from_db_models(
        db_quadrant_model_list:list[DB_Quadrant],
        quadrant_titles_list:list[list[QuadrantTitles]],
        sector_models_list:list[list[Sector]]) -> list[Quadrant]:
    _out = []
    _counter = 0
    for db_quadrant_model in db_quadrant_model_list:
        logging.debug(db_quadrant_model)

        _titles = []
        # _titles.append(quadrant_titles_list[_counter][0])
        for title_part in quadrant_titles_list[_counter]:  # the sector titles
            _titles.append(
                QuadrantTitles(
                    id=title_part.id,
                    title_part=title_part.title_part,
                    coord_x=title_part.coord_x,
                    coord_y=title_part.coord_y,
                )
            )
        try:
            _out.append(
                Quadrant(
                    id = db_quadrant_model.id,
                    title = _titles,
                    quadrant_summary = db_quadrant_model.quadrant_summary,
                    quadrant_css_class = db_quadrant_model.quadrant_css_class,
                    quadrant_elem_coords = db_quadrant_model.quadrant_elem_coords,
                    sectors = sector_models_list[_counter],
                )
            )
            _counter += 1
        except Exception as ex:
            logging.warning(f"failed to add quadrant {ex}")
    return _out
        
def _get_sector_models_from_db_models(quadrant_id:int, db_sector_model_list:list[DB_Sector],sector_title_model_list) -> list[Sector]:
    ''' retrieve the list of title parts for each set of sectors for supplied quadrant data '''
    _out = []
    _counter = 0
    for db_sector_model in db_sector_model_list:
        # print(db_sector_model)
        
        _titles = []
        for title_part in sector_title_model_list[_counter]:  # the sector titles
            _titles.append(
                SectorTitles(
                    id=title_part.id,
                    title_part=title_part.title_part,
                    coord_x=title_part.coord_x,
                    coord_y=title_part.coord_y,
               )
            )
            
        _out.append(
            Sector(
                id=db_sector_model.id,
                quadrant_id=quadrant_id,
                title=_titles,  # MAY NEED TO REMOVE THIS FORM THE MODEL!
                summary=db_sector_model.summary,
                description=db_sector_model.description,
            )
        )
        _counter += 1
    return _out

def _get_rating_models_from_db_models(db_rating_model_list:list[DB_Rating]) -> list[Rating]:
    _out = []
    for db_rating_model in db_rating_model_list:
        _out.append(
            Rating(
                id=db_rating_model.id,
                title=db_rating_model.title,
                description=db_rating_model.description,
            )
        )
    return _out

def _get_quadrant_title_parts(session,tp1:int, tp2:int) -> list[QuadrantTitles]:
    ''' return an array of titles [0, 1 or 2 length] '''
    _returnval = []
    if tp1 and tp2: # not null, or > 0
        _returnval.append(session.query(DB_QuadrantTitles).where(DB_QuadrantTitles.id == tp1).first())
        _returnval.append(session.query(DB_QuadrantTitles).where(DB_QuadrantTitles.id == tp2).first())
    if tp1 and not tp2: # not null, or > 0
        _returnval.append(session.query(DB_QuadrantTitles).where(DB_QuadrantTitles.id == tp1).first())
    if tp2 and not tp1: # not null, or > 0
        _returnval.append(session.query(DB_QuadrantTitles).where(DB_QuadrantTitles.id == tp2).first())
    return _returnval

def _get_sector_title_parts(session,tp1:int, tp2:int) -> list[SectorTitles]:
    ''' return an array of titles [0, 1 or 2 length] '''
    _returnval = []
    if tp1 and tp2: # not null, or > 0
        _returnval.append(session.query(DB_SectorTitles).where(DB_SectorTitles.id == tp1).first())
        _returnval.append(session.query(DB_SectorTitles).where(DB_SectorTitles.id == tp2).first())
    if tp1 and not tp2: # not null, or > 0
        _returnval.append(session.query(DB_SectorTitles).where(DB_SectorTitles.id == tp1).first())
    if tp2 and not tp1: # not null, or > 0
        _returnval.append(session.query(DB_SectorTitles).where(DB_SectorTitles.id == tp2).first())
    return _returnval


# TODO: Split handlers into modules mirroring the routers:

# generate compass data using extisting quadrants and sectors:
def set_compass(engine, definition:CompassDefinition,id:int = 0) -> int:
    # if int, update, else add new
    with Session(engine) as session:
        if id:
            # update:
            return -1
        else:
            # add new compass definition:
            # construct a DB model for the compass:
            _compass = DB_CompassDefinition(
                name = definition.name,
                quadrant_1 = definition.quadrants[0].quadrant,
                quadrant_2 = definition.quadrants[1].quadrant,
                quadrant_3 = definition.quadrants[2].quadrant,
                quadrant_4 = definition.quadrants[3].quadrant,
                # Q1
                quadrant_1_sector_1 = definition.quadrants[0].sectors[0],
                quadrant_1_sector_2 = definition.quadrants[0].sectors[1],
                quadrant_1_sector_3 = definition.quadrants[0].sectors[2],
                quadrant_1_sector_4 = definition.quadrants[0].sectors[3],
                quadrant_1_sector_5 = definition.quadrants[0].sectors[4],

                # Q2
                quadrant_2_sector_1 = definition.quadrants[1].sectors[0],
                quadrant_2_sector_2 = definition.quadrants[1].sectors[1],            
                quadrant_2_sector_3 = definition.quadrants[1].sectors[2],
                quadrant_2_sector_4 = definition.quadrants[1].sectors[3],

                # Q3
                quadrant_3_sector_1 = definition.quadrants[2].sectors[0],
                quadrant_3_sector_2 = definition.quadrants[2].sectors[1],            
                quadrant_3_sector_3 = definition.quadrants[2].sectors[2],
                quadrant_3_sector_4 = definition.quadrants[2].sectors[3],

                # Q4
                quadrant_4_sector_1 = definition.quadrants[3].sectors[0],
                quadrant_4_sector_2 = definition.quadrants[3].sectors[1],            
                quadrant_4_sector_3 = definition.quadrants[3].sectors[2],
                quadrant_4_sector_4 = definition.quadrants[3].sectors[3],

                # Ratings
                rating_1 = definition.ratings[0],
                rating_2 = definition.ratings[1],
                rating_3 = definition.ratings[2],
                rating_4 = definition.ratings[3],
                rating_5 = definition.ratings[4],
                rating_6 = definition.ratings[5],
                rating_7 = definition.ratings[6],
            )
            try:
                session.add(_compass)
                session.flush()
                # get ID:
                new_compass_id = _compass.id
                session.commit()
                return new_compass_id
            except Exception as ex:
                print(f"Exception attempting to insert new compass definition: {ex}")
        
    # if fails:
    return -2







