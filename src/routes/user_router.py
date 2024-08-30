from typing import Sequence

from fastapi import APIRouter, Depends, Body, Response, status
from sqlmodel import Session
from typing_extensions import Annotated

from controllers.user_controller import UserController
from database.services.database import Database
from models.requests.http_models import HttpErrorResponseModel
from models.requests.user_models import UserResponseModel, UserPayloadModel, UserImagePayloadModel, \
    UserWithImageResponseModel, UserLogTimePayloadModel


class UserRouter:
    router = APIRouter(prefix="/user", tags=["user"])

    @staticmethod
    @router.post("/",
                 status_code=status.HTTP_201_CREATED,
                 name="Create new user",
                 responses={
                     201: {"model": UserResponseModel},
                     400: {"model": HttpErrorResponseModel}
                 })
    async def create_user(
            *,
            session: Session = Depends(Database.get_session),
            body: Annotated[UserPayloadModel, Body()],
            response: Response
    ) -> UserResponseModel:
        created_user = UserController.create_new_user(session, body)
        response.status_code = status.HTTP_201_CREATED
        return created_user

    @staticmethod
    @router.get("/",
                responses={
                    200: {"model": Sequence[UserResponseModel]},
                    400: {"model": HttpErrorResponseModel}
                })
    async def get_list_of_users(
            *,
            session: Session = Depends(Database.get_session)
    ) -> Sequence[UserResponseModel]:
        return UserController.get_all_users(session)

    @staticmethod
    @router.get("/{user_id}",
                responses={200: {"model": UserWithImageResponseModel}, 400: {"model": HttpErrorResponseModel}})
    async def get_user_by_id(
            *, session: Session = Depends(Database.get_session), user_id: int
    ) -> UserWithImageResponseModel:
        return UserController.get_user_with_images(session, user_id)

    @staticmethod
    @router.post("/{user_id}/image",
                 responses={201: {"model": UserWithImageResponseModel}, 400: {"model": HttpErrorResponseModel}})
    async def create_images_for_user(
            *, session: Session = Depends(Database.get_session),
            user_id: int,
            body: Annotated[UserImagePayloadModel, Body(embed=False)]
    ) -> UserWithImageResponseModel:
        return UserController.create_images_for_user(session, user_id, body)

    @staticmethod
    @router.post("/log-time",
                 responses=
                 {
                     200: {
                         "model": UserWithImageResponseModel,
                         "description": "User time record created or updated successfully, depending on the action"
                     },
                     201: {
                         "model": UserWithImageResponseModel,
                         "description": "User not found in the database, a new one was created and a time record"
                     },
                     400: {"model": HttpErrorResponseModel}
                 })
    async def create_user_log_for_time(
            *, session: Session = Depends(Database.get_session),
            body: Annotated[UserLogTimePayloadModel, Body(embed=False)]
    ) -> UserWithImageResponseModel:
        return UserController.create_user_time_record(session, body)
