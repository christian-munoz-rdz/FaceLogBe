from typing import Optional, Sequence

from sqlmodel import Session, select

from database.models.areas import AreaDb
from models.errors.database_error import DatabaseException
from models.requests.area_models import AreaPayloadModel


class AreaDao:

    @staticmethod
    def create_area(session: Session, area: AreaPayloadModel, image: Optional[bytes]) -> AreaDb:
        try:
            area_db = AreaDb(
                name=area.name,
                description=area.description,
                module=area.module,
                classroom=area.classroom,
                campus=area.campus,
                department=area.department,
                division=area.division,
                image=image
            )
            session.add(area_db)
            session.flush([area_db])
            return area_db
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")

    @staticmethod
    def get_area_by_id(session: Session, area_id: int) -> AreaDb:
        try:
            area = session.exec(select(AreaDb).where(AreaDb.id == area_id)).first()
            if area is None:
                raise DatabaseException(http_status_code=204, error_message=f"Area {area_id} not found")
            return area
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")

    @staticmethod
    def get_area_list(session: Session) -> Sequence[AreaDb]:
        try:
            area = session.exec(select(AreaDb).order_by(AreaDb.name)).all()
            if area is None:
                raise DatabaseException(http_status_code=204, error_message=f"Empty area list")
            return area
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")
