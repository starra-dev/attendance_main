from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload ,Session
from sqlalchemy import func


import app.models as models
from app.database import engine , Base , get_db
from app.schema import CheckLogResponse,ChecklogCreate
from app.auth import CurrentUser


router = APIRouter()




@router.post ("", response_model=CheckLogResponse, status_code = status.HTTP_201_CREATED)
def check_in(checkin:ChecklogCreate, current_user: CurrentUser, db: Annotated[Session , Depends(get_db)]):

    user_result = db.execute(select(models.User).where(models.User.id == checkin.user_id))
    user = user_result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if already checked in on this date
    existing_result = db.execute(
        select(models.Checkin).where(
            models.Checkin.user_id == current_user.user_id,
            func.date(models.Checkin.timestamp) == checkin.date
        )
    )
    existing_log = existing_result.scalars().first()
    if existing_log:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="User already checked in on this date"
        )
    
    new_checkin = models.Checkin(
        user_id=current_user.user_id,
        action=checkin.action
    )
    db.add(new_checkin)
    db.commit()
    db.refresh(new_checkin)

    return CheckLogResponse(
        username= user.username,
        user_id= new_checkin.user_id,
        timestamp= new_checkin.timestamp,
        action= new_checkin.action
    )

    
@router.get ("/{user_id}/checkin", response_model=list[CheckLogResponse])
def get_user_log(user_id:int,current_user:CurrentUser, db: Annotated[Session , Depends(get_db)]):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not permitted"
        )
    user_result = db.execute(select(models.User).where(models.User.id == user_id).options(selectinload(models.User.checkins)))
    user = user_result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    logs = []
    for checkin in user.checkins:
        logs.append(CheckLogResponse(
            username= user.username,
            user_id= checkin.user_id,
            timestamp= checkin.timestamp,
            action= checkin.action
        ))
    return logs
