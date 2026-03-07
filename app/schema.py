from datetime import datetime,date,UTC
from pydantic import BaseModel , ConfigDict , Field , EmailStr


class UserBase(BaseModel):
    username: str = Field(min_length=1 , max_length=50)
    email : EmailStr = Field(max_length=120)
   
class UserCreate(UserBase):
    name : str = Field(min_length=1 , max_length=50)


class UserResponse(UserBase):
    model_config =ConfigDict(from_attributes=True)
    name :str
    id : int
    checkin: str
    image_file : str | None
    image_path : str


class CheckLogBase(BaseModel):
    username : str


class ChecklogCreate(CheckLogBase):
    date: date
    timezone: datetime
    action:bool

class CheckLogResponse(CheckLogBase):
    model_config =ConfigDict(from_attributes=True)
    
    
    user_id : int
    date : datetime
