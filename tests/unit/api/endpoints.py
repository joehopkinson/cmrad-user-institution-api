from unittest import mock

import pytest
from fastapi.testclient import TestClient

from cmrad_user_institution_api.api import models
from cmrad_user_institution_api.api.endpoints import app

client = TestClient(app)


@pytest.fixture(scope="function")
def test_client():
    return client


@mock.patch("cmrad_user_institution_api.domain.user_entity.uuid.uuid4")
def test_create_user(mock_uuid, test_client):
    user_id = "1"
    mock_uuid.return_value = user_id
    first_name = "John"
    last_name = "Doe"
    email_address = "john@doe.com"
    request = models.CreateUserRequest(
        first_name=first_name,
        last_name=last_name,
        email_address=email_address,
    )
    response = test_client.post("/users", json=request.model_dump())
    assert response.status_code == 201
    assert response.json() == {"message": f"User created with id: {user_id}"}


def test_get_user(test_client):
    pass


def test_get_users(test_client):
    pass


def test_update_user(test_client):
    pass


def test_delete_user(test_client):
    pass
