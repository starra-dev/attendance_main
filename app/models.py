from __future__ import annotations

from datetime import datetime, UTC ,date 
from sqlalchemy import ForeignKey,DateTime,Integer,String,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship

from database import Base


class User(Base):
    __tablename__ = "user"

    id : Mapped[int] = mapped_column(Integer,primary_key=True , index=True)
    name:Mapped[str] = mapped_column (String(50) , nullable=False)
    username:Mapped[str] = mapped_column (String(50), unique=True , nullable=False)
    email: Mapped[str] = mapped_column (String(120), unique=True , nullable=False)
    image_file : Mapped[str | None] = mapped_column( String(200),
        nullable=True,
        default=None
    )  
    checkin: Mapped[Checkin] = mapped_column (bool, unique=True , nullable=False) 

    def image_path(self)-> str:
        if self.image_file:
            return f"/media/profile/pic{self.image_file}"
        return "/static/profile_pic/default.jpg"
    
class Checkin(Base):
    __tablename__ = "checkin"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
     # Data Change Tracking
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True , index=True)
    # Audit Fields
    Date: Mapped[date] = mapped_column(date , date.now(),) # TRYING TO ADD A DATE FUNCTION HERE
    timestamp:Mapped[datetime] = mapped_column(DateTime (timezone=True), default=lambda: datetime.now(),)
    action: Mapped[bool] = mapped_column(bool, default=False nullable=False) # E.g., 'INSERT', 'UPDATE'
   


