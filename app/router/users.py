from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload ,Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, UTC, timedelta
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import app.models as models
from config import settings
from app.database import engine , Base , get_db
from app.schema import  UserCreate ,UserPublic,UserPrivate,UserUpdate, Token
from app.auth import CurrentUser, verify_password,create_access_token,hash_password


router = APIRouter()


templates= Jinja2Templates(directory="template")


@router.post("/register",
               response_model=UserPrivate,
                 status_code = status.HTTP_201_CREATED)
def create_user(user:UserCreate, db: Annotated[Session , Depends(get_db)]):

    result = db.execute (   select(models.User) .where(func.lower(models.User.username) == user.username.lower()))
    existing_user = result.scalars().first()
    result = db.execute (   select(models.User) .where(func.lower(models.User.email) == user.email.lower()))
    existing_email = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    if existing_email:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    new_user = models.User(
        name = user.name,
        username = user.username,
        email = user.email.lower(),
        passwordhash = hash_password(user.password),

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#Login user endpoint
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
    db:Annotated[Session, Depends(get_db)],
):
     result = db.execute(
         select(models.User).where(
             func.lower(models.User.email) == form_data.username.lower()),
     )
     user = result.scalars().first()

     if not user or not verify_password(form_data.password, user.passwordhash):
         raise HTTPException(
             status_code= status.HTTP_401_UNAUTHORIZED,
             detail="incorrect email or password"
         )
     

     access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
     access_token = create_access_token(
         data={"sub": str (user.id)},
         expires_delta=access_token_expires,
     )

     return Token(access_token=access_token, token_type="bearer")



@router.get("/me", response_model=UserPrivate)
def get_profile(current_user:CurrentUser
):
    return current_user

 

@router.put("/update", response_model=UserPrivate)
def update_user( user_id :int , user_update:UserUpdate,current_user:CurrentUser,db: Annotated[Session , Depends(get_db)]):
    if user_id != current_user.id:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Not Authorized"
        )

    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user_update.username is not None and user.username.lower() != user_update.username.lower():
     result = db.execute(select(models.User).where(func.lower(models.User.username) == user_update.username.lower()))
     existing_username = result.scalars().first()

     if existing_username :
         raise HTTPException (status_code= status.HTTP_400_BAD_REQUEST,
                              detail="Username Already in use")
         
    if user_update.email is not None and user.email.lower() != user_update.email.lower():
        result = db.execute(select(models.User).where(func.lower(models.User.email) == user_update.email.lower()))
        existing_email = result.scalars().first()

        if existing_email :
            raise HTTPException (status_code= status.HTTP_400_BAD_REQUEST,
                                detail="Email is Already registered")
        
    if user_update.username is not None:
        user.username =user_update.username
    if user_update.email is not None:
        user.email =user_update.email.lower()
    if user_update.image_file is not None:
        user.image_file =user_update.image_file
    if user_update.name is not None:
        user.name =user_update.name

    db.commit()
    db.refresh(user)
    return user




@router.delete ("/me/delete", status_code= status.HTTP_204_NO_CONTENT)
def delete_user_profile(current_user:CurrentUser, db: Annotated[Session , Depends(get_db)]):
       
    db.delete(current_user)
    db.commit()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")