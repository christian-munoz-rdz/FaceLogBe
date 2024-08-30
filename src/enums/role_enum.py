from enum import Enum


class RoleEnum(int, Enum):
    SUPERUSER = 1
    DEVELOPER = 2
    WRITER = 3
    REGULAR = 4
    NONE = 5
