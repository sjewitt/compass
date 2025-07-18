from pydantic import BaseModel, EmailStr, Field
# see https://fastapi.tiangolo.com/it/tutorial/extra-models/#multiple-models

class User(BaseModel):
    id: int=Field()     # new - from DB ID field
    name: str = Field()
    username: str = Field()
    email: EmailStr = Field()

class CreateUser(BaseModel):
    name: str = Field()
    username: str = Field()
    email: EmailStr = Field()
    password: str
    password_check: str

class Quadrant(BaseModel):
    id: int = Field()
    name: str = Field()

class Sector(BaseModel):
    id: int = Field()
    name: str = Field()

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
    # quadrant:Quadrant = Field()
    # sector:Sector = Field()
    rating:int = Field(min=0, max=5)

# https://fastapi.tiangolo.com/it/tutorial/body-nested-models/#define-a-submodel
class UserCompetencies(BaseModel):
    # user:int    #orig
    user:User  # new
    competencies:list[Competency]
