from pydantic import BaseModel
from enum import Enum
from tkinter import time



class Attendance(BaseModel):
    name:str
    id:int
    department:str
    checkin:bool
    timestamp:time
    


