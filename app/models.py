from __future__ import annotations

from datetime import datetime, UTC ,date 
from sqlalchemy import ForeignKey,DateTime,Integer,String,Text,Boolean
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id : Mapped[int] = mapped_column(Integer,primary_key=True , index=True)
    name:Mapped[str] = mapped_column (String(50) , nullable=False)
    username:Mapped[str] = mapped_column (String(50), unique=True , nullable=False)
    email: Mapped[str] = mapped_column (String(120), unique=True , nullable=False)
    passwordhash : Mapped[str] = mapped_column(String(200) , nullable=False)
    image_file : Mapped[str | None] = mapped_column( String(200),
        nullable=True,
        default=None
    )  
    checkins: Mapped[list["Checkin"]] = relationship("Checkin", back_populates="user" ,cascade="all, delete-orphan")

    @property
    def image_path(self)-> str:
        if self.image_file:
            return f"/media/profile_pic/{self.image_file}"
        return "/static/profile_pic/default.jpg"
    
class Checkin(Base):
    __tablename__ = "checkin"


    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True, index=True)
    timestamp:Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(UTC),)
    action: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="checkins")
   


