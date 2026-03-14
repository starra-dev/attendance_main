from typing import Annotated

from fastapi import FastAPI,Depends,HTTPException,Request ,status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError

from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException
import jwt

import app.models as models
from app.database import engine , Base , get_db
from app.router import checkins, users
from app.schema import CheckLogResponse,ChecklogCreate, UserCreate ,UserPublic,UserPrivate,UserUpdate
 
Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="template")

app.include_router(users.router , prefix="/api/users", tags=[users])
app.include_router(checkins.router , prefix="/api/checkin", tags=[checkins])

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="media"), name="media")


 