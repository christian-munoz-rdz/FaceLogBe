from typing import List, Sequence

from sqlalchemy import text
from sqlmodel import Session

from database.models.photo_embeddings import PhotoEmbeddingDb, UserFromEuclideanDistanceDb
from models.errors.database_error import DatabaseException


class PhotoEmbeddingDao:

    @staticmethod
    def save_bulk_photo_embeddings(session: Session, photo_embeddings: Sequence[PhotoEmbeddingDb]) -> Sequence[
        PhotoEmbeddingDb]:
        try:
            session.bulk_save_objects(photo_embeddings, return_defaults=True)
            for photo in photo_embeddings:
                if photo.id is None:
                    raise DatabaseException(http_status_code=500, error_message=f"Error saving photo {photo.type}")
            return photo_embeddings
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")

    @staticmethod
    def get_distance_squared_from_photo_embeddings(
            session: Session,
            embedding: List[float]
    ) -> UserFromEuclideanDistanceDb:
        try:
            target_statement = ''
            for i, value in enumerate(embedding):
                target_statement += 'SELECT %d AS dimension, %s AS value ' % (i, str(value))

                if i < len(embedding) - 1:
                    target_statement += ' UNION ALL '

            select_statement = f'''
                            SELECT * 
                            FROM (
                                SELECT user_id, SUM(subtract_dims) AS distance_squared
                                FROM (
                                    SELECT user_id, (source - target) * (source - target) AS subtract_dims
                                    FROM (
                                        SELECT user_photo.user_id, photo_embedding.value AS source, target.value AS target
                                        FROM user_photos user_photo
                                        LEFT JOIN photo_embeddings photo_embedding ON user_photo.id = photo_embedding.user_photo_id
                                        LEFT JOIN (
                                            {target_statement}  
                                        ) target ON photo_embedding.dimension = target.dimension
                                    ) AS diff
                                ) AS subquery
                                GROUP BY user_id
                            ) AS final
                            WHERE distance_squared < 100
                            ORDER BY distance_squared ASC
                        '''
            query = text(select_statement)
            result = session.exec(query).first()

            if result is None:
                raise DatabaseException(http_status_code=204, error_message="User not found")

            return result
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(http_status_code=500, error_message=f"Database error: {str(e)}")
