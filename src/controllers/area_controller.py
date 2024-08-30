from typing import Sequence

from fastapi import HTTPException
from sqlmodel import Session

from builders.area_builder import AreaBuilder
from database.dao.area_dao import AreaDao
from models.errors.database_error import DatabaseException
from models.requests.area_models import AreaPayloadModel, AreaResponseModel
from services.image_service import ImageService


class AreaController:

    @staticmethod
    def create_new_area(session: Session, area: AreaPayloadModel) -> AreaResponseModel:
        try:
            if area.image and (not ImageService.is_valid_image(area.image)):
                raise HTTPException(status_code=400, detail="Invalid image")
            image = ImageService.convert_to_binary(area.image) if area.image else None
            area_db = AreaDao.create_area(session, area, image)
            area_response = AreaBuilder.build_area_response(area_db, area.image)
            session.commit()
            return area_response
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
            raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

    @staticmethod
    def get_area_by_id(session: Session, area_id: int) -> AreaResponseModel:
        try:
            area_db = AreaDao.get_area_by_id(session, area_id)
            image = ImageService.convert_to_array(area_db.image) if area_db.image else None
            area_response = AreaBuilder.build_area_response(area_db, image)
            session.commit()
            return area_response
        except DatabaseException as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=e.http_status_code, detail=e.error_message)
        except Exception as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

    @staticmethod
    def get_all_areas(session: Session) -> Sequence[AreaResponseModel]:
        try:
            area_list_db = AreaDao.get_area_list(session)
            image_list = [ImageService.convert_to_array(area.image) if area.image else None for area in area_list_db]
            area_list_response = AreaBuilder.build_area_list_response(area_list_db, image_list)
            session.commit()
            return area_list_response
        except DatabaseException as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=e.http_status_code, detail=e.error_message)
        except Exception as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")
