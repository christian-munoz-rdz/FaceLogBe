from datetime import datetime
from typing import Optional
from sqlmodel import Column, DateTime, Field, SQLModel, func


class TimeRecordDb(SQLModel, table=True):
    __tablename__ = "time_records"
    id: Optional[int] = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    area_id: int = Field(foreign_key="areas.id")
    enter_photo_id: int = Field(foreign_key="user_photos.id")
    exit_photo_id: Optional[int] = Field(foreign_key="user_photos.id")
    created_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=func.now()))
    entered_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=func.now()))
    exited_at: Optional[datetime] = Field()
