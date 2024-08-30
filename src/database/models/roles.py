from typing import Optional
from sqlmodel import Field, SQLModel


class RoleDb(SQLModel, table=True):
    __tablename__ = "roles"
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str
    description: str = Field(index=True)
