from typing import Dict, Any

from deepface import DeepFace
from numpy import ndarray
from sqlmodel import Session

from database.dao.photo_embedding_dao import PhotoEmbeddingDao
from database.dao.user_dao import UserDao
from database.models.users import UserDb
from models.errors.custom_error_with_object import HandledException
from models.errors.database_error import DatabaseException
from models.requests.face_models import FaceImagePayloadModel
from services.image_service import ImageService


class FaceService:
    DETECTOR = "yunet"
    MODEL_NAME = "Facenet"
    MAX_IMAGE_WIDTH = 720
    MAX_IMAGE_HEIGHT = 720

    @staticmethod
    def represent_face(img_bytes: ndarray) -> Dict[str, Any]:
        """
        Represent facial images as multidimensional vector embeddings.

        Args:
           img_bytes (np.ndarray): a numpy array in BGR format.
               If the source image contains multiple faces, the result will
               include information for the first detected person only.

        Returns:
           results (Dict[str, Any]): A dictionary, containing the following fields:

           - embedding (np.array): Multidimensional vector representing facial features.
               The number of dimensions varies based on the reference model
               (e.g., FaceNet returns 128 dimensions, VGG-Face returns 4096 dimensions).

           - facial_area (dict): Detected facial area by face detection in dictionary format.
               Contains 'x' and 'y' as the left-corner point, and 'w' and 'h'
               as the width and height. If `detector_backend` is set to 'skip', it represents
               the full image area and is nonsensical.

           - face_confidence (float): Confidence score of face detection. If `detector_backend` is set
               to 'skip', the confidence will be 0 and is nonsensical.
        """
        face_representation = DeepFace.represent(
            img_path=img_bytes,
            detector_backend=FaceService.DETECTOR,
            enforce_detection=False,
            model_name=FaceService.MODEL_NAME,
        )
        return face_representation[0]

    @staticmethod
    def get_user_by_image(session: Session, image: FaceImagePayloadModel) -> UserDb:
        ## TODO: Almacenar los embeding, no se estan guardando
        np_image = ImageService.convert_list_to_numpy_array(image.photo)
        representation = FaceService.represent_face(np_image)

        try:
            user_representation_db = (
                PhotoEmbeddingDao.get_distance_squared_from_photo_embeddings(
                    session, representation["embedding"]
                )
            )
        except DatabaseException as e:
            if e.http_status_code == 204:
                raise HandledException(error=e, details=representation)
        except Exception as e:
            raise e

        user_db = UserDao.get_user(session, user_representation_db.user_id)
        return user_db
