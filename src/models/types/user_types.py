from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from enums.user_codes_enum import UserCodeCategoryEnum
from enums.user_enum import UserImageEnum


class UserCodeType(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    code: Optional[str]
    category: UserCodeCategoryEnum

class UserPhotoType(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    photo: List[List[int]]
    type: UserImageEnum = UserImageEnum.PROFILE
    created_at: Optional[datetime] = None
