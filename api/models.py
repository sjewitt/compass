from pydantic import BaseModel, EmailStr, Field
# see https://fastapi.tiangolo.com/it/tutorial/extra-models/#multiple-models

# explanation of Field():
#
# https://stackoverflow.com/questions/60661687/what-is-the-purpose-of-using-field-as-a-default-value-in-pydantic-schemas
# https://pydantic.dev/docs/validation/dev/concepts/fields/
#
# So not necessary for most of the below, BUT will be useful to at least partially answer the compasscefinition validation.
# Currently, the fastapi /docs model uses zeroes so I can add an annotation to force > 0 (though this will not of
# course validate the database content for that supplied ID...)


class APIResponseMessage(BaseModel):
    # status_code:int = 200
    message: str
    success: bool   # easily accessible flag indicating whether the front-end should try to further process.
    source: str     # the function/namespace.
    data: dict = {} # arbitrary data placeholder.


class User(BaseModel):
    id: int=Field()     # new - from DB ID field
    compass_id:int=Field()
    name: str = Field()
    username: str = Field()
    email: EmailStr = Field()

class CreateUser(BaseModel):
    compass_id:int=Field()
    name: str = Field()
    username: str = Field()
    email: EmailStr = Field()
    password: str
    password_check: str


'''
A User row can map to zero or more Competencies.
 - A Competency is added when a user selects something from the graphic
 - the update key therefore is `user_id + quadrant + sector`, with the updated value being the rating
 - therefore we do have some redundancy, but as it is ints, the data is very small
   - we don't have a single 'competency' lookup table (though we will need an in-code
     lookup mapping quad/sect to an actual name)
'''
class Competency(BaseModel):
    ''' this maps to the compass quadrants and sectors, and the current rating for each '''
    user_id:int = Field()        # FK to users table
    compass_id:int = Field()     # FK to compass_definition table
    quadrant:int = Field(min=0, max=3)  # zero-based indexes
    sector:int = Field(min=0, max=4)    # zero-based indexes
    rating:int = Field(min=0, max=5)    # zero-based indexes

# https://fastapi.tiangolo.com/it/tutorial/body-nested-models/#define-a-submodel
class UserCompetencies(BaseModel):
    user:User  # new
    competencies:list[Competency]


'''
Model the compass lookup data
'''
class SectorTitlesIn(BaseModel):  # RENAME!!
    title_part:str = Field()

class SectorTitles(SectorTitlesIn):
    id: int = Field()

class SectorIn(BaseModel):
    summary:str=Field()
    description:str=Field()

class Sector(SectorIn):
    id:int = Field()
    title : list[SectorTitles] = Field(max_length=2, default_factory=list)  # probably don't need this


class QuadrantTitlesIn(BaseModel):
    title_part:str=Field()

class QuadrantTitles(QuadrantTitlesIn):
    id: int = Field()   # I DO NOT NEED THIS!!
    # override the built-in dunder method so we get a better print:
    def __repr__(self):
        return "<QuadrantTitles(id='%s', title_part='%s')>" % (
            self.id,
            self.title_part
        )
    
# https://stackoverflow.com/questions/76398690/how-can-i-prevent-an-unknown-id-field-from-showing-in-fastapi-documentation-when
# Can I adapt the handler to bypass the nested model? It doesn't need it as I can pass an empty array...
# We also DO NOT need the CSS and coords as these are handled as constants (also, ties in with DB changes TODO:)
class QuadrantIn(BaseModel):
    quadrant_summary: str = Field()
    quadrant_description: str = Field()

# exclude the optional sector and title list:
class QuadrantBase(QuadrantIn):
    id: int = Field()

# TODO: Better document WHY I have three models here.
class Quadrant(QuadrantIn):
    id: int = Field()
    # https://stackoverflow.com/questions/63793662/how-to-give-a-pydantic-list-field-a-default-value
    title : list[QuadrantTitles] = Field(max_length=2,default_factory=list)
    sectors:list[Sector] = Field(max_length=5,default_factory=list)

# Don't need an 'in' model for this:
class CompassSummary(BaseModel):
    id:int = Field()
    name:str = Field(min_length=4, max_length=128)
    status_code:int = Field(200)


class RatingIn(BaseModel):
    title:str = Field()
    description:str = Field()

class Rating(RatingIn):
    id:int = Field()    # the database ID, which we will need for lookups etc.


class CompassData(BaseModel):
    id:int=Field(default_factory=0)
    title:str=Field()
    description:str=Field()
    data_quadrants: list[Quadrant] = Field(min_length=4, max_length=4)
    rating_description_lookup: list[Rating] = Field(min_length=7, max_length=7)  # to account for the code using 1-indexed lookup (TO FIX)

