from typing import Optional
from sqlmodel import Field, SQLModel


class AreaUserDb(SQLModel, table=True):
    __tablename__ = "area_users"
    id: Optional[int] = Field(primary_key=True)
    area_id: Optional[int] = Field(foreign_key="areas.id")
    user_id: Optional[int] = Field(foreign_key="users.id")
    user_type: str
