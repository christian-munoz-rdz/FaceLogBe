from typing import Sequence

from sqlmodel import Session, select

from database.models.area_users import AreaUserDb
from database.models.users import UserDb
from enums.role_enum import RoleEnum
from models.errors.database_error import DatabaseException
from models.requests.user_models import UserPayloadModel
from models.types.user_types import UserCodeType


class UserDao:

    @staticmethod
    def create_user(session: Session, name: str, email: str, role_id: RoleEnum) -> UserDb:
        try:
            user_db = UserDb(name=name, email=email, role_id=role_id.value)
            session.add(user_db)
            session.flush([user_db])
            return user_db
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")

    @staticmethod
    def get_all(session: Session) -> Sequence[UserDb]:
        try:
            users = session.exec(select(UserDb)).all()
            if users is None:
                raise DatabaseException(http_status_code=204, error_message="No users found")
            return users
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")

    @staticmethod
    def get_user(session: Session, user_id: int) -> UserDb:
        try:
            user = session.exec(select(UserDb).where(UserDb.id == user_id)).first()
            if user is None:
                raise DatabaseException(http_status_code=204, error_message=f"User {user_id} not found")
            return user
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")

    @staticmethod
    def create_area_users(session: Session, user_id: int, areas: Sequence[int]) -> Sequence[AreaUserDb]:
        try:
            area_users_list_db = []
            for area in areas:
                area_users_db = AreaUserDb(user_id=user_id, user_type="user", area_id=area)
                session.add(area_users_db)
                area_users_list_db.append(area_users_db)
            session.flush(area_users_list_db)
            return area_users_list_db
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")


