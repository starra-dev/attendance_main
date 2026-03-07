from fastapi import FastAPI, Request,Query
from datetime import datetime,date,time
from fastapi.responses import HTMLResponse
from app.models import Status
from app.models import Record
import sqlite3
from fastapi.templating import Jinja2Templates


app = FastAPI()
con = sqlite3.connect("attendance.db")
templates = Jinja2Templates(directory="/template/record.html")


# Status configuration
time = datetime.now()
@app.get("/status")
def get_status():
    if time.hour == Status:
     return Status

#searchbar backend 
@app.get("/",response_class=HTMLResponse)
def read_input(request: Request):
   return templates.TemplateResponse("record.html",{"request": request})
   


