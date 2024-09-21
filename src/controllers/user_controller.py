from datetime import datetime
from typing import Sequence

from fastapi import HTTPException
from sqlmodel import Session

from builders.user_builder import UserBuilder
from database.dao.area_dao import AreaDao
from database.dao.photo_embedding_dao import PhotoEmbeddingDao
from database.dao.user_code_dao import UserCodeDao
from database.dao.user_dao import UserDao
from database.dao.user_photo_dao import UserPhotoDao
from enums.time_record_enum import TimeRecordActionEnum
from enums.user_enum import UserImageEnum
from models.errors.database_error import DatabaseException
from models.requests.face_models import FaceImagePayloadModel
from models.requests.user_models import (
    UserPayloadModel,
    UserImagePayloadModel,
    UserWithImageResponseModel,
    UserResponseModel,
    UserLogTimePayloadModel,
)
from models.types.user_types import UserPhotoType
from services.image_service import ImageService
from services.time_record_service import TimeRecordService
from services.user_service import UserService


class UserController:

    @staticmethod
    def create_new_user(session: Session, user: UserPayloadModel) -> UserResponseModel:
        try:
            user_db = UserDao.create_user(session, user)
            codes_db = UserCodeDao.create_bulk_user_codes(session, user_db, user.codes)
            area_users_db = UserDao.create_area_users(session, user_db.id, [area.area_id for area in user.areas])
            session.commit()
            return UserBuilder.build_user_response(user_db, codes_db, area_users_db)
        except DatabaseException as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=e.http_status_code, detail=e.error_message)
        except Exception as e:
            print(e)
            session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Something went wrong: {str(e)}"
            )

    @staticmethod
    def get_all_users(session: Session) -> Sequence[UserResponseModel]:
        try:
            users_db = UserDao.get_all(session)
            user_responses = []
            for user_db in users_db:
                codes = []
                areas = []
                try:
                    codes = UserCodeDao.get_all_user_codes(session, user_db.id)
                    areas = AreaDao.get_user_areas(session, user_db.id)
                except DatabaseException as e:
                    if e.http_status_code == 204:
                        codes = []
                    raise e
                user_responses.append(UserBuilder.build_user_response(user_db, codes, areas))
            session.commit()
            return user_responses
        except DatabaseException as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=e.http_status_code, detail=e.error_message)
        except Exception as e:
            print(e)
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Something went wrong: {str(e)}"
            )

    @staticmethod
    def get_user_with_images(
            session: Session, user_id: int
    ) -> UserWithImageResponseModel:
        try:
            user_db = UserDao.get_user(session, user_id)
            user_photos = []
            user_codes = []
            user_areas = []
            try:
                user_photos = UserPhotoDao.get_user_photos(session, user_id)
            except DatabaseException as e:
                if e.http_status_code == 204:
                    user_photos = []
            except Exception as e:
                raise e

            try:
                user_codes = UserCodeDao.get_all_user_codes(session, user_db.id)
            except DatabaseException as e:
                if e.http_status_code == 204:
                    user_codes = []
            except Exception as e:
                raise e

            try:
                user_areas = AreaDao.get_user_areas(session, user_db.id)
            except DatabaseException as e:
                if e.http_status_code == 204:
                    user_areas = []
            except Exception as e:
                raise e

            response = UserBuilder.build_user_with_image_response(
                user_db, user_areas, user_codes, user_photos
            )
            session.commit()
            return response
        except DatabaseException as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=e.http_status_code, detail=e.error_message)
        except Exception as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    @staticmethod
    def create_images_for_user(
            session: Session, user_id: int, body: UserImagePayloadModel
    ) -> UserWithImageResponseModel:
        try:
            if len(body.photos) == 0:
                raise HTTPException(
                    status_code=400, detail="You must send valid images."
                )
            user_db = UserDao.get_user(session, user_id)
            user_codes_db = []
            try:
                user_codes_db = UserCodeDao.get_all_user_codes(session, user_db.id)
            except DatabaseException as e:
                if e.http_status_code == 204:
                    user_codes_db = []
                raise e
            photos_db = UserService.create_user_photos(session, user_id, body.photos)
            photos_db = UserPhotoDao.save_bulk_user_photos(session, photos_db)
            photo_embeddings_db = UserService.create_user_photo_embeddings(photos_db)
            PhotoEmbeddingDao.save_bulk_photo_embeddings(session, photo_embeddings_db)
            # response builder step
            images = []
            for photo in photos_db:
                images.append(
                    UserPhotoType(
                        id=photo.id,
                        user_id=user_db.id,
                        type=UserImageEnum(photo.type),
                        photo=ImageService.convert_to_array(photo.photo),
                        created_at=photo.created_at,
                    )
                )

            response = UserBuilder.build_user_with_image_response(
                user_db, user_codes_db, photos_db
            )
            session.commit()
            return response
        except DatabaseException as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=e.http_status_code, detail=e.error_message)
        except HTTPException as e:
            print(e)
            session.rollback()
            raise e
        except Exception as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=400, detail=f"Invalid image. {str(e)}")

    @staticmethod
    def create_user_time_record(
            session: Session, body: UserLogTimePayloadModel
    ) -> UserWithImageResponseModel:
        try:
            current_time = datetime.now()
            image = FaceImagePayloadModel(photo=body.photo)
            area_db = AreaDao.get_area_by_id(session, body.area_id)
            user_db, user_photo_db = UserService.get_user_by_image_or_create_default(
                session, image, area_db
            )

            time_record_db = TimeRecordService.create_time_record(
                session, TimeRecordActionEnum(body.action), user_db, area_db, user_photo_db, current_time
            )

            user_codes_db = UserCodeDao.get_all_user_codes(session, user_db.id)
            areas_db = AreaDao.get_user_areas(session, user_db.id)

            response = UserBuilder.build_user_with_image_response(
                user_db, areas_db, user_codes_db, [user_photo_db]
            )

            session.commit()
            return response
        except DatabaseException as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=e.http_status_code, detail=e.error_message)
        except Exception as e:
            print(e)
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Invalid time record. {str(e)}"
            )
