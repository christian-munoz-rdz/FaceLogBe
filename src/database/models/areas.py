from typing import Optional, List
from sqlmodel import Field, SQLModel


class AreaDb(SQLModel, table=True):
    __tablename__ = "areas"
    id: Optional[int] = Field(primary_key=True)
    name: str
    description: str
    module: str
    classroom: str
    campus: str
    department: str
    division: str
    image: Optional[bytes]
