from typing import Annotated

from fastapi import FastAPI,Depends,HTTPException,Request ,status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError

from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPEception

import app.models as models
from app.database import engine , Base , get_db
from app.router import checkin, users
from app.schema import CheckLogResponse,ChecklogCreate, UserCreate ,UserPublic,UserPrivate,UserUpdate
 
Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="template")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="media"), name="media")


 