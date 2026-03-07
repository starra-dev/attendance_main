from fastapi import FastAPI, Request,Query
from datetime import datetime,date,time
from fastapi.responses import HTMLResponse
from app.models import Status
from app.models import Record
import sqlite3
from fastapi.templating import Jinja2Templates


   


