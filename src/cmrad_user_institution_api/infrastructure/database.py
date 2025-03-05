from sqlmodel import Session, SQLModel, create_engine

from cmrad_user_institution_api.infrastructure.settings import settings

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)


def get_db_session():
    with Session(engine) as session:
        yield session
