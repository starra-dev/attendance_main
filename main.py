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
from app.auth import oauth2_scheme, verify_access_token
 
Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="template")

app.include_router(users.router , prefix="/api/users", tags=["users"])
app.include_router(checkins.router , prefix="/api/checkin", tags=["checkins"])

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/")
def user_page(request: Request, token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.execute(select(models.User).where(models.User.id == user_id_int)).scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return templates.TemplateResponse("user.html", {"request": request, "user": user})

 