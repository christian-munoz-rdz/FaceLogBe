from typing import List, Sequence

from sqlmodel import Session, select

from database.models.user_codes import UserCodeDb
from database.models.users import UserDb
from models.errors.database_error import DatabaseException
from models.types.user_types import UserCodeType


class UserCodeDao:

    @staticmethod
    def create_bulk_user_codes(session: Session, user_db: UserDb, user_codes: Sequence[UserCodeType]) -> Sequence[UserCodeDb]:
        try:
            created_codes_db = []
            for user_code in user_codes:
                user_code_db = UserCodeDb(user_id=user_db.id, code=user_code.code, category=user_code.category)
                session.add(user_code_db)
                created_codes_db.append(user_code_db)
            session.flush(created_codes_db)
            return created_codes_db
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")

    @staticmethod
    def get_all_user_codes(session: Session, user_id: int) -> Sequence[UserCodeDb]:
        try:
            codes = session.exec(select(UserCodeDb).where(UserCodeDb.user_id == user_id)).all()
            if codes is None:
                raise DatabaseException(http_status_code=204, error_message="No user codes found")
            return codes
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")