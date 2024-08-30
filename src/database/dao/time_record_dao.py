from datetime import datetime

from sqlmodel import Session, select, desc

from database.models.time_records import TimeRecordDb
from models.errors.database_error import DatabaseException


class TimeRecordDao:

    @staticmethod
    def create_time_record(session: Session, user_id: int, area_id: int, photo_id: int) -> TimeRecordDb:
        try:
            time_record_db = TimeRecordDb(user_id=user_id, area_id=area_id, enter_photo_id=photo_id)
            session.add(time_record_db)
            session.flush([time_record_db])
            return time_record_db
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")

    @staticmethod
    def add_exit_time(session: Session, time_record_db: TimeRecordDb, photo_id: int) -> TimeRecordDb:
        try:
            time_record_db.exited_at = datetime.now()
            time_record_db.exit_photo_id = photo_id
            session.add(time_record_db)
            session.flush([time_record_db])
            return time_record_db
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")

    @staticmethod
    def get_last_time_record(session: Session, user_id: int) -> TimeRecordDb:
        try:
            time_record_db = session.exec(
                select(TimeRecordDb)
                .where(TimeRecordDb.user_id == user_id)
                .order_by(desc(TimeRecordDb.created_at))
            ).first()
            return time_record_db
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")
