from pydantic import BaseModel, ConfigDict,Field

class BookCreate(BaseModel):
    title:str = Field(min_length=1,max_length=100)
    author:str = Field(min_length=1,max_length=100)
    description:str = Field(min_length=1,max_length=200)
    rating:float = Field(ge=0.0,le=5.0)

class BookResponse(BaseModel):
    #  allows Pydantic to read data from ORM model attributes directly!
    model_config = ConfigDict(from_attributes=True) 
    id:int
    title:str
    author:str
    description:str
    rating:float
