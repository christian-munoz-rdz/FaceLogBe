from typing import Sequence

from sqlmodel import Session, select

from database.models.users import UserDb
from models.errors.database_error import DatabaseException
from models.requests.user_models import UserPayloadModel


class UserDao:

    @staticmethod
    def create_user(session: Session, user: UserPayloadModel) -> UserDb:
        try:
            user_db = UserDb(name=user.name, email=user.email, role_id=user.role_id.value)
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
