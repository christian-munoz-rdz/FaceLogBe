from typing import Optional
from sqlmodel import Field, SQLModel


class PhotoEmbeddingDb(SQLModel, table=True):
    __tablename__ = "photo_embeddings"
    id: Optional[int] = Field(primary_key=True)
    user_photo_id: Optional[int] = Field(foreign_key="user_photos.id")
    dimension: int
    value: float

class UserFromEuclideanDistanceDb(SQLModel):
    user_id: int
    distance_squared: float