from typing import List

from sqlmodel import Session

from builders.face_builder import FaceBuilder
from builders.user_builder import UserBuilder
from database.dao.user_code_dao import UserCodeDao
from database.dao.user_photo_dao import UserPhotoDao
from models.errors.database_error import DatabaseException
from models.requests.face_models import (
    FaceDescriptorResponseModel,
    FaceImagePayloadModel,
)
from models.requests.user_models import UserResponseModel
from services.face_service import FaceService
from services.image_service import ImageService


class FaceController:
    DETECTOR = "yunet"
    MODEL_NAME = "Facenet"

    @staticmethod
    def find_user(session: Session, image: FaceImagePayloadModel) -> UserResponseModel:
        try:
            user_db = FaceService.get_user_by_image(session, image)
            user_codes = []
            try:
                user_codes = UserCodeDao.get_all_user_codes(session, user_db.id)
            except DatabaseException as e:
                if e.http_status_code == 204:
                    user_codes = []
                raise e
            session.commit()
            return UserBuilder.build_user_response(user_db, user_codes)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(
                http_status_code=500, error_message=f"Database error: {str(e)}"
            )

    @staticmethod
    def describe_face_for_testing(
            session: Session, user_id: int
    ) -> List[FaceDescriptorResponseModel]:
        try:
            user_images = UserPhotoDao.get_user_photos_for_analisys(session, user_id)

            faces_detected = []
            for user_image in user_images:
                np_image = ImageService.convert_to_numpy_for_deepface(user_image.photo)
                representation = FaceService.represent_face(np_image)
                faces_detected.append(FaceBuilder.build_face_descriptor(representation))

            session.commit()
            return faces_detected
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(
                http_status_code=500, error_message=f"Database error: {str(e)}"
            )
