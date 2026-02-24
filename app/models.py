from enum import Enum
from pydantic import BaseModel
from datetime import datetime,date,time

class Status(Enum):
    EARLY =  time <= 9,
    LATE = time > 9


class Record(BaseModel):
    name: str
    date: date
    status: Status


class Profile(BaseModel):
    name: str
    email : str
    password: str





