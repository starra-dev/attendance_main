from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload ,Session


import app.models as models
from app.database import engine , Base , get_db
from app.schema import CheckLogResponse,ChecklogCreate


router = APIRouter()




@router.post ("", response_model=CheckLogResponse, status_code = status.HTTP_201_CREATED)
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

    
@router.get ("/api/checkin/{user_id}/checkins", response_model=list[CheckLogResponse])
def get_user_log(user_id:int, db: Annotated[Session , Depends(get_db)]):
    # verify that the user exists before fetching logs
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    logs = user.checkins
    return logs