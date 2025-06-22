from pydantic import BaseModel, EmailStr, Field
# see https://fastapi.tiangolo.com/it/tutorial/extra-models/#multiple-models

class User(BaseModel):
    name: str = Field()
    username: str = Field()
    email: EmailStr = Field()

class Competency(BaseModel):
    ''' this maps to the compass quadrants and sectors, and the current rating for each '''
    user_id:int = Field()
    quadrant:int = Field(min=0, max=3)
    sector:int = Field(min=0, max=4)
    rating:int = Field(min=0, max=5)

# https://fastapi.tiangolo.com/it/tutorial/body-nested-models/#define-a-submodel
class UserCompetencies(BaseModel):
    user:int
    competencies:list[Competency]
