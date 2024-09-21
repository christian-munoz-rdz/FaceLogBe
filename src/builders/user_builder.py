from typing import Sequence

from database.models.area_users import AreaUserDb
from database.models.areas import AreaDb
from database.models.user_codes import UserCodeDb
from database.models.user_photos import UserPhotoDb
from database.models.users import UserDb
from enums.role_enum import RoleEnum
from enums.user_enum import UserImageEnum
from models.requests.user_models import UserWithImageResponseModel, UserResponseModel
from models.types.area_types import AreaType
from models.types.user_types import UserCodeType, UserPhotoType
from services.image_service import ImageService


class UserBuilder:

    @staticmethod
    def build_user_response(
            user: UserDb, codes: Sequence[UserCodeDb], areas: Sequence[AreaDb],
    ) -> UserResponseModel:
        return UserResponseModel(
            id=user.id,
            name=user.name,
            role_id=RoleEnum(user.role_id),
            email=user.email,
            created_at=user.created_at,
            codes=[
                UserCodeType(
                    code=code.code, user_id=user.id, id=code.id, category=code.category
                )
                for code in codes
            ],
            areas=[
                AreaType(
                    id=area_db.id,
                    name=area_db.name,
                    description=area_db.description,
                    module=area_db.module,
                    classroom=area_db.classroom,
                    campus=area_db.campus,
                    department=area_db.department,
                    division=area_db.division,
                    image=ImageService.convert_to_array(area_db.image) if area_db.image else None,
                )
                for area_db in areas
            ],
        )

    @staticmethod
    def build_user_with_image_response(
            user: UserDb, areas: Sequence[AreaDb], codes: Sequence[UserCodeDb], photos: Sequence[UserPhotoDb]
    ) -> UserWithImageResponseModel:
        return UserWithImageResponseModel(
            id=user.id,
            name=user.name,
            role_id=RoleEnum(user.role_id),
            email=user.email,
            created_at=user.created_at,
            codes=[
                UserCodeType(
                    code=code.code, user_id=user.id, id=code.id, category=code.category
                )
                for code in codes
            ],
            areas=[
                AreaType(
                    id=area_db.id,
                    name=area_db.name,
                    description=area_db.description,
                    module=area_db.module,
                    classroom=area_db.classroom,
                    campus=area_db.campus,
                    department=area_db.department,
                    division=area_db.division,
                    image=ImageService.convert_to_array(area_db.image) if area_db.image else None,
                )
                for area_db in areas
            ],
            photos=[
                UserPhotoType(
                    id=photo.id,
                    user_id=user.id,
                    type=UserImageEnum(photo.type),
                    photo=ImageService.convert_to_array(photo.photo),
                    created_at=photo.created_at,
                )
                for photo in photos
            ],
        )
