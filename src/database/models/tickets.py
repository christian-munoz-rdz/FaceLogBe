from datetime import datetime
from typing import Optional
from sqlmodel import Column, DateTime, Field, SQLModel, func


class TicketDb(SQLModel, table=True):
    __tablename__ = "tickets"
    id: Optional[int] = Field(primary_key=True)
    area_id: Optional[int] = Field(foreign_key="areas.id")
    created_by: Optional[int] = Field(foreign_key="users.id")
    title: str
    description: str
    status: str
    created_at: datetime = Field(sa_column=Column(DateTime, default=func.now()))
