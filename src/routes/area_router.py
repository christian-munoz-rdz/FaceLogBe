from typing import Sequence

from fastapi import APIRouter, Body, Depends
from sqlmodel import Session
from typing_extensions import Annotated

from controllers.area_controller import AreaController
from database.services.database import Database
from models.requests.area_models import AreaPayloadModel, AreaResponseModel
from models.requests.http_models import HttpErrorResponseModel


class AreaRouter:
    router = APIRouter(prefix="/area", tags=["area"])

    @staticmethod
    @router.post("/",
                 responses={200: {"model": AreaResponseModel}, 400: {"model": HttpErrorResponseModel}}
                 )
    async def create_area(
            *, session: Session = Depends(Database.get_session), area: Annotated[AreaPayloadModel, Body(embed=False)],
    ) -> AreaResponseModel:
        return AreaController.create_new_area(session, area)

    @staticmethod
    @router.get("/{area_id}",
                responses={200: {"model": AreaResponseModel}, 404: {"model": HttpErrorResponseModel}}
                )
    async def get_area_by_id(
            *, session: Session = Depends(Database.get_session), area_id: int
    ) -> AreaResponseModel:
        return AreaController.get_area_by_id(session, area_id)

    @staticmethod
    @router.get("/",
                responses={200: {"model": Sequence[AreaResponseModel]}, 404: {"model": HttpErrorResponseModel}}
                )
    async def get_all_areas(
            *, session: Session = Depends(Database.get_session)
    ) -> Sequence[AreaResponseModel]:
        return AreaController.get_all_areas(session)


