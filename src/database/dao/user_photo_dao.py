from datetime import datetime
from typing import Sequence

from sqlmodel import Session, select

from database.models.user_photos import UserPhotoDb
from enums.user_enum import UserImageEnum
from models.errors.database_error import DatabaseException


class UserPhotoDao:

    @staticmethod
    def create_user_photo(session: Session, current_time: datetime, image: bytes, type: UserImageEnum, user_id: int):
        try:
            user_photo_db = UserPhotoDb(user_id=user_id, photo=image, type=type, created_at=current_time)
            session.add(user_photo_db)
            session.flush([user_photo_db])
            return user_photo_db
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")

    @staticmethod
    def get_user_photos(session: Session, user_id: int) -> Sequence[UserPhotoDb]:
        try:
            photos = (
                session.exec(
                    select(UserPhotoDb).where(UserPhotoDb.user_id == user_id)
                )).all()
            if photos is None:
                raise DatabaseException(http_status_code=204, error_message=f"No photos found for user {user_id}")
            return photos
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")

    @staticmethod
    def get_user_photos_for_analisys(session: Session, user_id: int) -> Sequence[UserPhotoDb]:
        try:
            photos = (
                session.exec(
                    select(UserPhotoDb).where(UserPhotoDb.user_id == user_id,
                                              UserPhotoDb.type == UserImageEnum.ANALYSIS)
                )).all()
            if photos is None:
                raise DatabaseException(http_status_code=204, error_message=f"No photos found for user {user_id}")
            return photos
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")

    @staticmethod
    def save_bulk_user_photos(session: Session, photos_db: Sequence[UserPhotoDb]) -> Sequence[
        UserPhotoDb]:
        try:
            session.bulk_save_objects(photos_db, return_defaults=True)
            for photo in photos_db:
                if photo.id is None:
                    raise DatabaseException(http_status_code=500, error_message=f"Error saving photo {photo.type}")
            return photos_db
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")
