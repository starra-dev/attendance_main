from datetime import datetime,date,UTC
from pydantic import BaseModel , ConfigDict , Field , EmailStr


class UserBase(BaseModel):
    username: str = Field(min_length=1 , max_length=50)
    email : EmailStr = Field(max_length=120)
   
class UserCreate(UserBase):
    name : str = Field(min_length=1 , max_length=50)
    password : str = Field(min_length=8 )


class UserPublic(BaseModel):
    model_config =ConfigDict(from_attributes=True)
    name :str
    id : int
    image_file : str | None
    image_path : str

class UserPrivate(UserPublic):
    email: EmailStr
    
class UserUpdate(BaseModel):
    name :str| None = Field( default=None ,min_length=1 , max_length=50)
    username: str| None = Field( default=None ,min_length=1 , max_length=50)
    email : EmailStr |None = Field( default=None ,max_length=120)
    image_file : str | None = Field( default=None , min_length=1,max_length=200)


class Token(BaseModel):
    access_token :str
    token_type:str

    
class  CheckLogBase(BaseModel):

    username: str


class ChecklogCreate(CheckLogBase):
    user_id: int                   # identifier of the user performing the checkin
    date: date
    timezone: datetime
    action: bool

class CheckLogResponse(CheckLogBase):
    model_config =ConfigDict(from_attributes=True)
    
    user_id: int 
    date: date