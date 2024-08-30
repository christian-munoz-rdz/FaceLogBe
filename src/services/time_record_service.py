from datetime import datetime

from sqlmodel import Session


from database.dao.time_record_dao import TimeRecordDao
from database.models.areas import AreaDb
from database.models.time_records import TimeRecordDb
from database.models.user_photos import UserPhotoDb
from database.models.users import UserDb
from enums.time_record_enum import TimeRecordActionEnum
from models.errors.database_error import DatabaseException


class TimeRecordService:

    # TODO: Implement testing of this method once the rules are defined
    @staticmethod
    def create_time_record(
            session: Session,
            action: TimeRecordActionEnum,
            user_db: UserDb,
            area_db: AreaDb,
            user_photo_db: UserPhotoDb,
            transaction_time: datetime
    ) -> TimeRecordDb:
        # Doens't matter the action if the user was just created, always create a new time record
        if user_db.created_at > transaction_time:
            return TimeRecordDao.create_time_record(session, user_db.id, area_db.id, user_photo_db.id)

        prev_time_record = TimeRecordDao.get_last_time_record(session, user_db.id)
        if prev_time_record is None:
            return TimeRecordDao.create_time_record(session, user_db.id, area_db.id, user_photo_db.id)

        if action == TimeRecordActionEnum.ENTER: #TODO: define the rules for this
            # verify that previous time record was an exit
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            last_entry_is_from_today = (
                        prev_time_record.created_at.replace(hour=0, minute=0, second=0, microsecond=0)
                        >= today)
            if prev_time_record.exited_at is None and last_entry_is_from_today:
                raise DatabaseException(http_status_code=400, error_message="User already entered")
            return TimeRecordDao.create_time_record(session, user_db.id, area_db.id, user_photo_db.id)

        if action == TimeRecordActionEnum.EXIT: # TODO: define the rules for this
            # verify that previous time record was an entry
            if prev_time_record.exited_at is not None:
                raise DatabaseException(http_status_code=400, error_message="User already exited")

            return TimeRecordDao.add_exit_time(session, prev_time_record, user_photo_db.id)