class QuadrantDefinition(BaseModel):
    quadrant:int=Field()
    # This needs front-end logic to account for the first quadrant having 5...
    sectors:list[int] = Field(min_length=4, max_length=5)

# map to actual database model:
class CompassDefinitionIn(BaseModel):
    name:str = Field(min_length=4, max_length=128)
    description:str = Field()

    # Specify the quadrants (4)
    quadrant_1 : int = Field(gt=0)  # database ID
    quadrant_2 : int = Field(gt=0)
    quadrant_3 : int = Field(gt=0)
    quadrant_4 : int = Field(gt=0)

    # specify quadrant_title parts:
    q1_tp1 : int = Field(gt=0)
    q1_tp2 : int = Field(gt=0)
    q2_tp1 : int = Field(gt=0)
    q2_tp2 : int = Field(gt=0)
    q3_tp1 : int = Field(gt=0)
    q3_tp2 : int = Field(gt=0)
    q4_tp1 : int = Field(gt=0)
    q4_tp2 : int = Field(gt=0)

    # specify the sectors per quadrant (5, 4, 4, 4)
    quadrant_1_sector_1 : int = Field(gt=0)
    quadrant_1_sector_2 : int = Field(gt=0)
    quadrant_1_sector_3 : int = Field(gt=0)
    quadrant_1_sector_4 : int = Field(gt=0)
    quadrant_1_sector_5 : int = Field(gt=0)

    # specify q1 sector titles
    q1_s1_tp1 : int = Field(gt=0)
    q1_s1_tp2 : int = Field(gt=0)
    q1_s2_tp1 : int = Field(gt=0)
    q1_s2_tp2 : int = Field(gt=0)
    q1_s3_tp1 : int = Field(gt=0)
    q1_s3_tp2 : int = Field(gt=0)
    q1_s4_tp1 : int = Field(gt=0)
    q1_s4_tp2 : int = Field(gt=0)
    q1_s5_tp1 : int = Field(gt=0)
    q1_s5_tp2 : int = Field(gt=0)

    quadrant_2_sector_1 : int = Field(gt=0)
    quadrant_2_sector_2 : int = Field(gt=0)
    quadrant_2_sector_3 : int = Field(gt=0)
    quadrant_2_sector_4 : int = Field(gt=0)

    # specify q2 sector titles
    q2_s1_tp1 : int = Field(gt=0)
    q2_s1_tp2 : int = Field(gt=0)
    q2_s2_tp1 : int = Field(gt=0)
    q2_s2_tp2 : int = Field(gt=0)
    q2_s3_tp1 : int = Field(gt=0)
    q2_s3_tp2 : int = Field(gt=0)
    q2_s4_tp1 : int = Field(gt=0)
    q2_s4_tp2 : int = Field(gt=0)

    quadrant_3_sector_1 : int = Field(gt=0)
    quadrant_3_sector_2 : int = Field(gt=0)
    quadrant_3_sector_3 : int = Field(gt=0)
    quadrant_3_sector_4 : int = Field(gt=0)

    # specify q3 sector titles
    q3_s1_tp1 : int = Field(gt=0)
    q3_s1_tp2 : int = Field(gt=0)
    q3_s2_tp1 : int = Field(gt=0)
    q3_s2_tp2 : int = Field(gt=0)
    q3_s3_tp1 : int = Field(gt=0)
    q3_s3_tp2 : int = Field(gt=0)
    q3_s4_tp1 : int = Field(gt=0)
    q3_s4_tp2 : int = Field(gt=0)

    quadrant_4_sector_1 : int = Field(gt=0)
    quadrant_4_sector_2 : int = Field(gt=0)
    quadrant_4_sector_3 : int = Field(gt=0)
    quadrant_4_sector_4 : int = Field(gt=0)

    # specify q4 sector titles
    q4_s1_tp1 : int = Field(gt=0)
    q4_s1_tp2 : int = Field(gt=0)
    q4_s2_tp1 : int = Field(gt=0)
    q4_s2_tp2 : int = Field(gt=0)
    q4_s3_tp1 : int = Field(gt=0)
    q4_s3_tp2 : int = Field(gt=0)
    q4_s4_tp1 : int = Field(gt=0)
    q4_s4_tp2 : int = Field(gt=0)

    # and the Ratings (7!!):
    rating_1 : int = Field(gt=0)
    rating_2 : int = Field(gt=0)
    rating_3 : int = Field(gt=0)
    rating_4 : int = Field(gt=0)
    rating_5 : int = Field(gt=0)
    rating_6 : int = Field(gt=0)
    rating_7 : int = Field(gt=0)

class CompassDefinition(CompassDefinitionIn):
    id:int = Field(gt=0)  # the database ID, which we will need for lookups etc.