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
from app.schema import  UserCreate ,UserPublic,CheckLogResponse,ChecklogCreate,UserPrivate
 
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="template")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="media"), name="media")


@app.post ("/api/register", response_model=UserPublic, status_code = status.HTTP_201_CREATED)
def create_user(user:UserCreate, db: Annotated[Session , Depends(get_db)]):
    result = db.execute (   select(models.User) .where(models.User.username == user.username))
    existing_user = result.scalars.first()

    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    result = db.execute (   select(models.User) .where(models.User.email== user.email))
    existing_email = result.scalars.first()

    if existing_email:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    new_user = models.User(
        name = user.name,
        username = user.username,
        email = user.email

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

      
@app.get ("/api/user/{user_id}", response_model=UserPublic)
def get_user(user_id: int, db: Annotated[Session , Depends(get_db)]):
    # query by the primary key field `id` and use the parameter directly
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if user:
        return user
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")



@app.post ("/api/checkin", response_model=CheckLogResponse, status_code = status.HTTP_201_CREATED)
def check_in(checkin:ChecklogCreate, db: Annotated[Session , Depends(get_db)]):
    # make sure schema includes user_id (add if missing)
    result = db.execute(select(models.Checkin).where(models.Checkin.user_id == checkin.user_id))
    existing_log = result.scalars().first()

    if existing_log:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="User already checked in"
        )
    new_checkin = models.Checkin(
        user_id=checkin.user_id,
        action=checkin.action,
        Date=checkin.date  # if you intend to store the provided date
    )
    db.add(new_checkin)
    db.commit()
    db.refresh(new_checkin)

    return new_checkin

    
@app.get ("/api/checkin/{user_id}/checkins", response_model=list[CheckLogResponse])
def get_user_log(user_id:int, db: Annotated[Session , Depends(get_db)]):
    # verify that the user exists before fetching logs
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    result = db.execute(select(models.Checkin).where(models.Checkin.user_id == user_id))
    logs = result.scalars().all()
    return logs

 