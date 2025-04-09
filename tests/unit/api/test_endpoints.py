import uuid
from unittest import mock

import pytest

from user_institution_api.api import models
from user_institution_api.infrastructure import models as orm_models


@pytest.fixture
def mock_user_event():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email_address": "john@doe.com",
    }


@pytest.fixture
def mock_institution_event():
    return {
        "institution_name": "Test Institution",
    }


def create_user(session, user_id, user_event):
    user_orm = orm_models.UserORM(**user_event, user_id=user_id)
    session.add(user_orm)
    session.commit()
    session.refresh(user_orm)
    return user_orm


def create_institution(session, institution_id, institution_event):
    institution_orm = orm_models.InstitutionORM(
        **institution_event, institution_id=institution_id
    )
    session.add(institution_orm)
    session.commit()
    session.refresh(institution_orm)
    return institution_orm


def create_association(session, user_id, institution_id, is_primary):
    association_orm = orm_models.UserInstitutionORM(
        user_id=user_id,
        institution_id=institution_id,
        is_primary=is_primary,
    )
    session.add(association_orm)
    session.commit()
    session.refresh(association_orm)
    return association_orm


@mock.patch("user_institution_api.domain.user.uuid.uuid4")
def test_create_user(mock_uuid, mock_client, mock_session, mock_user_event):
    user_id = str(uuid.uuid4())
    mock_uuid.return_value = user_id

    request = models.CreateUserRequest(**mock_user_event)
    response = mock_client.post("/users", json=request.model_dump())
    assert response.status_code == 201
    assert response.json() == {
        "message": f"User created successfully",
        "user_id": user_id,
    }
    assert mock_session.get(orm_models.UserORM, user_id).model_dump() == {
        **mock_user_event,
        "user_id": user_id,
    }


def test_get_user(mock_client, mock_session, mock_user_event):
    # Prepare existing user
    user_id = str(uuid.uuid4())
    user_orm = create_user(mock_session, user_id, mock_user_event)

    response = mock_client.get(f"/users/{user_orm.user_id}")
    assert response.status_code == 200
    assert response.json() == {**mock_user_event, "user_id": user_orm.user_id}


def test_update_user(mock_client, mock_session, mock_user_event):
    user_id = str(uuid.uuid4())
    create_user(mock_session, user_id, mock_user_event)

    new_email_address = "john@doe.co.uk"
    request = models.UpdateUserRequest(email_address=new_email_address)
    response = mock_client.patch(f"/users/{user_id}", json=request.model_dump())
    assert response.status_code == 201
    assert response.json() == {
        "user_id": user_id,
        "email_address": new_email_address,
        "first_name": mock_user_event["first_name"],
        "last_name": mock_user_event["last_name"],
    }


def test_add_user_institution_association(
    mock_client, mock_session, mock_user_event, mock_institution_event
):
    user_id = str(uuid.uuid4())
    create_user(mock_session, user_id, mock_user_event)
    institution1_id = str(uuid.uuid4())
    create_institution(mock_session, institution1_id, mock_institution_event)

    request = models.AddUserInstitutionAssociationRequest(is_primary=False)
    response1 = mock_client.post(
        f"/users/{user_id}/institutions/{institution1_id}", json=request.model_dump()
    )
    assert response1.status_code == 201
    assert response1.json() == {
        "message": "Association created successfully",
        "user_id": user_id,
        "institution_id": institution1_id,
    }
    assert mock_session.get(
        orm_models.UserInstitutionORM, (user_id, institution1_id)
    ).model_dump() == {
        "user_id": user_id,
        "institution_id": institution1_id,
        "is_primary": False,
    }

    # Validate user can have multiple non-primary associations
    institution2_id = str(uuid.uuid4())
    create_institution(mock_session, institution2_id, mock_institution_event)
    mock_client.post(
        f"/users/{user_id}/institutions/{institution2_id}", json=request.model_dump()
    )
    assert mock_session.get(
        orm_models.UserInstitutionORM, (user_id, institution2_id)
    ).model_dump() == {
        "user_id": user_id,
        "institution_id": institution2_id,
        "is_primary": False,
    }


