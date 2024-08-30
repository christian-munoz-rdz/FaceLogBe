from datetime import datetime
from typing import List, Sequence, Tuple

from fastapi import HTTPException
from sqlmodel import Session

from database.dao.user_dao import UserDao
from database.dao.user_photo_dao import UserPhotoDao
from database.models.areas import AreaDb
from database.models.photo_embeddings import PhotoEmbeddingDb
from database.models.user_photos import UserPhotoDb
from database.models.users import UserDb
from enums.role_enum import RoleEnum
from enums.user_enum import UserImageEnum
from models.errors.database_error import DatabaseException
from models.requests.face_models import FaceImagePayloadModel
from models.requests.user_models import UserPayloadModel
from models.types.user_types import UserPhotoType
from services.face_service import FaceService
from services.image_service import ImageService


class UserService:

    @staticmethod
    def create_user_photos(
            session: Session,
            user_id: int,
            photos: List[UserPhotoType]
    ) -> List[UserPhotoDb]:
        current_time = datetime.now()
        photos_db = []
        # creation of blob photo objects
        for index, photo in enumerate(photos):
            if photo.photo and (not ImageService.is_valid_image(photo.photo)):
                raise HTTPException(status_code=400, detail=f"Invalid image in index {index}")
            image = ImageService.convert_to_binary(photo.photo)
            photos_db.append(
                UserPhotoDao.create_user_photo(session, current_time, image, photo.type, user_id)
            )
        return photos_db

    @staticmethod
    def create_user_photo_embeddings(
            photos: Sequence[UserPhotoDb]
    ) -> Sequence[PhotoEmbeddingDb]:
        photo_embeddings_db = []
        for index, photo_db in enumerate(photos):
            image = ImageService.convert_to_numpy_for_deepface(photo_db.photo) if photo_db.photo else None
            if image is None:
                raise HTTPException(status_code=400, detail=f"Invalid image in index {index}")
            face_embeddings = FaceService.represent_face(image)
            if (face_embeddings['face_confidence'] < 0.5):
                raise HTTPException(
                    status_code=400,
                    detail=f"Face confidence is less than 0.5 in image "
                           f"at index {index}, please send a better image."
                )
            for dimension, face_embedding in enumerate(face_embeddings['embedding']):
                photo_embeddings_db.append(
                    PhotoEmbeddingDb(
                        user_photo_id=photo_db.id,
                        dimension=dimension,
                        value=face_embedding
                    )
                )
        return photo_embeddings_db

    @staticmethod
    def get_user_by_image_or_create_default(session, image: FaceImagePayloadModel, area_db: AreaDb) -> Tuple[
        UserDb, UserPhotoDb
    ]:
        try:
            user_db = FaceService.get_user_by_image(session, image)
            photo = ImageService.convert_to_binary(image.photo)
            user_photo_db = UserPhotoDao.create_user_photo(session, datetime.now(), photo, UserImageEnum.RECORD,
                                                           user_db.id)
            return user_db, user_photo_db
        except DatabaseException as e:
            # not user found, create a new one
            current_timestamp = datetime.isoformat(datetime.now())
            max_area_name_length = 255 - len("YYYY-MM-DD HH:MM:SS.mmmmmm")
            area_name = area_db.name if len(area_db.name) <= max_area_name_length else area_db.name[
                                                                                       :max_area_name_length]
            user_name = f'{area_name}-{current_timestamp}'
            user_db = UserDao.create_user(session, UserPayloadModel(name=user_name, email=None, role_id=RoleEnum.NONE))
            photo = ImageService.convert_to_binary(image.photo)
            user_photo_db = UserPhotoDao.create_user_photo(session, datetime.now(), photo, UserImageEnum.RECORD,
                                                           user_db.id)
            return user_db, user_photo_db
