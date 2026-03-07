import sqlite3
from app.models import Profile
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
conn = sqlite3.connect("attendance.db")
template = Jinja2Templates(directory="/template/register.html")
cur = conn.cursor()
DATABASE_URL = "attendance.db"



#JWT_TOKEN=jwt-token-loggoogle-access

@app.post("/register")
def save_profile():
    create_profile = cur.execute('''CREATE TABLE IF NOT EXISTS Profile
       name text,        
       email text,
       password text        
                ''')
        conn.commit()
    return



@app.post("")
def login():
    #statement
    return ""


def validatePassword():
    return ""
context = {"request": request, 
           "title": "Home Page", 
           "message": "Welcome to FastAPI HTML!"}