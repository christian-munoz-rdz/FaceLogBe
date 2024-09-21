from typing import Optional, List

from pydantic import BaseModel


class AreaUserType(BaseModel):
    id: Optional[int] = None
    area_id: Optional[int] = None
    user_id: Optional[int] = None
    user_type: str  # TODO: Define enum for this field


class AreaType(BaseModel):
    id: Optional[int]
    name: str
    description: str
    module: str
    classroom: str
    campus: str
    department: str
    division: str
    image: Optional[List[List[int]]]
