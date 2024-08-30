from datetime import datetime
from typing import Optional
from sqlmodel import Column, DateTime, Field, SQLModel


class UserPhotoDb(SQLModel, table=True):
    __tablename__ = "user_photos"
    id: Optional[int] = Field(primary_key=True)
    user_id: Optional[int] = Field(foreign_key="users.id")
    photo: bytes
    type: str
    created_at: datetime = Field(sa_column=Column(DateTime, default=datetime.now()))
