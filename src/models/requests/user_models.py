from datetime import datetime
from typing import Union, List, Optional

from pydantic import BaseModel

from enums.role_enum import RoleEnum
from enums.time_record_enum import TimeRecordActionEnum
from models.types.area_types import AreaUserType, AreaType
from models.types.user_types import UserCodeType, UserPhotoType


class UserPayloadModel(BaseModel):
    name: str
    role_id: RoleEnum
    email: Optional[str]
    codes: List[UserCodeType]
    areas: List[AreaUserType]

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Juan Perez",
                "role_id": 4,
                "email": "juanito123@test.com",
                "codes": [
                    {
                        "code": "0000000000",
                        "category": "STUDENT"
                    }
                ],
                "areas": [
                    {
                        "area_id": 1
                    }
                ]
            }
        }
    }


class UserImagePayloadModel(BaseModel):
    photos: List[UserPhotoType]

    model_config = {
        "json_schema_extra": {
            "example": {
                "photos": [
                    {
                        "type": "PROFILE",
                        "photo": [
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]
                        ]
                    },
                    {
                        "type": "ANALYSIS",
                        "photo": [
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]
                        ]
                    }
                ]
            }
        }
    }


class UserResponseModel(BaseModel):
    id: int
    name: str
    role_id: RoleEnum
    email: Union[str, None]
    created_at: datetime
    codes: List[UserCodeType]
    areas: List[AreaType]

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Juan Perez",
                "role_id": 4,
                "email": "juanito123@test.com",
                "created_at": "2021-09-07T00:00:00",
                "codes": [
                    {
                        "id": 1,
                        "user_id": 1,
                        "code": "0000000000",
                        "category": "STUDENT"
                    }
                ],
                "areas": [
                    {
                        "id": 1,
                        "name": "iLabTDI",
                        "description": "La mejor area de todas claro que si",
                        "module": "N",
                        "classroom": "001",
                        "campus": "CUCEI",
                        "department": "Ingenierias",
                        "division": "DIVEC",
                    }
                ]
            }
        }
    }


class UserWithImageResponseModel(UserResponseModel):
    photos: List[UserPhotoType]

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Juan Perez",
                "role_id": 4,
                "email": "juanito123@test.com",
                "created_at": "2021-09-07T00:00:00",
                "codes": [
                    {
                        "id": 1,
                        "user_id": 1,
                        "code": "0000000000",
                        "category": "STUDENT"
                    }
                ],
                "photos": [
                    {
                        "id": 1,
                        "type": "PROFILE",
                        "photo": [
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]
                        ]
                    }
                ]
            }
        }
    }


class UserLogTimeResponseModel(BaseModel):
    id: int
    name: str
    role_id: RoleEnum
    email: Union[str, None]
    created_at: datetime
    time_record: datetime
    action: TimeRecordActionEnum
    photo: List[List[int]]
    area_id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Juan Perez",
                "role_id": 4,
                "email": "juanito1234@test.com",
                "created_at": "2021-09-07T00:00:00",
                "time_record": "2021-09-07T00:00:00",
                "action": "ENTER",
                "photo": [
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ]
            }
        }
    }


class UserLogTimePayloadModel(BaseModel):
    area_id: int
    action: str
    photo: List[List[int]]

    model_config = {
        "json_schema_extra": {
            "example": {
                "area_id": 1,
                "action": "ENTER",
                "photo": [
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ]
            }
        }
    }
