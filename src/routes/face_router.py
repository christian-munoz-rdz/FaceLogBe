from typing import List

from fastapi import APIRouter, Depends, Body
from sqlmodel import Session
from typing_extensions import Annotated

from controllers.face_controller import (FaceController)
from database.services.database import Database
from models.requests.face_models import FaceDescriptorResponseModel, FaceImagePayloadModel
from models.requests.http_models import HttpErrorResponseModel
from models.requests.user_models import UserResponseModel


class FaceRouter:
    router = APIRouter(prefix="/face", tags=["face"])

    @staticmethod
    @router.post("/find-user",
                 responses={200: {"model": UserResponseModel}, 204: {}, 400: {"model": HttpErrorResponseModel}})
    async def find_user(*, session: Session = Depends(Database.get_session),
                        body: Annotated[FaceImagePayloadModel,
                        Body(
                            embed=False,
                            example={
                                "image": [
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0]
                                ]
                            })]
                        ) -> UserResponseModel:
        return FaceController.find_user(session, body)

    @staticmethod
    @router.post("/describe-for-test",
                 responses={
                     200: {
                         "model": List[FaceDescriptorResponseModel],
                         "content": {
                             "application/json": {
                                 "example": {
                                     "embedding": [0.1, 0.2, 0.3],
                                     "facial_area": {
                                         "x": 60,
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
                         },
                     },
                     201: {
                         "model": List[FaceDescriptorResponseModel],
                         "content": {
                             "application/json": {
                                 "example": {
                                     "embedding": [0.1, 0.2, 0.3],
                                     "facial_area": {
                                         "x": 60,
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
                         },
                     },
                     400: {"model": HttpErrorResponseModel}})
    async def describe_face_for_testing(*, session: Session = Depends(Database.get_session),
                                        user_id: int) -> List[FaceDescriptorResponseModel]:
        return FaceController.describe_face_for_testing(session, user_id)
