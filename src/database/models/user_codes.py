from typing import Optional

from sqlmodel import Field, SQLModel

from enums.user_codes_enum import UserCodeCategoryEnum


class UserCodeDb(SQLModel, table=True):
    __tablename__ = "user_codes"
    id: Optional[int] = Field(primary_key=True)
    user_id: Optional[int] = Field(foreign_key="users.id")
    code: Optional[str]
    category: UserCodeCategoryEnum
