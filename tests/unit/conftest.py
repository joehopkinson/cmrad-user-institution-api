import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from user_institution_api.api.endpoints import app
from user_institution_api.infrastructure import database

client = TestClient(app)
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
session = Session(engine)


@pytest.fixture(scope="session", autouse=True)
def setup():
    SQLModel.metadata.create_all(engine)
    app.dependency_overrides[database.get_db_session] = lambda: session


@pytest.fixture(scope="function")
def mock_client():
    return client


@pytest.fixture(scope="function")
def mock_session():
    return session
