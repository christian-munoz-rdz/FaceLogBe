from typing import List

from pydantic import BaseModel


class FaceImagePayloadModel(BaseModel):
    photo: List[List[int]]

    model_config = {
        "json_schema_extra": {
            "example": {
                "photo": [
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ]
            }
        }
    }


class FaceDescriptorResponseModel(BaseModel):
    embedding: List[float]
    facial_area: dict
    face_confidence: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "embedding": [0.1, 0.2, 0.3],
                "facial_area": {"x": 60,
                                "y": 28,
                                "w": 77,
                                "h": 111,
                                "left_eye": [
                                    74,
                                    71
                                ],
                                "right_eye": [
                                    109,
                                    72
                                ]},
                "face_confidence": "0.91"
            }
        }
    }
