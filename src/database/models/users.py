from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Column, DateTime, func


class UserDb(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(index=True)
    email: Optional[str] = Field(index=True, unique=True)
    role_id: int = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=func.now()))