def test_add_primary_user_institution_association(
    mock_client, mock_session, mock_user_event, mock_institution_event
):
    user_id = str(uuid.uuid4())
    create_user(mock_session, user_id, mock_user_event)
    institution1_id = str(uuid.uuid4())
    create_institution(mock_session, institution1_id, mock_institution_event)

    request_primary = models.AddUserInstitutionAssociationRequest(is_primary=True)
    response1 = mock_client.post(
        f"/users/{user_id}/institutions/{institution1_id}",
        json=request_primary.model_dump(),
    )
    assert response1.status_code == 201
    assert response1.json() == {
        "message": "Association created successfully",
        "user_id": user_id,
        "institution_id": institution1_id,
    }
    assert mock_session.get(
        orm_models.UserInstitutionORM, (user_id, institution1_id)
    ).model_dump() == {
        "user_id": user_id,
        "institution_id": institution1_id,
        "is_primary": True,
    }

    # Validate user can have only one primary association
    institution2_id = str(uuid.uuid4())
    create_institution(mock_session, institution2_id, mock_institution_event)
    response2 = mock_client.post(
        f"/users/{user_id}/institutions/{institution2_id}",
        json=request_primary.model_dump(),
    )
    assert response2.status_code == 400
    assert response2.json() == {
        "detail": "Invalid user-institution association",
    }

    request_non_primary = models.AddUserInstitutionAssociationRequest(is_primary=False)
    response3 = mock_client.post(
        f"/users/{user_id}/institutions/{institution2_id}",
        json=request_non_primary.model_dump(),
    )
    assert response3.status_code == 201
    assert response3.json() == {
        "message": "Association created successfully",
        "user_id": user_id,
        "institution_id": institution2_id,
    }


def test_get_user_institution_associations(
    mock_client, mock_session, mock_user_event, mock_institution_event
):
    user_id = str(uuid.uuid4())
    create_user(mock_session, user_id, mock_user_event)
    institution1_id = str(uuid.uuid4())
    create_institution(mock_session, institution1_id, mock_institution_event)
    create_association(mock_session, user_id, institution1_id, is_primary=False)

    institution2_id = str(uuid.uuid4())
    create_institution(mock_session, institution2_id, mock_institution_event)
    create_association(mock_session, user_id, institution2_id, is_primary=True)

    response = mock_client.get(f"/users/{user_id}/institutions")
    assert response.status_code == 200

    expected_response = {
        "user_id": user_id,
        "institution_ids": {institution1_id, institution2_id},
        "primary_institution_id": institution2_id,
    }
    actual_response = response.json()
    actual_response["institution_ids"] = set(actual_response["institution_ids"])
    assert actual_response == expected_response


def test_get_institution(
    mock_client, mock_session, mock_user_event, mock_institution_event
):
    user_id = str(uuid.uuid4())
    create_user(mock_session, user_id, mock_user_event)
    institution_id = str(uuid.uuid4())
    create_institution(mock_session, institution_id, mock_institution_event)
    create_association(mock_session, user_id, institution_id, is_primary=False)

    response = mock_client.get(f"/institutions/{institution_id}")
    assert response.status_code == 200
    assert response.json() == {
        "institution_id": institution_id,
        "institution_name": "Test Institution",
        "user_count": 1,
    }


def test_add_user_institution_association_invalid(mock_client, mock_session):
    pass


def test_get_users(mock_client):
    pass


def test_delete_user(mock_client):
    pass


def test_create_institution(mock_client):
    pass


def test_get_institutions(mock_client):
    pass


def test_update_institution(mock_client):
    pass


def test_delete_institution(mock_client):
    pass
