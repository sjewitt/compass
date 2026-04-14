from pydantic import BaseModel, EmailStr, Field
# see https://fastapi.tiangolo.com/it/tutorial/extra-models/#multiple-models

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
    user_id:int = Field()   # actually a FK to users table
    quadrant:int = Field(min=0, max=3)
    sector:int = Field(min=0, max=4)
    rating:int = Field(min=0, max=5)

# https://fastapi.tiangolo.com/it/tutorial/body-nested-models/#define-a-submodel
class UserCompetencies(BaseModel):
    # user:int    #orig
    user:User  # new
    competencies:list[Competency]


'''
Model the compass lookup data
'''
class SectorTitles(BaseModel):  # RENAME!!
    id: int = Field()
    # sector_id:int = Field()
    title_part:str = Field()
    coord_x:int=Field()
    coord_y:int=Field()

class Sector(BaseModel):
    id:int = Field()
    # quadrant_id:int=Field(default_factory=0) # this can probably go?
    title : list[SectorTitles] = Field(max_length=2, default_factory=list)
    summary:str=Field()
    description:str=Field()

# TO REVISIT
# This is exactly what the oreilly course described as the method for not showing the ID
# on te response model when a DB is used

# class _QuadrantTitlesId(BaseModel):
#     id: int = Field()

# class _QuadrantTitlesBase(BaseModel):
#     title_part:str=Field()    

# class QuadrantTitles(_QuadrantTitlesId,_QuadrantTitlesBase):
#     def __repr__(self):
#         return "<QuadrantTitles(ID='%s', title_part='%s')>" % (
#             self.id,
#             self.title_part
#         )

# class QuadrantTitlesIn(_QuadrantTitlesBase):
#     def __repr__(self):
#         return "<QuadrantTitles(title_part='%s')>" % (
#             self.title_part
#         )

class QuadrantTitles(BaseModel):
    id: int = Field()   # I DO NOT NEED THIS!!
    # quadrant_id:int=Field() # WTF?
    title_part:str=Field()
    coord_x:int  = Field()
    coord_y:int  = Field()
    # override the built-in dunder method so we get a better print:
    def __repr__(self):
        return "<QuadrantTitles(id='%s', title_part='%s')>" % (
            self.id,
            self.title_part
        )

# https://stackoverflow.com/questions/76398690/how-can-i-prevent-an-unknown-id-field-from-showing-in-fastapi-documentation-when
# HAH!! Also, see the oreilly course I am doing. He does exactly this!
# class _QuadrantId(BaseModel):
#     id: int = Field()

# class _QuadrantBase(BaseModel):
#     # title : list[QuadrantTitles] = Field(max_length=2)
#     quadrant_summary: str = Field()
#     quadrant_css_class:str = Field()
#     quadrant_elem_coords:str = Field()

# class QuadrantIn(_QuadrantBase):
#     title : list[QuadrantTitlesIn] = Field(max_length=2)
#     # pass

# class Quadrant(_QuadrantBase, _QuadrantId):
#     title : list[QuadrantTitles] = Field(max_length=2)
#     # pass

class Quadrant(BaseModel):
    id: int = Field()
    # https://stackoverflow.com/questions/63793662/how-to-give-a-pydantic-list-field-a-default-value
    title : list[QuadrantTitles] = Field(max_length=2,default_factory=list)
    quadrant_summary: str = Field()
    quadrant_css_class:str = Field()
    quadrant_elem_coords:str = Field()
    sectors:list[Sector] = Field(min_length=4, max_length=5,default_factory=list)

class CompassSummary(BaseModel):
    id:int = Field()
    name:str = Field(min_length=4, max_length=128)


# class Q0(Quadrant):
#     sectors:list[Sector]=Field(min_length=5, max_length=5)
# class Q1(Quadrant):
#     sectors:list[Sector]=Field(min_length=4, max_length=4)
# class Q2(Quadrant):
#     sectors:list[Sector]=Field(min_length=4, max_length=4)
# class Q3(Quadrant):
#     sectors:list[Sector]=Field(min_length=4, max_length=4)

class RatingIn(BaseModel):
    # ID?
    title:str = Field()
    description:str = Field()

class Rating(RatingIn):
    id:int = Field()    # the database ID, which we will need for lookups etc.

class CompassData(BaseModel):
    id:int=Field(default_factory=0)
    title:str=Field()
    data_quadrants: list[Quadrant] = Field(min_length=4, max_length=4)
    # name:str = Field(min_length=4, max_length=128)
    # quad_0:Quadrant = Q0
    # quad_1:Quadrant = Q1
    # quad_2:Quadrant = Q2
    # quad_3:Quadrant = Q3
    # quad_0:Q0 = Field()
    # quad_1:Q1 = Field()
    # quad_2:Q2 = Field()
    # quad_3:Q3 = Field()
    rating_description_lookup: list[Rating] = Field(min_length=7, max_length=7)  # to account for the code using 1-indexed lookup (TO FIX)

class QuadrantDefinition(BaseModel):
    quadrant:int=Field()
    # This needs front-end logic to account for the first quadrant having 5...
    sectors:list[int] = Field(min_length=4, max_length=5)

# constants defining the Compass quadrant and sector titles,
# the quadrant colours and the main quadrant title border coords:
# class Coordinate(BaseModel):
#     coord:list[int]=Field(min_length=2, max_length=2)

# class TitleCoordinate(BaseModel):
#     coordinates:list[Coordinate] = Field(min_length=1, max_length=2)

# class QuadrantTitles(BaseModel):
#     # define outer quad title borders
#     points:list[int] = Field(min_length=8, max_length=8)
#     title:TitleCoordinate = Field()
#     sectors:list[TitleCoordinate] = Field(min_length=4, max_length=5)


class CompassDefinition(BaseModel):
    name:str = Field(min_length=4, max_length=128)
    # these are all ints (IDs of the relevant quadrants and sectors)
    quadrants:list[QuadrantDefinition] = Field(min_length=4, max_length=4)
    ratings:list[int] = Field(min_length=7, max_length=7)   # these are Ratig IDs
    # titles: list[QuadrantTitles] = Field(min_length=4, max_length=4)

