from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, Session
import os


class Database:

    sqlModel = SQLModel
    engine: Engine

    @staticmethod
    def start_database():
        Database.engine = create_engine(os.getenv("SQL_URL"), echo=False)
        Database.sqlModel.metadata.create_all(Database.engine)
        SQLModel.metadata.create_all(Database.engine)

    @staticmethod
    def get_session():
        with Session(Database.engine) as session:
            session.expire_on_commit = False
            yield session
