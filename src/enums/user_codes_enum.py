from enum import Enum


class UserCodeCategoryEnum(str, Enum):
    STUDENT = 'STUDENT'
    GRADUATE = 'GRADUATE'
    TEACHER = 'TEACHER'
    RECTOR = 'RECTOR'
    ADMINISTRATIVE = 'ADMINISTRATIVE'
    VOLUNTEER = 'VOLUNTEER'
    UNKNOWN = 'UNKNOWN'
