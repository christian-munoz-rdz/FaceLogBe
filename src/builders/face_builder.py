from typing import Any, Dict

from models.requests.face_models import FaceDescriptorResponseModel


class FaceBuilder:

    @staticmethod
    def build_face_descriptor(face_descriptor: Dict[str, Any]) -> FaceDescriptorResponseModel:
        return FaceDescriptorResponseModel(
            embedding=face_descriptor["embedding"],
            facial_area=face_descriptor["facial_area"],
            face_confidence=face_descriptor["face_confidence"]
        )